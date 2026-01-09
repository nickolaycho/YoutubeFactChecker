from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from functools import cached_property
from urllib.parse import urlparse, parse_qs, ParseResult

class Transcriptor:
    def __init__(self, video_url: str) -> None:
        self.video_url = video_url
        self.parsed_url: ParseResult = urlparse(self.video_url)

    @cached_property
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
    
    @cached_property
    def video_id(self) -> str:
        video_id = self.video_id_from_short_url(self.parsed_url)
        if video_id:
            return video_id

        video_id = self.video_id_from_standard_url(self.parsed_url)
        if video_id:
            return video_id

        raise ValueError(f"Invalid YouTube URL: {self.video_url}")
    
    def video_id_from_short_url(self,
        parsed_url: ParseResult) -> str:
        if parsed_url.hostname != "youtu.be":
            return None
        return parsed_url.path.lstrip("/") or ""
    
    def video_id_from_standard_url(self,
        parsed_url: ParseResult) -> str:
        if not parsed_url.hostname or "youtube.com" not in parsed_url.hostname:
            return ""

        query_params: dict = parse_qs(parsed_url.query)
        video_ids = query_params.get("v")

        if not video_ids:
            return ""

        return video_ids[0]