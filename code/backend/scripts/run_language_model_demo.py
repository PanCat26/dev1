import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from language_model.client import generate


async def test_streaming(prompt: str):
    messages = [
        {"role": "system", "content": "You are a helpful coding assistant. Be concise."},
        {"role": "user", "content": prompt},
    ]

    print(f"Prompt: {prompt}")
    print("Response: ", end="", flush=True)

    async for token in generate(messages, max_tokens=256):
        print(token, end="", flush=True)

    print("\n\nDone.")


def main():
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Write a Python function that reverses a string."
    asyncio.run(test_streaming(prompt))


if __name__ == "__main__":
    main()
