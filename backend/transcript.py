from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled, VideoUnavailable
import time

def get_transcript_from_id(video_id): 
    """ 
    Getting Rate Blocked hahaha 
    """ 
    ytt_api = YouTubeTranscriptApi() 
    content = ytt_api.fetch(video_id) 
    transcript_text = ' '.join([segment.text for segment in content])
    return transcript_text

        
if __name__ == "__main__":
    get_transcript_from_id("ANB-Drr1rD4")