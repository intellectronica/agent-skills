#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Lorem ipsum generator script.

Usage:
    uv run generate.py [options]

Options:
    --paragraphs N      Number of paragraphs (default: 3)
    --sentences N       Sentences per paragraph (default: 5)
    --words N           Approximate total word count
    --characters N      Exact number of characters (truncates to match)
    --tokens N          Estimated LLM token count (~4 chars/token)
    --continuous        Output as continuous text without paragraph breaks
    --headings N        Number of sections with headings (each gets paragraphs underneath)
    --bullets N         Number of bullet points per section (use with --headings)
    --numbered          Use numbered lists instead of bullets
    --mixed N           Generate realistic document with N sections, varied content types
    --output FILE       Write to file instead of stdout
    --format FORMAT     Output format: text, markdown, html (default: markdown)
"""

import argparse
import random
import sys

# Classic lorem ipsum vocabulary
WORDS = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
    "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
    "magna", "aliqua", "enim", "ad", "minim", "veniam", "quis", "nostrud",
    "exercitation", "ullamco", "laboris", "nisi", "aliquip", "ex", "ea", "commodo",
    "consequat", "duis", "aute", "irure", "in", "reprehenderit", "voluptate",
    "velit", "esse", "cillum", "fugiat", "nulla", "pariatur", "excepteur", "sint",
    "occaecat", "cupidatat", "non", "proident", "sunt", "culpa", "qui", "officia",
    "deserunt", "mollit", "anim", "id", "est", "laborum", "perspiciatis", "unde",
    "omnis", "iste", "natus", "error", "voluptatem", "accusantium", "doloremque",
    "laudantium", "totam", "rem", "aperiam", "eaque", "ipsa", "quae", "ab", "illo",
    "inventore", "veritatis", "quasi", "architecto", "beatae", "vitae", "dicta",
    "explicabo", "nemo", "ipsam", "quia", "voluptas", "aspernatur", "aut", "odit",
    "fugit", "consequuntur", "magni", "dolores", "eos", "ratione", "sequi",
    "nesciunt", "neque", "porro", "quisquam", "nihil", "numquam", "eius", "modi",
    "tempora", "corporis", "suscipit", "laboriosam", "aliquid", "commodi",
    "consequatur", "autem", "vel", "eum", "iure", "quam", "nihil", "molestiae",
    "illum", "quo", "maxime", "placeat", "facere", "possimus", "assumenda",
    "repellendus", "temporibus", "quibusdam", "officiis", "debitis", "rerum",
    "necessitatibus", "saepe", "eveniet", "voluptates", "repudiandae", "recusandae",
    "itaque", "earum", "hic", "tenetur", "sapiente", "delectus", "reiciendis",
    "voluptatibus", "maiores", "alias", "perferendis", "doloribus", "asperiores",
    "repellat"
]

# Canonical opening
OPENING = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."


def generate_word():
    return random.choice(WORDS)


def generate_words(count):
    return [generate_word() for _ in range(count)]


def generate_sentence(min_words=6, max_words=15):
    length = random.randint(min_words, max_words)
    words = generate_words(length)
    words[0] = words[0].capitalize()
    return " ".join(words) + "."


def generate_paragraph(sentences=5, use_opening=False):
    result = []
    for i in range(sentences):
        if i == 0 and use_opening:
            result.append(OPENING)
        else:
            result.append(generate_sentence())
    return " ".join(result)


def generate_heading():
    word_count = random.randint(2, 4)
    words = generate_words(word_count)
    return " ".join(w.capitalize() for w in words)


def generate_bullet_item():
    word_count = random.randint(4, 10)
    words = generate_words(word_count)
    words[0] = words[0].capitalize()
    return " ".join(words)


def format_output(content, fmt, is_heading=False, heading_level=2):
    if fmt == "html":
        if is_heading:
            return f"<h{heading_level}>{content}</h{heading_level}>"
        return f"<p>{content}</p>"
    elif fmt == "markdown":
        if is_heading:
            return "#" * heading_level + " " + content
        return content
    else:  # plain text
        return content


def format_list_item(content, fmt, numbered=False, index=1):
    if fmt == "html":
        return f"<li>{content}</li>"
    elif fmt == "markdown":
        if numbered:
            return f"{index}. {content}"
        return f"- {content}"
    else:
        if numbered:
            return f"{index}. {content}"
        return f"* {content}"


def generate_mixed_section(fmt, use_opening=False):
    """Generate a section with varied content types."""
    lines = []

    # Choose section structure randomly
    structure = random.choice([
        "paragraphs",           # Just paragraphs
        "bullets",              # Just bullet list
        "numbered",             # Just numbered list
        "para_then_bullets",    # Paragraph intro + bullets
        "para_then_numbered",   # Paragraph intro + numbered
        "subheadings",          # Subheadings with paragraphs
        "subheadings_mixed",    # Subheadings with mixed content
    ])

    if structure == "paragraphs":
        num_paras = random.randint(1, 3)
        for i in range(num_paras):
            para = generate_paragraph(random.randint(3, 6), use_opening=(i == 0 and use_opening))
            lines.append(format_output(para, fmt))
            lines.append("")

    elif structure == "bullets":
        num_bullets = random.randint(3, 7)
        if fmt == "html":
            lines.append("<ul>")
        for i in range(num_bullets):
            item = generate_bullet_item()
            lines.append(format_list_item(item, fmt, numbered=False, index=i+1))
        if fmt == "html":
            lines.append("</ul>")
        lines.append("")

    elif structure == "numbered":
        num_items = random.randint(3, 6)
        if fmt == "html":
            lines.append("<ol>")
        for i in range(num_items):
            item = generate_bullet_item()
            lines.append(format_list_item(item, fmt, numbered=True, index=i+1))
        if fmt == "html":
            lines.append("</ol>")
        lines.append("")

    elif structure == "para_then_bullets":
        para = generate_paragraph(random.randint(2, 4), use_opening=use_opening)
        lines.append(format_output(para, fmt))
        lines.append("")
        num_bullets = random.randint(3, 6)
        if fmt == "html":
            lines.append("<ul>")
        for i in range(num_bullets):
            item = generate_bullet_item()
            lines.append(format_list_item(item, fmt, numbered=False, index=i+1))
        if fmt == "html":
            lines.append("</ul>")
        lines.append("")

    elif structure == "para_then_numbered":
        para = generate_paragraph(random.randint(2, 4), use_opening=use_opening)
        lines.append(format_output(para, fmt))
        lines.append("")
        num_items = random.randint(3, 6)
        if fmt == "html":
            lines.append("<ol>")
        for i in range(num_items):
            item = generate_bullet_item()
            lines.append(format_list_item(item, fmt, numbered=True, index=i+1))
        if fmt == "html":
            lines.append("</ol>")
        lines.append("")

    elif structure == "subheadings":
        num_subs = random.randint(2, 4)
        for _ in range(num_subs):
            subheading = generate_heading()
            lines.append(format_output(subheading, fmt, is_heading=True, heading_level=3))
            lines.append("")
            para = generate_paragraph(random.randint(2, 4))
            lines.append(format_output(para, fmt))
            lines.append("")

    elif structure == "subheadings_mixed":
        # Intro paragraph
        para = generate_paragraph(random.randint(2, 3), use_opening=use_opening)
        lines.append(format_output(para, fmt))
        lines.append("")

        num_subs = random.randint(2, 3)
        for _ in range(num_subs):
            subheading = generate_heading()
            lines.append(format_output(subheading, fmt, is_heading=True, heading_level=3))
            lines.append("")

            # Random content under subheading
            if random.choice([True, False]):
                para = generate_paragraph(random.randint(2, 3))
                lines.append(format_output(para, fmt))
                lines.append("")
            else:
                num_bullets = random.randint(3, 5)
                if fmt == "html":
                    lines.append("<ul>")
                for i in range(num_bullets):
                    item = generate_bullet_item()
                    lines.append(format_list_item(item, fmt, numbered=False, index=i+1))
                if fmt == "html":
                    lines.append("</ul>")
                lines.append("")

    return lines


def main():
    parser = argparse.ArgumentParser(description="Generate lorem ipsum text")
    parser.add_argument("--paragraphs", type=int, default=3, help="Number of paragraphs")
    parser.add_argument("--sentences", type=int, default=5, help="Sentences per paragraph")
    parser.add_argument("--words", type=int, help="Approximate total word count")
    parser.add_argument("--characters", type=int, help="Exact character count (truncates to match)")
    parser.add_argument("--tokens", type=int, help="Estimated LLM token count (~4 chars/token)")
    parser.add_argument("--continuous", action="store_true", help="Continuous text without breaks")
    parser.add_argument("--headings", type=int, help="Number of sections with headings")
    parser.add_argument("--bullets", type=int, help="Bullet points per section")
    parser.add_argument("--numbered", action="store_true", help="Use numbered lists")
    parser.add_argument("--mixed", type=int, help="Generate realistic document with N sections")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--format", "-f", choices=["text", "markdown", "html"], default="markdown")

    args = parser.parse_args()

    # Convert tokens/characters to word count estimate for generation
    # Then we'll truncate to exact character count if needed
    target_chars = None
    if args.characters:
        target_chars = args.characters
        # Estimate words needed: avg ~8 chars per word (including space)
        args.words = (args.characters // 6) + 10  # Generate extra, then truncate
    elif args.tokens:
        target_chars = args.tokens * 4  # ~4 chars per token
        args.words = (target_chars // 6) + 10

    output_lines = []
    use_opening = True

    # Mixed document mode - realistic varied structure
    if args.mixed:
        for section_idx in range(args.mixed):
            heading = generate_heading()
            output_lines.append(format_output(heading, args.format, is_heading=True))
            output_lines.append("")
            section_lines = generate_mixed_section(args.format, use_opening=(section_idx == 0))
            output_lines.extend(section_lines)

    # Structured mode (headings with optional word count target)
    elif args.headings:
        num_headings = args.headings

        # Calculate content per section based on word count or defaults
        if args.words:
            words_per_section = args.words // num_headings
        else:
            words_per_section = None

        for section_idx in range(num_headings):
            heading = generate_heading()
            output_lines.append(format_output(heading, args.format, is_heading=True))
            output_lines.append("")

            if args.bullets:
                # Bullet list mode
                if args.format == "html":
                    tag = "ol" if args.numbered else "ul"
                    output_lines.append(f"<{tag}>")

                num_bullets = args.bullets
                if words_per_section:
                    # Estimate bullets needed for word count
                    words_per_bullet = 7  # average
                    num_bullets = max(args.bullets, words_per_section // words_per_bullet)

                section_words = 0
                for i in range(num_bullets):
                    if words_per_section and section_words >= words_per_section:
                        break
                    item = generate_bullet_item()
                    section_words += len(item.split())
                    output_lines.append(format_list_item(item, args.format, args.numbered, i + 1))

                if args.format == "html":
                    output_lines.append(f"</{tag}>")
                output_lines.append("")
            else:
                # Paragraph mode under headings
                if words_per_section:
                    # Generate paragraphs until word count reached
                    section_words = 0
                    while section_words < words_per_section:
                        para = generate_paragraph(args.sentences, use_opening=use_opening)
                        use_opening = False
                        section_words += len(para.split())
                        output_lines.append(format_output(para, args.format))
                        output_lines.append("")
                else:
                    # Use paragraph count
                    paragraphs_per_section = max(1, args.paragraphs // num_headings)
                    for _ in range(paragraphs_per_section):
                        para = generate_paragraph(args.sentences, use_opening=use_opening)
                        use_opening = False
                        output_lines.append(format_output(para, args.format))
                        output_lines.append("")

    # Plain word count mode (no structure)
    elif args.words:
        words_generated = 0
        paragraphs = []
        while words_generated < args.words:
            para = generate_paragraph(args.sentences, use_opening=use_opening)
            use_opening = False
            paragraphs.append(para)
            words_generated += len(para.split())

        if args.continuous:
            output_lines.append(" ".join(paragraphs))
        else:
            for para in paragraphs:
                output_lines.append(format_output(para, args.format))
                if args.format != "html":
                    output_lines.append("")

    # Standard paragraph mode
    else:
        paragraphs = []
        for _ in range(args.paragraphs):
            para = generate_paragraph(args.sentences, use_opening=use_opening)
            use_opening = False
            paragraphs.append(para)

        if args.continuous:
            output_lines.append(" ".join(paragraphs))
        else:
            for para in paragraphs:
                output_lines.append(format_output(para, args.format))
                if args.format != "html":
                    output_lines.append("")

    # Join and output
    result = "\n".join(output_lines).strip()

    # Truncate to exact character count if specified
    if target_chars and len(result) > target_chars:
        result = result[:target_chars].rstrip()

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
