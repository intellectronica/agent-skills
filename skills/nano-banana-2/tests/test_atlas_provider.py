import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

from PIL import Image

SCRIPT = Path(__file__).parents[1] / "scripts" / "generate_image.py"
SPEC = importlib.util.spec_from_file_location("nano_banana_generate", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def png_bytes() -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (2, 2), "blue").save(buffer, format="PNG")
    return buffer.getvalue()


class FakeResponse:
    def __init__(
        self,
        *,
        payload=None,
        content=b"",
        url="https://static.atlascloud.ai/output.png",
    ):
        self.payload = payload
        self.content = content
        self.url = url

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self, posts, gets):
        self.posts = list(posts)
        self.gets = list(gets)
        self.post_calls = []
        self.get_calls = []

    def post(self, url, **kwargs):
        self.post_calls.append((url, kwargs))
        return self.posts.pop(0)

    def get(self, url, **kwargs):
        self.get_calls.append((url, kwargs))
        return self.gets.pop(0)


class AtlasProviderTests(unittest.TestCase):
    def test_text_generation_submits_once_and_polls_with_bounded_gets(self):
        session = FakeSession(
            posts=[
                FakeResponse(
                    payload={"code": 200, "data": {"id": "pred_1", "status": "created"}}
                )
            ],
            gets=[
                FakeResponse(
                    payload={
                        "code": 200,
                        "data": {"id": "pred_1", "status": "processing"},
                    }
                ),
                FakeResponse(
                    payload={
                        "code": 200,
                        "data": {
                            "id": "pred_1",
                            "status": "completed",
                            "outputs": ["https://static.atlascloud.ai/output.png"],
                        },
                    }
                ),
                FakeResponse(content=png_bytes()),
            ],
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "result.png"
            saved = MODULE.generate_with_atlas(
                session,
                api_key="test-key",
                prompt="a blue square",
                output_path=output,
                input_paths=[],
                resolution="1K",
                aspect_ratio="1:1",
                pil_image=Image,
                sleep=lambda _delay: None,
            )
            self.assertEqual(saved, [output.resolve()])
            self.assertTrue(output.exists())

        self.assertEqual(len(session.post_calls), 1)
        payload = session.post_calls[0][1]["json"]
        self.assertEqual(payload["model"], MODULE.ATLAS_TEXT_MODEL)
        self.assertEqual(payload["resolution"], "1k")
        self.assertEqual(len(session.get_calls), 3)

    def test_edit_uploads_reference_then_submits_edit_model(self):
        upload_url = "https://atlas-img.oss-accelerate-overseas.aliyuncs.com/input.png"
        output_url = "https://static.atlascloud.ai/output.png"
        session = FakeSession(
            posts=[
                FakeResponse(
                    payload={"code": 200, "data": {"download_url": upload_url}}
                ),
                FakeResponse(
                    payload={
                        "code": 200,
                        "data": {
                            "id": "pred_2",
                            "status": "completed",
                            "outputs": [output_url],
                        },
                    }
                ),
            ],
            gets=[FakeResponse(content=png_bytes())],
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            reference = Path(temp_dir) / "reference.png"
            Image.new("RGB", (2, 2), "red").save(reference)
            output = Path(temp_dir) / "edited.png"
            MODULE.generate_with_atlas(
                session,
                api_key="test-key",
                prompt="make it blue",
                output_path=output,
                input_paths=[reference],
                resolution="2K",
                aspect_ratio="16:9",
                pil_image=Image,
                sleep=lambda _delay: None,
            )
            self.assertTrue(output.exists())

        self.assertEqual(len(session.post_calls), 2)
        payload = session.post_calls[1][1]["json"]
        self.assertEqual(payload["model"], MODULE.ATLAS_EDIT_MODEL)
        self.assertEqual(payload["images"], [upload_url])

    def test_immediate_failure_is_reported_without_polling(self):
        for payload in (
            {"data": {"status": "failed", "error": "bad prompt"}},
            {"data": {"id": "abc123", "status": "failed", "error": "bad prompt"}},
        ):
            session = FakeSession(posts=[FakeResponse(payload=payload)], gets=[])
            with (
                tempfile.TemporaryDirectory() as tmp,
                self.assertRaisesRegex(RuntimeError, "generation failed: bad prompt"),
            ):
                MODULE.generate_with_atlas(
                    session,
                    api_key="test-key",
                    prompt="x",
                    output_path=Path(tmp) / "out.png",
                    input_paths=[],
                    resolution="1K",
                    aspect_ratio=None,
                    pil_image=Image,
                    sleep=lambda _: None,
                )
            self.assertEqual(session.get_calls, [])

    def test_untrusted_output_url_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "untrusted Atlas media URL"):
            MODULE._validate_atlas_media_url("http://127.0.0.1/private.png")


if __name__ == "__main__":
    unittest.main()
