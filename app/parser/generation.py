import json
import os, sys
import openai

from dotenv import load_dotenv
from app.parser.prompts import BATCH_PERSONAL_SUMMARY_PROMPT, OVERALL_PERSONAL_SUMMARY_PROMPT

load_dotenv()

client = openai.OpenAI()


def generate_batches_summary(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": BATCH_PERSONAL_SUMMARY_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0.0,
        max_tokens=2048,
    )

    answer = response.choices[0].message.content
    return answer

def generate_overall_summary(text,person):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": OVERALL_PERSONAL_SUMMARY_PROMPT.format(person=person)},
            {"role": "user", "content": text}
        ],
        temperature=0.0,
        max_tokens=4096,
    )

    answer = response.choices[0].message.content
    return answer

