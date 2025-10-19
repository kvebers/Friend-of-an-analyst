from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled, VideoUnavailable
import time

def get_transcript_from_id(video_id):
    """
    Getting Rate Blocked hahaha
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, 
            languages=['en', 'en-US', 'en-GB']
        )
        print(transcript)
        return " ".join([entry["text"] for entry in transcript])
    except NoTranscriptFound:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            for transcript in transcript_list:
                data = transcript.fetch()
                print(f"Found transcript in language: {transcript.language_code}")
                return " ".join([entry["text"] for entry in data])
        except Exception as e:
            return ""
    
    except TranscriptsDisabled:
        return ""
    except VideoUnavailable:
        return ""
    except Exception as e:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return " ".join([entry["text"] for entry in transcript])
        except:
            return ""
        

if __name__ == "__main__":
    get_transcript_from_id("ANB-Drr1rD4")