from collections.abc import Callable

from youtube_transcript_api import YouTubeTranscriptApi
from app.core.llm_analyzer import LLMAnalyzer
from app.core.transcriptor import Transcriptor
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from app.core.structured_output import AnalyzeResponse

class FactChecker:
    def __init__(self,
            video_url: str,
            transcriptor: Transcriptor | Callable[[str], Transcriptor] | None = None,
            llm_analyzer: LLMAnalyzer | Callable[[str, type[AnalyzeResponse]], LLMAnalyzer] | None = None) -> None:
        self.video_url:str = video_url
        if transcriptor is None:
            self.transcriptor: Transcriptor = Transcriptor(video_url=self.video_url)
        elif callable(transcriptor):
            self.transcriptor = transcriptor(self.video_url)
        else:
            self.transcriptor = transcriptor

        if llm_analyzer is None:
            self.llm_analyzer_factory: Callable[[str, type[AnalyzeResponse]], LLMAnalyzer] = (
                lambda transcript, schema: LLMAnalyzer(transcript=transcript, schema=schema)
            )
            self.llm_analyzer: LLMAnalyzer | None = None
        elif callable(llm_analyzer):
            self.llm_analyzer_factory = llm_analyzer
            self.llm_analyzer = None
        else:
            self.llm_analyzer_factory = lambda transcript, schema: llm_analyzer
            self.llm_analyzer = llm_analyzer

    @property
    def result(self) -> AnalyzeResponse:
        transcript: str = self.transcriptor.transcript
        capped_transcript: str = self.cap(transcript, 30000)
        llm_analyzer: LLMAnalyzer = self.llm_analyzer or self.llm_analyzer_factory(
            capped_transcript,
            AnalyzeResponse,
        )
        result: AnalyzeResponse = llm_analyzer.analyze_transcript
        return result

    @staticmethod
    def cap(text: str, cap: int) -> str:
        return text[:cap]

    



