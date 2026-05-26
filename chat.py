from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    }
]

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chat ended.")
        break

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama-3.1-8b-instant",
        temperature=0.7,
        max_tokens=200
    )

    reply = chat_completion.choices[0].message.content

    print("AI:", reply)

    messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )