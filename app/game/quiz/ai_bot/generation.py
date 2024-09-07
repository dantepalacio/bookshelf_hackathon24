import json
import os, sys
import openai

from dotenv import load_dotenv
from .prompts import GENERATE_QUESTIONS_PROMPT, COMPARE_ANSWERS_PROMPT

load_dotenv()

client = openai.OpenAI()


def generate_questions(context):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": GENERATE_QUESTIONS_PROMPT},
            {"role": "user", "content": f'Заданный контекст: \n{context}'}
        ],
        temperature=0.8,
        max_tokens=2048,
    )

    answer = response.choices[0].message.content
    return answer

def compare_answers(source_answer, user_answer):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": COMPARE_ANSWERS_PROMPT},
            {"role": "user", "content": f'Исходные ответы: {source_answer} \n Ответы пользователя: {user_answer}'}
        ],
        temperature=0.0,
        max_tokens=2048,
    )

    answer = response.choices[0].message.content
    return answer