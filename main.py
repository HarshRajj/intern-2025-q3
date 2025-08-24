import os
import backoff
from google import generativeai as genai
import structlog
from dotenv import load_dotenv

# 1. Configure structlog for clear, structured logging
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)
log = structlog.get_logger()

GEMINI_MODEL = 'gemini-1.5-flash'
TWEET_SAMPLES = [
    {"topic": "the future of renewable energy", "tone": "optimistic", "max_words": 30},
    {"topic": "tips for effective remote work", "tone": "professional", "max_words": 25},
    {"topic": "the joy of discovering new music", "tone": "enthusiastic", "max_words": 35},
]

# 2. Add the backoff decorator to the function
# This will retry the function on any Exception (including possible 5xx errors)
@backoff.on_exception(
    backoff.expo,
    Exception,
    max_time=60
)
def generate_tweet(topic: str, tone: str, max_words: int) -> None:
    log.info(
        "Generating tweet: request sent", 
        topic=topic, 
        tone=tone, 
        max_words=max_words
    )
    
    try:
        prompt = (
            f"Generate a tweet about the following topic: '{topic}'. "
            f"The tone of the tweet should be {tone}. "
            f"Please ensure the tweet is under {max_words} words. "
            f"Do not include any hashtags or URLs."
        )

        model = genai.GenerativeModel(GEMINI_MODEL)
        generation_config = {"temperature": 0.8}
        response = model.generate_content(prompt, generation_config=generation_config)

        log.info(
            "Generating tweet: response received",
            topic=topic,
            response_text=response.text.strip()
        )

        print("--- Sample Tweet ---")
        print(f"Topic: {topic}, Tone: {tone}, Max Words: {max_words}")
        print(f"Tweet: {response.text.strip()}")
        print("-" * 20 + "\n")

    except Exception as e:
        # Optionally, check for 5xx error in e or its message if the API exposes it
        log.error(
            "An error occurred while generating tweet",
            topic=topic,
            error=str(e)
        )
        # Re-raise the exception to allow backoff to catch it
        raise e

def main() -> None:
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        log.error("GOOGLE_API_KEY was not found. Please check your .env file.")
        return

    genai.configure(api_key=api_key)

    for sample in TWEET_SAMPLES:
        try:
            generate_tweet(
                topic=sample["topic"], 
                tone=sample["tone"], 
                max_words=sample["max_words"]
            )
        except Exception as e:
            log.error("Failed to generate tweet after multiple retries", sample=sample)


if __name__ == "__main__":
    main()