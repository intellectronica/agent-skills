#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["youtube-transcript-api>=1.0.0"]
# ///
"""
Extract transcript from a YouTube video.

Usage:
    uv run scripts/get_transcript.py <video_id_or_url> [--timestamps] [--title-only]
"""

import sys
import re
import json
import argparse
import urllib.parse
import urllib.request
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from various YouTube URL formats or return as-is if already an ID."""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url_or_id}")


def get_title(video_id: str) -> str:
    """Fetch the video title via YouTube's oEmbed API (no auth required)."""
    video_url = urllib.parse.quote(f"https://www.youtube.com/watch?v={video_id}")
    oembed_url = f"https://www.youtube.com/oembed?url={video_url}&format=json"
    try:
        with urllib.request.urlopen(oembed_url, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("title", "").strip()
    except Exception:
        return ""


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS or MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def get_transcript(video_id: str, with_timestamps: bool = False) -> str:
    """Fetch and format transcript for a YouTube video."""
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id)

    if with_timestamps:
        lines = [f"[{format_timestamp(snippet.start)}] {snippet.text}" for snippet in transcript.snippets]
    else:
        lines = [snippet.text for snippet in transcript.snippets]

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Get YouTube video transcript')
    parser.add_argument('video', help='YouTube video URL or video ID')
    parser.add_argument('--timestamps', '-t', action='store_true',
                        help='Include timestamps in output')
    parser.add_argument('--title-only', action='store_true',
                        help='Print only the video title and exit')
    args = parser.parse_args()

    try:
        video_id = extract_video_id(args.video)
        if args.title_only:
            print(get_title(video_id))
            return
        transcript = get_transcript(video_id, with_timestamps=args.timestamps)
        print(transcript)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
