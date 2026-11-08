#!/usr/bin/env python3
"""Interactive CLI chat using deepseek4free."""

import os
import sys
from dotenv import load_dotenv
from dsk.api import DeepSeekAPI

load_dotenv()

TOKEN = os.getenv("DEEPSEEK_AUTH_TOKEN", "").strip()
if not TOKEN:
    print("ERROR: Set DEEPSEEK_AUTH_TOKEN in .env")
    sys.exit(1)

def main():
    api = DeepSeekAPI(TOKEN)
    print("DeepSeek Chat (type 'exit' or Ctrl+C to quit)")
    print("-" * 40)

    while True:
        try:
            prompt = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not prompt or prompt.lower() in ("exit", "quit", "q"):
            print("Bye!")
            break

        try:
            chat_id = api.create_chat_session()
            print("Assistant: ", end="", flush=True)
            for chunk in api.chat_completion(chat_id, prompt, thinking_enabled=False):
                if chunk.get("type") == "text" and chunk.get("content"):
                    print(chunk["content"], end="", flush=True)
            print()
        except Exception as e:
            print(f"\n[Error] {e}")

if __name__ == "__main__":
    main()
