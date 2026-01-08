from urllib.parse import urlparse, parse_qs, ParseResult
from youtube_transcript_api import YouTubeTranscriptApi
from functools import cached_property
from app.core.llm import analyze_transcript
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

class FactChecker():
    def __init__(self, video_url: str):
        self.video_url:str = video_url

    @property
    def result(self):
        # hard cap per evitare prompt enormi
        transcript = self.transcript[: 30000]
        return analyze_transcript(transcript)
    
    @property
    def transcript(self) -> str:
        try:
            fetched = YouTubeTranscriptApi().fetch(
                video_id=self.video_id,
                languages=("it", "en"),
                preserve_formatting=False,
            )
            return "\n".join(snippet.text for snippet in fetched)
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            raise ValueError(f"Transcript not available for this video: {e}")
    
    @property
    def video_id(self) -> str:
        u: ParseResult = urlparse(self.video_url)
        if u.hostname in ("youtu.be",):
            vid = u.path.lstrip("/")
            if vid:
                return vid
        if u.hostname and "youtube.com" in u.hostname:
            qs = parse_qs(u.query)
            if "v" in qs and qs["v"]:
                return qs["v"][0]
        raise ValueError("Invalid YouTube URL")
