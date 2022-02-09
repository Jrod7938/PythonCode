import os
import openai

openai.api_key = "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"

while True:
  question = input("How can i help you: ")
  response = openai.Completion.create(
    engine="text-davinci-001",
    prompt=f"{question}",
    temperature=0.7,
    max_tokens=64,
    top_p=1,
    frequency_penalty=0.2,
    presence_penalty=0.2
  )
  print(f"Answer: {response['choices'][0]['text']}")