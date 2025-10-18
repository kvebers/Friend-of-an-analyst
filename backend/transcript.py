from youtube_transcript_api import YouTubeTranscriptApi

def get_tranctipt_from_id(video_id):
    yt_transcript_api = YouTubeTranscriptApi()
    transcript = yt_transcript_api.fetch(video_id)
    subtitle = ""
    for chunk in transcript:
        subtitle += chunk.text
    return subtitle