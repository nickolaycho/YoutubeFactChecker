from app.core.transcriptor import Transcriptor

class TestFactCheck():
    def test_video_id(self):
        t = Transcriptor(video_url="https://youtu.be/abc123")
        assert t.video_id == "abc123"

        t = Transcriptor(video_url="https://www.youtube.com/watch?v=JV3pL1_mn2M&t=2s")
        assert t.video_id == "JV3pL1_mn2M"

    def test_transcript_gets_text(self):
        t = Transcriptor(video_url="https://www.youtube.com/watch?v=REL_SEaGTPQ")
        transcript = t.transcript
        assert " " in transcript
        assert len(transcript.split()) > 50