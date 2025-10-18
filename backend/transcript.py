from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript_from_id(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    subtitle = " ".join(chunk['text'] for chunk in transcript)
    return subtitle