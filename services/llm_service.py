import os
from dotenv import load_dotenv
from openai import OpenAI


class LlmService:
    _client = None

    def __init__(self):
        load_dotenv()

        self.url = os.getenv("OPENAI_URL")

        if not self.url:
            raise ValueError("Unable to load api")

        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("Unable to load api key")

        if LlmService._client is None:
            LlmService._client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    @staticmethod
    def get_topic_paragraph(topic):

        response = LlmService._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are an elementary school teacher writing educational content for 4th grade students (ages 9-10). Write a clear, engaging paragraph about the given topic using:

                    - Simple vocabulary appropriate for 4th grade reading level
                    - Short to medium sentences (8-15 words each)
                    - 3-4 sentences total
                    - Present factual, age-appropriate information
                    - Use an encouraging, friendly tone
                    - Avoid complex concepts, scary topics, or inappropriate content
                    - Make it interesting and educational
                    
                    Keep the paragraph between 50-80 words."""},
                {"role": "user", "content": f"Write a paragraph about {topic}"}
            ],
            max_tokens=150,
            temperature=0.5
        )

        paragraph = response.choices[0].message.content
        return paragraph

    @staticmethod
    def get_topic_sentences(topic):
        response = LlmService._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are an elementary school teacher creating a grammar exercise for 4th grade students. Take the given topic and write 2-3 simple sentences about it, but include 3-7 obvious grammar mistakes that 4th graders can identify and correct.

                    Include mistakes like:
                    - Missing capitalization at sentence start
                    - Missing periods
                    - Simple subject-verb agreement errors
                    - Basic punctuation mistakes
                    
                    Make the content educational and age-appropriate. The mistakes should be clear and not confusing."""},
                {"role": "user", "content": f"Create sentences with grammar mistakes about: {topic}"}
            ],
            max_tokens=150,
            temperature=0.5
        )

        sentences = response.choices[0].message.content
        return sentences
