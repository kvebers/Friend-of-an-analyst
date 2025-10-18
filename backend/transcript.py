from youtube_transcript_api import YouTubeTranscriptApi

test_id = "CYlon2tvywA"

def get_tranctipt_from_id(video_id):
    yt_transcript_api = YouTubeTranscriptApi()
    transcript = yt_transcript_api.fetch(video_id)
    get_combined_text = ""
    for element in transcript:
        get_combined_text += element.text
    print(get_combined_text)

get_tranctipt_from_id(test_id)
