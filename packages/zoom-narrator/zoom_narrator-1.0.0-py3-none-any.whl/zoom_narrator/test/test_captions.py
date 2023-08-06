from unittest import IsolatedAsyncioTestCase, mock
from .. import captions
from datetime import timedelta
import freezegun


class TestCaptions(IsolatedAsyncioTestCase):
    def assert_is_arthur(self, captionfile):
        self.assertIsNotNone(captionfile)
        self.assertEqual(
            captionfile.events[0].text,
            "Arthur the Rat, read by Brian Goggin from Ireland.",
        )

    def test_autoload(self):
        captionfile = captions.load(
            None, "zoom_narrator/test/fixtures/arthur the rat.mp3"
        )

        self.assert_is_arthur(captionfile)

    def test_manual_load(self):
        captionfile = captions.load(
            "zoom_narrator/test/fixtures/arthur the rat.vtt", "some/nonsense"
        )

        self.assert_is_arthur(captionfile)

    def test_dump(self):
        captionfile = captions.load(
            None, "zoom_narrator/test/fixtures/arthur the rat.mp3"
        )

        self.assertIn(
            "0.005: Arthur the Rat, read by Brian Goggin from Ireland.",
            captions.dump_captions(captionfile),
        )

    async def test_timed_captions(self):
        with freezegun.freeze_time() as frozen_time:
            with mock.patch(
                "asyncio.sleep",
                side_effect=lambda x: frozen_time.tick(timedelta(seconds=x)),
            ) as aisleep:
                captionfile = captions.load(
                    "zoom_narrator/test/fixtures/very_simple_subs.srt", "some/nonsense"
                )

                caption_list = [
                    caption.plaintext
                    async for caption in captions.timed_captions(captionfile)
                ]

                self.assertEqual(
                    ["First Subtitle", "Second Subtitle", "Third Subtitle"],
                    caption_list,
                )

                aisleep.assert_has_awaits(
                    [mock.call(0), mock.call(10.001), mock.call(10)]
                )
