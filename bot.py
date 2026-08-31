import asyncio
from pyrogram import Client, filters

# ==========================================
# 1. إعدادات حساب المطور والبوت
# ==========================================
API_ID =  
API_HASH = 
BOT_TOKEN = 

# ==========================================
# 2. معرفات المجموعات
# ==========================================
SOURCE_GROUP_ID = -   # مجموعة Ziiiizoooo (المراقبة)
TARGET_GROUP_ID = -   # مجموعة بووووت (التقارير)

# ==========================================
# تهيئة البوت
# ==========================================
app = Client(" ", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# قواميس الفلترة والكلمات الدلالية
INTENT_KEYWORDS = ["ابغى", "ابي", "احتاج", "مطلوب", "مين يسوي", "مين يضبط", "بكم", "تكلفة", "فزعتكم", "عاجل", "ابحث عن", "مشروع"]
SERVICE_CATEGORIES = {
    "💻 برمجة وتطوير": ["تطبيق", "موقع", "متجر", "سلة", "زد", "شوبيفاي", "مبرمج", "سكريبت", "كود", "منصة", "بوت"],
    "🎨 تصميم وجرافيك": ["لوقو", "شعار", "هوية بصرية", "بوست", "موشن جرافيك", "انفوجرافيك", "بنر", "تصميم واجهة"],
    "📊 أعمال ومحاسبة": ["دراسة جدوى", "داشبورد", "اكسيل", "محاسب", "قوائم مالية", "تقارير مالية", "ميزانية", "مسك دفاتر"],
    "📝 كتابة وترجمة": ["مقال", "بحث", "ترجمة", "محتوى", "سيرة ذاتية", "سي في", "بروفايل شركة", "تدقيق"],
    "📈 تسويق رقمي": ["حملة اعلانية", "سناب شات", "تيك توك", "سيو", "SEO", "تسويق", "ادارة حسابات", "مبيعات"]
}

@app.on_message(filters.chat(SOURCE_GROUP_ID) & filters.text)
async def process_leads(client, message):
    text = message.text
    if not any(word in text for word in INTENT_KEYWORDS):
        return

    detected_categories = []
    matched_services = []

    for category, keywords in SERVICE_CATEGORIES.items():
        matches = [kw for kw in keywords if kw in text]
        if matches:
            if category not in detected_categories:
                detected_categories.append(category)
            matched_services.extend(matches)

    if detected_categories:
        user_name = message.from_user.first_name if message.from_user else "مجهول"
        username = f"@{message.from_user.username}" if (message.from_user and message.from_user.username) else "لا يوجد"
        message_link = message.link or "غير متوفر"

        alert_msg = (
            f"🎯 **عميل جديد تم التقاطه!**\n\n"
            f"👤 **العميل:** {user_name} ({username})\n"
            f"📂 **الخدمة:** {', '.join(detected_categories)}\n"
            f"🔑 **الكلمات الملتقطة:** {', '.join(set(matched_services))}\n"
            f"💬 **الطلب:**\n{text}\n\n"
            f"🔗 [الذهاب للرسالة الأصلية]({message_link})"
        )
        await client.send_message(TARGET_GROUP_ID, alert_msg)

if __name__ == "__main__":
    print("🚀 جاري تشغيل رادار الفلترة لبوت (هنــد الــصافـي)...")
    app.run()
