#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "openai>=1.50.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Generate and edit images using OpenAI's GPT Image 1.5 model via the Responses API.

Usage:
    # Generate new image
    uv run generate_image.py --prompt "description" --filename "output.png" [options]

    # Edit image (conversational, no mask)
    uv run generate_image.py --prompt "edit instructions" --filename "output.png" --input-image "input.png" [options]

    # Edit image with mask (precise inpainting)
    uv run generate_image.py --prompt "what to add" --filename "output.png" --input-image "input.png" --mask "mask.png" [options]
"""

import argparse
import base64
import os
import sys
from io import BytesIO
from pathlib import Path


def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument first, then environment."""
    if provided_key:
        return provided_key
    return os.environ.get("OPENAI_API_KEY")


def create_full_transparent_mask(image_path: str) -> bytes:
    """Create a fully transparent PNG mask matching the input image dimensions."""
    from PIL import Image

    with Image.open(image_path) as img:
        width, height = img.size

    # Create fully transparent image (all pixels have alpha=0)
    mask = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    buf = BytesIO()
    mask.save(buf, format="PNG")
    return buf.getvalue()


def generate_image_responses_api(
    client,
    prompt: str,
    quality: str = "medium",
    size: str = "1024x1024",
    background: str = "auto",
) -> bytes:
    """Generate image using the Responses API with gpt-image-1.5."""

    # Build tool configuration for image generation
    tool_config = {
        "type": "image_generation",
        "quality": quality,
    }

    # Add size if not auto
    if size != "auto":
        tool_config["size"] = size

    # Add background setting
    if background != "auto":
        tool_config["background"] = background

    # Call the Responses API
    response = client.responses.create(
        model="gpt-4.1",  # Model that orchestrates the image generation tool
        input=prompt,
        tools=[tool_config],
    )

    # Extract the generated image
    for output in response.output:
        if output.type == "image_generation_call":
            return base64.b64decode(output.result)

    raise RuntimeError("No image was generated in the response")


def edit_image_with_mask(
    client,
    prompt: str,
    image_path: str,
    mask_path: str | None,
    size: str = "1024x1024",
) -> bytes:
    """Edit image using the Image API with mask support."""
    from PIL import Image

    # If no mask provided, create a fully transparent one (edit entire image)
    if mask_path:
        mask_file = open(mask_path, "rb")
    else:
        mask_bytes = create_full_transparent_mask(image_path)
        mask_file = BytesIO(mask_bytes)
        mask_file.name = "mask.png"

    try:
        result = client.images.edit(
            model="gpt-image-1.5",
            image=open(image_path, "rb"),
            mask=mask_file,
            prompt=prompt,
            size=size if size != "auto" else "1024x1024",
        )

        image_base64 = result.data[0].b64_json
        return base64.b64decode(image_base64)
    finally:
        if mask_path:
            mask_file.close()


def main():
    parser = argparse.ArgumentParser(
        description="Generate and edit images using OpenAI GPT Image 1.5"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Image description or editing instructions"
    )
    parser.add_argument(
        "--filename", "-f",
        required=True,
        help="Output filename (e.g., output.png)"
    )
    parser.add_argument(
        "--input-image", "-i",
        help="Optional input image path for editing"
    )
    parser.add_argument(
        "--mask", "-m",
        help="Optional mask image path for precise inpainting (PNG with transparent areas to edit)"
    )
    parser.add_argument(
        "--quality", "-q",
        choices=["low", "medium", "high"],
        default="medium",
        help="Output quality: low, medium (default), or high"
    )
    parser.add_argument(
        "--size", "-s",
        choices=["1024x1024", "1024x1536", "1536x1024", "auto"],
        default="1024x1024",
        help="Output size (default: 1024x1024)"
    )
    parser.add_argument(
        "--background", "-b",
        choices=["transparent", "opaque", "auto"],
        default="auto",
        help="Background type for generation (default: auto)"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="OpenAI API key (overrides OPENAI_API_KEY env var)"
    )

    args = parser.parse_args()

    # Get API key
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set OPENAI_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    # Import here after checking API key to avoid slow import on error
    from openai import OpenAI

    # Initialise client
    client = OpenAI(api_key=api_key)

    # Set up output path
    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Determine operation mode
    if args.input_image:
        # Validate input image exists
        if not Path(args.input_image).exists():
            print(f"Error: Input image not found: {args.input_image}", file=sys.stderr)
            sys.exit(1)

        if args.mask:
            # Validate mask exists
            if not Path(args.mask).exists():
                print(f"Error: Mask image not found: {args.mask}", file=sys.stderr)
                sys.exit(1)

            print(f"Editing image with mask using Image API...")
            print(f"  Input: {args.input_image}")
            print(f"  Mask: {args.mask}")
            print(f"  Size: {args.size}")

            try:
                image_bytes = edit_image_with_mask(
                    client,
                    args.prompt,
                    args.input_image,
                    args.mask,
                    args.size,
                )
            except Exception as e:
                print(f"Error editing image with mask: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            # Edit without mask - use Image API with auto-generated full mask
            print(f"Editing image using Image API (full image edit)...")
            print(f"  Input: {args.input_image}")
            print(f"  Size: {args.size}")

            try:
                image_bytes = edit_image_with_mask(
                    client,
                    args.prompt,
                    args.input_image,
                    None,  # No mask - will create full transparent mask
                    args.size,
                )
            except Exception as e:
                print(f"Error editing image: {e}", file=sys.stderr)
                sys.exit(1)
    else:
        # Generation mode - use Responses API
        print(f"Generating image using Responses API...")
        print(f"  Quality: {args.quality}")
        print(f"  Size: {args.size}")
        print(f"  Background: {args.background}")

        try:
            image_bytes = generate_image_responses_api(
                client,
                args.prompt,
                args.quality,
                args.size,
                args.background,
            )
        except Exception as e:
            print(f"Error generating image: {e}", file=sys.stderr)
            sys.exit(1)

    # Save the image
    from PIL import Image

    image = Image.open(BytesIO(image_bytes))

    # Handle format conversion if needed
    if args.background == "transparent" or output_path.suffix.lower() == ".png":
        # Keep RGBA for transparent or PNG output
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        image.save(str(output_path), "PNG")
    else:
        # Convert to RGB for non-transparent output
        if image.mode == "RGBA":
            rgb_image = Image.new("RGB", image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[3])
            rgb_image.save(str(output_path), "PNG")
        elif image.mode == "RGB":
            image.save(str(output_path), "PNG")
        else:
            image.convert("RGB").save(str(output_path), "PNG")

    full_path = output_path.resolve()
    print(f"\nImage saved: {full_path}")


if __name__ == "__main__":
    main()
