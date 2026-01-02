from pyrogram import Client, filters
from time import time
from config import *
from database import *

app = Client(
    "business_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


@app.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply(
        "🤖 Welcome\n\n"
        "Plans:\n"
        "/buy_basic – 7 days\n"
        "/buy_pro – 30 days\n"
        "/buy_vip – 90 days\n"
    )


# ---- BUY COMMANDS ----

@app.on_message(filters.command("buy_basic"))
async def buy_basic(_, msg):
    await activate(msg.from_user.id, "basic", msg)


@app.on_message(filters.command("buy_pro"))
async def buy_pro(_, msg):
    await activate(msg.from_user.id, "pro", msg)


@app.on_message(filters.command("buy_vip"))
async def buy_vip(_, msg):
    await activate(msg.from_user.id, "vip", msg)


async def activate(user_id, plan, msg):
    days = PLANS[plan]
    expiry = int(time()) + days * 86400
    add_user(user_id, plan, expiry)

    await msg.reply(
        f"✅ Subscription Activated\n\n"
        f"Plan: {plan.upper()}\n"
        f"Valid for: {days} days"
    )


# ---- ADMIN COMMANDS ----

@app.on_message(filters.command("add") & filters.user(ADMINS))
async def admin_add(_, msg):
    user_id = int(msg.command[1])
    plan = msg.command[2]
    days = int(msg.command[3])

    expiry = int(time()) + days * 86400
    add_user(user_id, plan, expiry)

    await msg.reply("✅ User added")


@app.on_message(filters.command("remove") & filters.user(ADMINS))
async def admin_remove(_, msg):
    user_id = int(msg.command[1])
    remove_user(user_id)
    await msg.reply("❌ User removed")


@app.on_message(filters.command("status"))
async def status(_, msg):
    user = get_user(msg.from_user.id)

    if not user:
        await msg.reply("❌ No active plan")
        return

    remaining = user[2] - int(time())
    days = remaining // 86400

    await msg.reply(
        f"📦 Plan: {user[1]}\n"
        f"⏳ Days left: {days}"
    )


print("✅ Bot running")
app.run()
