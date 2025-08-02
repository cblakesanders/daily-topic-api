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
    def get_grammar_exercise_with_answers(topic):
        response = LlmService._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are an elementary school teacher creating a grammar exercise for 4th grade students. Take the given topic and create 2-3 simple sentences about it with intentional grammar mistakes, plus their corrected versions.

                    Requirements:
                    - Write 2-3 sentences with obvious grammar mistakes that 4th graders can identify
                    - Include mistakes like: missing capitalization, missing periods, subject-verb agreement errors, basic punctuation mistakes
                    - Make content educational and age-appropriate
                    - Return the response in this exact format:
                    
                    EXERCISE:
                    [sentences with mistakes as a single paragraph]
                    
                    ANSWERS:
                    [corrected sentences, one per line]
                    
                    Example:
                    EXERCISE:
                    the sun is hot plants need water birds can fly
                    
                    ANSWERS:
                    The sun is hot.
                    Plants need water.
                    Birds can fly."""},
                {"role": "user", "content": f"Create a grammar exercise with answers about: {topic}"}
            ],
            max_tokens=200,
            temperature=0.5
        )

        response_text = response.choices[0].message.content.strip()
        
        # Parse the response to extract exercise and answers
        parts = response_text.split('ANSWERS:')
        if len(parts) != 2:
            # Fallback if parsing fails
            return "Error generating grammar exercise", []
        
        exercise_part = parts[0].replace('EXERCISE:', '').strip()
        answers_part = parts[1].strip()
        
        # Split answers into array
        answers = [answer.strip() for answer in answers_part.split('\n') if answer.strip()]
        
        return exercise_part, answers
