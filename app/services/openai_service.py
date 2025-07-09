from openai import OpenAI
from app.core.config import settings
client = OpenAI(
  api_key=settings.OPENAI_API_KEY
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);