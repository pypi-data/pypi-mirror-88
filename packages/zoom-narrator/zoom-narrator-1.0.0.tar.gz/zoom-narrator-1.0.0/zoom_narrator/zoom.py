import json
import os
from contextlib import asynccontextmanager

from aiohttp import ClientSession

RESUME_FILE = ".resumesession"


@asynccontextmanager
async def open_zoom_session(api_key):
    async with ClientSession() as http_session:
        session = ZoomSession(http_session, api_key)
        try:
            yield session
        finally:
            session.close()


class ZoomSession:
    def __init__(self, http_session, api_key, seq_start=0):
        self.http_session = http_session
        self.api_key = api_key

        # The closed captioning API is very minimalistic, and one limitation that creates is the inability to reset the sequence
        # number. Hence if more than one connection is going to be made to a given meeting over its lifetime, we need to
        # remember where we left off or it will get unhappy with our "out-of-order" data and delay new lines until some timeout
        # expires.
        self._seq = self._load_resume_seq()

    @property
    def seq(self):
        current = self._seq
        self._seq += 1
        return current

    async def send_caption(self, caption: str):
        await self.http_session.post(
            self.api_key,
            params={"seq": self.seq, "lang": "en-US"},
            data=caption,
        )

        print(caption)

    def _load_resume_seq(self):
        resume_seq = 0
        if os.path.exists(RESUME_FILE):
            with open(RESUME_FILE) as resume_file:
                saved = json.load(resume_file)
                assert "seq", "api_key" in saved.keys()
                if saved["api_key"] == self.api_key:
                    resume_seq = saved["seq"]

        return resume_seq

    def _save_resume_seq(self):
        with open(RESUME_FILE, "w") as resume_file:
            json.dump({"api_key": self.api_key, "seq": self._seq}, resume_file)

    def close(self):
        self._save_resume_seq()
