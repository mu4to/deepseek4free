deepseek4free + پراکسی OpenAI برای DeepSeek Harness

یک کلاینت غیررسمی و مهندسی معکوس‌شده برای استفاده از API رایگان چت تحت وب DeepSeek، به همراه یک سرور سازگار با OpenAI که امکان استفاده از آن را در DeepSeek Harness و سایر ابزارهای سازگار با OpenAI فراهم می‌کند.

⚠️ توجه: این پروژه API رسمی DeepSeek نیست. این ابزار از همان بک‌اندی استفاده می‌کند که وب‌سایت chat.deepseek.com از آن استفاده می‌کند. استفاده از آن با مسئولیت خودتان است. توکن‌های احراز هویت ممکن است منقضی شوند، محدودیت نرخ درخواست وجود دارد و Cloudflare ممکن است درخواست‌ها را مسدود کند.
✨ امکانات
دسترسی رایگان به چت DeepSeek بدون نیاز به کلید API پولی
ارائه سرور سازگار با OpenAI
پشتیبانی از APIهای زیر:
/v1/chat/completions
/v1/models
سازگار با بخش Custom Provider در DeepSeek Harness
پشتیبانی از پاسخ‌دهی جریانی (Streaming)
پشتیبانی از حالت تفکر و استدلال (Thinking / Reasoner)
پشتیبانی از مدل‌های deepseek-chat و deepseek-reasoner
رابط خط فرمان تعاملی (CLI) از طریق chat.py
🚀 شروع سریع
1. دریافت پروژه و نصب وابستگی‌ها
bash
git clone https://github.com/YOUR_USERNAME/deepseek4free.git
cd deepseek4free

python -m venv venv


فعال‌سازی محیط مجازی:

ویندوز:

bash
venv\Scripts\activate


لینوکس و macOS:

bash
source venv/bin/activate


نصب وابستگی‌ها:

bash
pip install -r requirements.txt

2. دریافت توکن احراز هویت (Auth Token)
وارد وب‌سایت chat.deepseek.com شوید.
کلید F12 را فشار دهید تا ابزار Developer Tools باز شود.
به بخش Application بروید.
از قسمت Local Storage، دامنه https://chat.deepseek.com را انتخاب کنید.
مقدار userToken را پیدا و کپی کنید.

روش جایگزین از طریق کنسول مرورگر:

javascript
JSON.parse(localStorage.getItem("userToken")).value

نکته امنیتی: توکن حساب خود را محرمانه نگه دارید و هرگز آن را در مخزن عمومی GitHub منتشر نکنید.
3. تنظیمات پروژه

ابتدا فایل تنظیمات نمونه را کپی کنید:

bash
cp .env.example .env


سپس فایل .env را باز کنید و توکن دریافت‌شده را در محل مربوطه قرار دهید.

4. اجرای سرور OpenAI Proxy

برای اجرای سرور دستور زیر را وارد کنید:

bash
python openai_server.py


در صورت اجرای موفق، سرور روی آدرس زیر در دسترس خواهد بود:

text
http://127.0.0.1:8000/v1

🔌 استفاده در DeepSeek Harness

پس از اجرای سرور، مراحل زیر را دنبال کنید:

سرور را اجرا کنید:
bash
python openai_server.py

در DeepSeek Harness وارد بخش زیر شوید:
text
Settings → Models → Add Model Provider

گزینه Custom Model API را انتخاب کنید.
تنظیمات زیر را وارد کنید:
گزینه	مقدار
Provider ID	deepseek4free
Display Name	DeepSeek Free
Base URL	http://127.0.0.1:8000/v1
API Protocol	OpenAI Chat Completions
API Key	dummy
Model	deepseek-chat یا deepseek-reasoner
تنظیمات را ذخیره کرده و مدل موردنظر را انتخاب کنید.
💡 نکته: پس از تغییر Provider، بهتر است یک Session جدید در Harness ایجاد کنید تا از بروز مشکلات احتمالی مربوط به تاریخچه مکالمات قبلی جلوگیری شود.
💬 استفاده از رابط خط فرمان (CLI)

برای اجرای چت تعاملی، دستور زیر را اجرا کنید:

bash
python chat.py


با این دستور می‌توانید مستقیماً از طریق ترمینال با DeepSeek گفتگو کنید.

🌐 نقاط پایانی API
متد	مسیر	توضیحات
GET	/v1/models	نمایش فهرست مدل‌های موجود
POST	/v1/chat/completions	ارسال درخواست چت با پشتیبانی از Streaming و Non-Streaming
GET	/health	بررسی وضعیت سلامت سرور
🧪 نمونه درخواست API

نمونه زیر نحوه ارسال یک درخواست به سرور را نشان می‌دهد:

bash
curl http://127.0.0.1:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-chat",
    "messages": [
      {
        "role": "user",
        "content": "Hello"
      }
    ],
    "stream": false
  }'

⚠️ نکات و محدودیت‌ها
انقضای توکن: توکن احراز هویت ممکن است پس از مدتی منقضی شود. در این صورت باید مجدداً از وب‌سایت DeepSeek توکن دریافت کنید.
محدودیت درخواست: بک‌اند رایگان وب‌سایت DeepSeek دارای محدودیت تعداد درخواست است.
Cloudflare: ممکن است Cloudflare در برخی مواقع درخواست‌ها را مسدود کند.
تاریخچه مکالمات: تاریخچه مکالمات Harness به‌طور کامل به بک‌اند ارسال نمی‌شود. در نسخه فعلی، برای سادگی و جلوگیری از خطاهای مربوط به محتوای خالی (null-content errors)، فقط آخرین پیام کاربر ارسال می‌شود.
این پروژه با اهداف آموزشی و استفاده شخصی توسعه داده شده است. لطفاً مسئولانه از آن استفاده کنید و شرایط استفاده از سرویس DeepSeek را رعایت کنید.
📁 ساختار پروژه
text
deepseek4free/
│
├── dsk/                  # کتابخانه اصلی
│   ├── api.py            # ارتباط با API
│   ├── pow.py            # محاسبات Proof of Work
│   ├── wasm/             # فایل‌های WebAssembly
│   └── ...
│
├── openai_server.py      # سرور پراکسی سازگار با OpenAI
├── chat.py               # رابط چت تعاملی CLI
├── example.py            # نمونه کد استفاده
├── requirements.txt      # وابستگی‌های پروژه
├── .env.example          # فایل نمونه تنظیمات
└── README.md             # مستندات پروژه

🔗 پروژه اصلی

این نسخه یک Fork از پروژه اصلی است که امکانات و بهبودهای زیر را اضافه می‌کند:

اضافه شدن پراکسی پایدار و سازگار با OpenAI
رفع مشکلات سازگاری با نسخه‌های جدیدتر Python
بهبود مدیریت درخواست‌ها برای سازگاری بهتر با DeepSeek Harness
ساده‌سازی نحوه استفاده از API در ابزارهای شخص ثالث
📜 مجوز استفاده (License)

برای مشاهده شرایط استفاده و مجوز پروژه، فایل LICENSE را مطالعه کنید.

ساخته‌شده برای دسترسی ساده‌تر به DeepSeek و استفاده از آن در ابزارهای سازگار با OpenAI.
