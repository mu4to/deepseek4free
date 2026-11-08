#!/bin/bash
cd "$(dirname "$0")"
if [ ! -f .env ]; then
  echo "Create .env from .env.example and set DEEPSEEK_AUTH_TOKEN"
  exit 1
fi
python openai_server.py
