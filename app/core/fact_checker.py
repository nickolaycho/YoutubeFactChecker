from youtube_transcript_api import YouTubeTranscriptApi
from app.core.llm_analyzer import LLMAnalyzer
from app.core.transcriptor import Transcriptor
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from app.core.structured_output import AnalyzeResponse

class FactChecker:
    def __init__(self,
            video_url: str,
            transcriptor: Transcriptor=Transcriptor,
            llm_analyzer: LLMAnalyzer=LLMAnalyzer) -> None:
        self.video_url:str = video_url
        self.transcriptor: Transcriptor = transcriptor
        self.llm_analyzer: LLMAnalyzer = llm_analyzer

    @property
    def result(self) -> AnalyzeResponse:
        transcriptor: Transcriptor = self.transcriptor(
            video_url=self.video_url,
        )
        transcript: str = transcriptor.transcript
        capped_transcript: str = self.cap(transcript, 30000)
        llm_analyzer: LLMAnalyzer = self.llm_analyzer(
            transcript=capped_transcript,
            schema=AnalyzeResponse
        )
        result: AnalyzeResponse = llm_analyzer.analyze_transcript
        return result

    def cap(self, text: str, cap: int) -> str:
        return text[:cap]

    




