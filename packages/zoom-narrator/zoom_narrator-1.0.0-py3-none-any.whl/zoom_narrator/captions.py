import asyncio
import os
from datetime import datetime, timedelta
from functools import partial
from typing import Optional, AsyncGenerator

import pysubs2

CAPTIONS_EXTENSIONS = ["ssa", "ass", "tmp", "vtt", "srt"]


def _probe(audio_path: str) -> Optional[str]:
    audio_name = _root_name(audio_path)
    audio_dir = os.path.dirname(audio_path)

    for file in os.listdir(audio_dir):
        if (
            _root_name(file) == audio_name
            and _last_extension(file) in CAPTIONS_EXTENSIONS
        ):
            return os.path.join(audio_dir, file)

    return None


def load(caption_path: Optional[str], audio_path: str) -> pysubs2.SSAFile:
    if not caption_path:
        caption_path = _probe(audio_path)
    if not caption_path:
        raise ValueError("Couldn't find caption file, please specify manually.")

    return pysubs2.load(caption_path)


def dump_captions(captions: pysubs2.SSAFile) -> str:
    return "\n".join(
        [f"{event.start/1000:05}: {event.text}" for event in captions.events]
    )


async def timed_captions(
    captions: pysubs2.SSAFile,
) -> AsyncGenerator[pysubs2.SSAEvent, None]:
    wait_until_event_time = partial(_wait_until_reltime, datetime.now())

    for event in captions:
        await wait_until_event_time(event.start)
        yield event


async def _wait_until_reltime(base_time: datetime, reltime_ms: int) -> None:
    abs_time = base_time + timedelta(milliseconds=reltime_ms)
    time_until = abs_time - datetime.now()

    # If the system ever gets delayed and time_until winds up being less than zero, events will just start triggering
    # as soon as they're queued until things get caught up.
    await asyncio.sleep(time_until.total_seconds())


def _root_name(path):
    return os.path.basename(path).split(".")[0]


def _last_extension(path):
    return os.path.basename(path).split(".")[-1]
