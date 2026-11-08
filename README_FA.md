# راهنمای فارسی – deepseek4free برای DeepSeek Harness

## نصب

```bash
pip install -r requirements.txt
cp .env.example .env
# توکن را داخل .env بگذار
python openai_server.py
```

## گرفتن توکن

1. برو به https://chat.deepseek.com و لاگین کن
2. F12 → Application → Local Storage → userToken → value را کپی کن

## تنظیم در Harness

- Base URL: `http://127.0.0.1:8000/v1`
- Model: `deepseek-chat` یا `deepseek-reasoner`
- API Key: هر چیزی (مثلاً `dummy`)

سرور باید روشن بماند.
