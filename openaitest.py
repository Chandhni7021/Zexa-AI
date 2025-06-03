import openai
from config import apikey

openai.api_key = apikey

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",  # or "gpt-4" or "gpt-3.5-turbo"
    messages=[
        {"role": "user", "content": "Write an email to my boss for resignation?"}
    ]
)

print(response.choices[0].message.content)
