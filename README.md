# deepseek4free + OpenAI Proxy for DeepSeek Harness

Unofficial reverse-engineered client for DeepSeek's **free web chat API**, plus an OpenAI-compatible server so you can use it inside **DeepSeek Harness** (and other OpenAI-compatible tools).

> ⚠️ This is **not** the official DeepSeek API. It uses the same backend as [chat.deepseek.com](https://chat.deepseek.com). Use at your own risk. Tokens can expire, rate limits apply, and Cloudflare may block requests.

---

## Features

- Free access to DeepSeek chat (no paid API key required)
- OpenAI-compatible `/v1/chat/completions` + `/v1/models`
- Works with **DeepSeek Harness** Custom Provider
- Streaming support
- Thinking / reasoner mode (`deepseek-reasoner`)
- Simple interactive CLI (`chat.py`)

---

## Quick Start

### 1. Clone & install

```bash
git clone https://github.com/YOUR_USERNAME/deepseek4free.git
cd deepseek4free
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Get your auth token

1. Open [chat.deepseek.com](https://chat.deepseek.com) and log in
2. Press `F12` → **Application** → **Local Storage** → `https://chat.deepseek.com`
3. Copy the `value` of `userToken`

Or in the browser console:

```js
JSON.parse(localStorage.getItem("userToken")).value
```

### 3. Configure

```bash
cp .env.example .env
# Edit .env and paste your token
```

### 4. Run the OpenAI server

```bash
python openai_server.py
```

Server starts at: `http://127.0.0.1:8000/v1`

---

## Use with DeepSeek Harness

1. Start the server (`python openai_server.py`)
2. In Harness go to **Settings → Models → Add model provider**
3. Choose **Custom model API**
4. Fill in:

| Field            | Value                          |
|------------------|--------------------------------|
| Provider ID      | `deepseek4free`                |
| Display name     | DeepSeek Free                  |
| Base URL         | `http://127.0.0.1:8000/v1`     |
| API protocol     | OpenAI Chat Completions        |
| API Key          | `dummy` (any string)           |
| Model            | `deepseek-chat` or `deepseek-reasoner` |

5. Save and select the model.

> Tip: Start a **new session** in Harness after changing the provider to avoid old history issues.

---

## Interactive CLI

```bash
python chat.py
```

---

## API Endpoints

| Method | Path                     | Description                |
|--------|--------------------------|----------------------------|
| GET    | `/v1/models`             | List available models      |
| POST   | `/v1/chat/completions`   | Chat (stream & non-stream) |
| GET    | `/health`                | Health check               |

### Example

```bash
curl http://127.0.0.1:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "Hello"}],
    "stream": false
  }'
```

---

## Notes & Limitations

- Token can expire — re-extract from the website when needed
- Rate limits exist on the free web backend
- Cloudflare may occasionally block requests (see original project for bypass tools)
- Conversation history from Harness is **not** fully forwarded; only the last user message is used (by design, for simplicity and to avoid null-content errors)
- This project is for educational / personal use

---

## Project structure

```
deepseek4free/
├── dsk/                  # Core library (API client, PoW, etc.)
│   ├── api.py
│   ├── pow.py
│   ├── wasm/
│   └── ...
├── openai_server.py      # OpenAI-compatible proxy (for Harness)
├── chat.py               # Simple CLI chat
├── example.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Original project
  
This fork/package adds a stable OpenAI proxy, fixes for newer Python versions, and Harness-friendly request handling.

---

## License

See [LICENSE](LICENSE). Use responsibly.
