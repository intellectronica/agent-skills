#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "google-genai>=1.65.0",
#     "pillow>=12.1.1",
#     "requests>=2.32.0",
# ]
# ///
"""
Generate and edit images using Nano Banana 2 via Gemini or Atlas Cloud.

Usage examples:
    uv run ./.agents/skills/nano-banana-2/scripts/generate_image.py \
      --prompt "A serene Japanese garden at sunrise" \
      --filename "output.png" \
      --resolution 2K \
      --aspect-ratio 16:9

    uv run ./.agents/skills/nano-banana-2/scripts/generate_image.py \
      --prompt "Turn this into a cinematic poster" \
      --filename "edited.png" \
      --input-image "input.png" \
      --resolution 4K
"""

import argparse
import os
import re
import sys
import time
from io import BytesIO
from pathlib import Path
from urllib.parse import urljoin, urlparse

SUPPORTED_ASPECT_RATIOS = [
    "1:1",
    "1:4",
    "1:8",
    "2:3",
    "3:2",
    "3:4",
    "4:1",
    "4:3",
    "4:5",
    "5:4",
    "8:1",
    "9:16",
    "16:9",
    "21:9",
]
SUPPORTED_RESOLUTIONS = ["512px", "1K", "2K", "4K"]
MAX_REFERENCE_IMAGES = 14
ATLAS_API_BASE = "https://api.atlascloud.ai/api/v1"
ATLAS_TEXT_MODEL = "google/nano-banana-2/text-to-image"
ATLAS_EDIT_MODEL = "google/nano-banana-2/edit"
ATLAS_ASPECT_RATIOS = {
    "1:1",
    "3:2",
    "2:3",
    "3:4",
    "4:3",
    "4:5",
    "5:4",
    "9:16",
    "16:9",
    "21:9",
}
ATLAS_TERMINAL_SUCCESS = {"completed", "succeeded"}
ATLAS_TERMINAL_FAILURE = {"failed", "timeout", "canceled", "cancelled"}
ATLAS_OUTPUT_HOST_SUFFIXES = (".atlascloud.ai", ".aliyuncs.com")
ATLAS_MAX_DOWNLOAD_BYTES = 64 * 1024 * 1024
ATLAS_MAX_REDIRECTS = 3


def get_gemini_api_key(provided_key: str | None) -> str | None:
    """Get Gemini API key from argument first, then environment."""
    if provided_key:
        return provided_key
    return os.environ.get("GEMINI_API_KEY")


def get_atlas_api_key(provided_key: str | None) -> str | None:
    """Get Atlas API key from argument first, then environment."""
    if provided_key:
        return provided_key
    return os.environ.get("ATLASCLOUD_API_KEY")


def save_png(image, output_path: Path) -> None:
    """Save image as PNG in RGB mode."""
    if image.mode == "RGBA":
        rgb_image = image.convert("RGB")
        rgb_image.save(str(output_path), "PNG")
    elif image.mode == "RGB":
        image.save(str(output_path), "PNG")
    else:
        image.convert("RGB").save(str(output_path), "PNG")


def auto_detect_resolution(input_images, user_resolution: str) -> str:
    """Auto-select output size from input references when user left default 1K."""
    if user_resolution != "1K" or not input_images:
        return user_resolution

    max_dim = max(max(image.size) for image in input_images)
    if max_dim >= 3000:
        return "4K"
    if max_dim >= 1500:
        return "2K"
    if max_dim <= 640:
        return "512px"
    return "1K"


def _atlas_data(response) -> dict:
    """Validate an Atlas response and return its data object."""
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise TypeError("Atlas Cloud returned a non-object response")
    code = payload.get("code")
    if code not in (None, 200):
        message = payload.get("message") or payload.get("error") or f"code {code}"
        raise RuntimeError(f"Atlas Cloud request failed: {message}")
    data = payload.get("data", payload)
    if not isinstance(data, dict):
        raise TypeError("Atlas Cloud response is missing a data object")
    return data


def _validate_atlas_media_url(url: str) -> str:
    """Allow downloads only from known HTTPS media hosts."""
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if (
        parsed.scheme != "https"
        or parsed.username
        or parsed.password
        or parsed.port not in (None, 443)
        or not any(
            host == suffix[1:] or host.endswith(suffix)
            for suffix in ATLAS_OUTPUT_HOST_SUFFIXES
        )
    ):
        raise RuntimeError(f"Refusing untrusted Atlas media URL: {url}")
    return url


def _upload_atlas_image(session, path: Path, api_key: str) -> str:
    """Upload one reference image exactly once."""
    with path.open("rb") as handle:
        response = session.post(
            f"{ATLAS_API_BASE}/model/uploadMedia",
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": (path.name, handle, "application/octet-stream")},
            timeout=(10, 120),
        )
    data = _atlas_data(response)
    url = data.get("download_url") or data.get("url")
    if not isinstance(url, str) or not url:
        raise RuntimeError("Atlas Cloud upload response is missing download_url")
    return _validate_atlas_media_url(url)


def _atlas_outputs(data: dict) -> list[str]:
    outputs = data.get("outputs") or []
    if isinstance(outputs, str):
        outputs = [outputs]
    if not isinstance(outputs, list):
        raise TypeError("Atlas Cloud returned an invalid outputs value")
    return [item for item in outputs if isinstance(item, str) and item]


def _poll_atlas_prediction(
    session,
    prediction_id: str,
    api_key: str,
    *,
    attempts: int = 30,
    initial_delay: float = 3.0,
    sleep=time.sleep,
) -> list[str]:
    """Poll a prediction with bounded GET-only backoff."""
    if not re.fullmatch(r"[A-Za-z0-9_-]+", prediction_id):
        raise RuntimeError("Atlas Cloud returned an invalid prediction id")

    delay = initial_delay
    for attempt in range(attempts):
        response = session.get(
            f"{ATLAS_API_BASE}/model/prediction/{prediction_id}",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30,
        )
        data = _atlas_data(response)
        status = str(data.get("status", "")).lower()
        if status in ATLAS_TERMINAL_SUCCESS:
            outputs = _atlas_outputs(data)
            if not outputs:
                raise RuntimeError("Atlas Cloud completed without an output URL")
            return outputs
        if status in ATLAS_TERMINAL_FAILURE:
            error = data.get("error") or data.get("message") or status
            raise RuntimeError(f"Atlas Cloud generation failed: {error}")
        if attempt + 1 < attempts:
            sleep(delay)
            delay = min(delay * 1.5, 12.0)

    raise TimeoutError(f"Atlas Cloud prediction did not finish after {attempts} checks")


def _download_atlas_image(session, url: str, output_path: Path, pil_image) -> None:
    """Download one trusted output and normalize it to PNG.

    Redirects are followed manually so every hop is validated *before* it is
    requested, and the body is streamed so the size limit is enforced while
    reading instead of after the whole response is buffered.
    """
    current = _validate_atlas_media_url(url)
    for _ in range(ATLAS_MAX_REDIRECTS + 1):
        response = session.get(
            current, timeout=(10, 120), allow_redirects=False, stream=True
        )
        try:
            if getattr(response, "is_redirect", False):
                location = (getattr(response, "headers", None) or {}).get("Location")
                if not location:
                    raise RuntimeError("Atlas Cloud output redirect has no Location")
                current = _validate_atlas_media_url(urljoin(current, location))
                continue
            response.raise_for_status()
            declared = (getattr(response, "headers", None) or {}).get("Content-Length")
            if declared and declared.isdigit() and int(declared) > ATLAS_MAX_DOWNLOAD_BYTES:
                raise RuntimeError("Atlas Cloud output exceeds the 64 MiB download limit")
            chunks: list[bytes] = []
            received = 0
            for chunk in response.iter_content(chunk_size=64 * 1024):
                received += len(chunk)
                if received > ATLAS_MAX_DOWNLOAD_BYTES:
                    raise RuntimeError(
                        "Atlas Cloud output exceeds the 64 MiB download limit"
                    )
                chunks.append(chunk)
        finally:
            close = getattr(response, "close", None)
            if close:
                close()
        image = pil_image.open(BytesIO(b"".join(chunks)))
        save_png(image, output_path)
        return
    raise RuntimeError("Atlas Cloud output redirected too many times")


def generate_with_atlas(
    session,
    *,
    api_key: str,
    prompt: str,
    output_path: Path,
    input_paths: list[Path],
    resolution: str,
    aspect_ratio: str | None,
    pil_image,
    sleep=time.sleep,
) -> list[Path]:
    """Generate through Atlas using one submit POST and bounded polling."""
    images = [_upload_atlas_image(session, path, api_key) for path in input_paths]
    model = ATLAS_EDIT_MODEL if images else ATLAS_TEXT_MODEL
    payload = {
        "model": model,
        "prompt": prompt,
        "resolution": resolution.lower(),
        "output_format": "png",
        "enable_sync_mode": False,
        "enable_base64_output": False,
    }
    if aspect_ratio:
        payload["aspect_ratio"] = aspect_ratio
    if images:
        payload["images"] = images

    response = session.post(
        f"{ATLAS_API_BASE}/model/generateImage",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=(10, 120),
    )
    data = _atlas_data(response)
    outputs = _atlas_outputs(data)
    status = str(data.get("status", "")).lower()
    if status in ATLAS_TERMINAL_FAILURE:
        error = data.get("error") or data.get("message") or status
        raise RuntimeError(f"Atlas Cloud generation failed: {error}")
    if status not in ATLAS_TERMINAL_SUCCESS or not outputs:
        prediction_id = data.get("id")
        if not isinstance(prediction_id, str) or not prediction_id:
            raise RuntimeError("Atlas Cloud response is missing a prediction id")
        outputs = _poll_atlas_prediction(session, prediction_id, api_key, sleep=sleep)

    saved_paths = []
    for index, url in enumerate(outputs, start=1):
        current_path = (
            output_path
            if index == 1
            else output_path.with_name(
                f"{output_path.stem}-{index}{output_path.suffix or '.png'}"
            )
        )
        _download_atlas_image(session, url, current_path, pil_image)
        saved_paths.append(current_path.resolve())
    return saved_paths


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate/edit images with Nano Banana 2 via Gemini or Atlas Cloud"
    )
    parser.add_argument(
        "--prompt", "-p", required=True, help="Image prompt/instructions"
    )
    parser.add_argument(
        "--filename", "-f", required=True, help="Output filename (.png recommended)"
    )
    parser.add_argument(
        "--provider",
        choices=["gemini", "atlas"],
        default="gemini",
        help="API provider. Default: gemini",
    )
    parser.add_argument(
        "--input-image",
        "-i",
        action="append",
        default=[],
        help=(
            "Optional reference/input image path. Repeat flag for multiple images "
            f"(up to {MAX_REFERENCE_IMAGES})."
        ),
    )
    parser.add_argument(
        "--resolution",
        "-r",
        choices=SUPPORTED_RESOLUTIONS,
        default="1K",
        help="Output resolution: 512px, 1K (default), 2K, or 4K",
    )
    parser.add_argument(
        "--aspect-ratio",
        "-a",
        choices=SUPPORTED_ASPECT_RATIOS,
        help="Optional output aspect ratio",
    )
    parser.add_argument(
        "--api-key", "-k", help="Gemini API key (overrides GEMINI_API_KEY)"
    )
    parser.add_argument(
        "--atlas-api-key",
        help="Atlas Cloud API key (overrides ATLASCLOUD_API_KEY)",
    )

    args = parser.parse_args()

    api_key = (
        get_atlas_api_key(args.atlas_api_key)
        if args.provider == "atlas"
        else get_gemini_api_key(args.api_key)
    )
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        if args.provider == "atlas":
            print("Provide --atlas-api-key or set ATLASCLOUD_API_KEY.", file=sys.stderr)
        else:
            print("Provide --api-key or set GEMINI_API_KEY.", file=sys.stderr)
        sys.exit(1)

    if len(args.input_image) > MAX_REFERENCE_IMAGES:
        print(
            f"Error: Too many input images ({len(args.input_image)}). "
            f"Maximum supported: {MAX_REFERENCE_IMAGES}.",
            file=sys.stderr,
        )
        sys.exit(1)

    from PIL import Image as PILImage

    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    input_images = []
    if args.input_image:
        for image_path in args.input_image:
            try:
                with PILImage.open(image_path) as opened_image:
                    image = opened_image.copy()
                input_images.append(image)
                print(f"Loaded input image: {image_path}")
            except Exception as exc:  # noqa: BLE001 - CLI boundary reports decoder errors
                print(
                    f"Error loading input image '{image_path}': {exc}", file=sys.stderr
                )
                sys.exit(1)

    output_resolution = auto_detect_resolution(input_images, args.resolution)

    if args.provider == "atlas":
        if args.resolution == "512px":
            print(
                "Error: Atlas Cloud supports 1K, 2K, and 4K for this model.",
                file=sys.stderr,
            )
            sys.exit(1)
        if output_resolution == "512px":
            output_resolution = "1K"
        if args.aspect_ratio and args.aspect_ratio not in ATLAS_ASPECT_RATIOS:
            print(
                "Error: Atlas Cloud does not support this aspect ratio for Nano Banana 2. "
                f"Use: {', '.join(sorted(ATLAS_ASPECT_RATIOS))}.",
                file=sys.stderr,
            )
            sys.exit(1)

        import requests

        try:
            saved_paths = generate_with_atlas(
                requests.Session(),
                api_key=api_key,
                prompt=args.prompt,
                output_path=output_path,
                input_paths=[Path(path) for path in args.input_image],
                resolution=output_resolution,
                aspect_ratio=args.aspect_ratio,
                pil_image=PILImage,
            )
        except Exception as exc:  # noqa: BLE001 - CLI boundary reports provider errors
            print(f"Error generating image: {exc}", file=sys.stderr)
            sys.exit(1)

        print("\nSaved image file(s):")
        for path in saved_paths:
            print(path)
        return

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    image_config_kwargs = {"image_size": output_resolution}
    if args.aspect_ratio:
        image_config_kwargs["aspect_ratio"] = args.aspect_ratio

    if input_images:
        contents = [args.prompt, *input_images]
        print(
            "Editing/generating from references "
            f"({len(input_images)} image(s)), resolution {output_resolution}"
            + (f", aspect ratio {args.aspect_ratio}" if args.aspect_ratio else "")
            + "..."
        )
    else:
        contents = [args.prompt]
        print(
            f"Generating image with resolution {output_resolution}"
            + (f", aspect ratio {args.aspect_ratio}" if args.aspect_ratio else "")
            + "..."
        )

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-image-preview",
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(**image_config_kwargs),
            ),
        )

        image_parts = 0
        saved_paths = []

        for part in response.parts:
            if part.text is not None:
                print(f"Model response: {part.text}")
            elif part.inline_data is not None:
                image_parts += 1

                image_data = part.inline_data.data
                if isinstance(image_data, str):
                    import base64

                    image_data = base64.b64decode(image_data)

                image = PILImage.open(BytesIO(image_data))

                if image_parts == 1:
                    current_path = output_path
                else:
                    current_path = output_path.with_name(
                        f"{output_path.stem}-{image_parts}{output_path.suffix or '.png'}"
                    )

                save_png(image, current_path)
                saved_paths.append(current_path.resolve())

        if saved_paths:
            print("\nSaved image file(s):")
            for path in saved_paths:
                print(path)
        else:
            print("Error: No image was generated in the response.", file=sys.stderr)
            sys.exit(1)

    except Exception as exc:  # noqa: BLE001 - existing CLI boundary reports SDK errors
        print(f"Error generating image: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
