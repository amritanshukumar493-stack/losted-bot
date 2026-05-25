import os
import re
import gc
import json
import time
import random
import asyncio
import logging
import requests

from yt_dlp import YoutubeDL

from pyrogram import Client, filters, enums
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ChatPermissions
)

from pyrogram.errors import (
    FloodWait,
    ChatAdminRequired,
    UserAdminInvalid
)

API_ID = 30607967
API_HASH = "c2fd1d5d420922dd0a8eec4e12e7d862"
BOT_TOKEN = "8820452200:AAFsmTcX5qwRKVU3zaXQurlJsev4_TEBgeY"

OWNER_ID = 8074231185 # Apna real Telegram User ID yahan daal lena admin commands ke liye
BOT_USERNAME = "LOSTED_EVERx" # YAHAN APNE BOT KA ASLI USERNAME DAAL BINA @ KE

CHANNEL_URL = "https://t.me/+ew3vF7QqEVRkYTVh"
SUPPORT_URL = "https://t.me/LOSTED_EVERx"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

LOGGER = logging.getLogger(__name__)

app = Client(
    "premium_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=25,
    sleep_threshold=30,
    parse_mode=enums.ParseMode.MARKDOWN
)

os.makedirs("downloads", exist_ok=True)
os.makedirs("database", exist_ok=True)

WARN_DB = "database/warns.json"

COOLDOWN = {}
TAG_STOPS = {}

START_TEXT = """
╭━━━━━━━━━━━━━━━╮
┃ 👾 — ͟͞͞ 𝐋𝚶𝛅𝚻𝚬𝐃 𝚬𝐕𝚬𝐑𝚼𝚻𝚮𝚰𝚴𝐆ˎˊ˗
╰━━━━━━━━━━━━━━━╯

✨ ᴡᴇʟᴄᴏᴍᴇ {},

⚙️ ᴏғғɪᴄɪᴀʟ ʙᴏᴛ ʙʏ ʙʜᴏᴏᴍs
🚀 ᴀᴅᴠᴀɴᴄᴇᴅ ᴛᴀɢɢɪɴɢ & ᴍᴏᴅᴇʀᴀᴛɪᴏɴ 
⚡ @LOSTED_EVERx

✨ ᴘʟᴇᴀsᴇ sᴇʟᴇᴄᴛ ᴀɴ ᴏᴘᴛɪᴏɴ ғʀᴏᴍ ᴛʜᴇ ᴍᴇɴᴜ ʙᴇʟᴏᴡ.
"""

COMMANDS_TEXT = """
╭━━━━━━━━━━━━━━━╮
┃ 📚 ᴄᴏᴍᴍᴀɴᴅ ᴍᴇɴᴜ
╰━━━━━━━━━━━━━━━╯

✨ Cʜᴏᴏsᴇ ᴀ ᴄᴀᴛᴇɢᴏʀʏ ʙᴇʟᴏᴡ ᴛᴏ ᴇxᴘʟᴏʀᴇ.
"""

TAG_TEXT = """
📚 ᴛᴀɢɢɪɴɢ ᴄᴏᴍᴍᴀɴᴅs :

/tektag ➠ Tᴀɢ ᴜsᴇʀs ɪɴᴅɪᴠɪᴅᴜᴀʟʟʏ.
/utag ➠ Tᴀɢ ᴜsᴇʀs ɪɴ ʙᴀᴛᴄʜᴇs ᴏғ 5.
/mtag ➠ Rᴇᴘʟʏ ᴛᴏ ᴍᴇᴅɪᴀ ᴛᴏ ᴛᴀɢ ᴜsᴇʀs.
/atag ➠ Tᴀɢ ᴀʟʟ ᴀᴅᴍɪɴs.
/etag ➠ Eᴍᴏᴊɪ ᴛᴀɢ sʏsᴛᴇᴍ.
/stag ➠ Cᴜsᴛᴏᴍ ᴛᴇxᴛ ᴛᴀɢ.
/stop ➠ Sᴛᴏᴘ ᴛʜᴇ ᴛᴀɢɢɪɴɢ ᴘʀᴏᴄᴇss.
"""

GAME_TEXT = """
🎳 ɢᴀᴍᴇ ᴄᴏᴍᴍᴀɴᴅs :

/slap ➠ Sʟᴀᴘ ᴀ ᴜsᴇʀ.
/kiss ➠ Kɪss ᴀ ᴜsᴇʀ.
/quote ➠ Gᴇᴛ ᴀ ʀᴀɴᴅᴏᴍ ǫᴜᴏᴛᴇ.
/dart ➠ Tʜʀᴏᴡ ᴀ ᴅᴀʀᴛ.
/football ➠ Kɪᴄᴋ ᴀ ғᴏᴏᴛʙᴀʟʟ.
/slot ➠ Sᴘɪɴ ᴛʜᴇ sʟᴏᴛ ᴍᴀᴄʜɪɴᴇ.
/basket ➠ Sʜᴏᴏᴛ ᴀ ʙᴀsᴋᴇᴛʙᴀʟʟ.
/bowling ➠ Bᴏᴡʟ ᴀ ʙᴀʟʟ.
/dice ➠ Rᴏʟʟ ᴛʜᴇ ᴅɪᴄᴇ.
"""

OTHER_TEXT = """
🗣 ᴏᴛʜᴇʀ ᴄᴏᴍᴍᴀɴᴅs :

/admins ➠ Lɪsᴛ ᴀʟʟ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs.
/bots ➠ Lɪsᴛ ᴀʟʟ ʙᴏᴛs ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.
/info ➠ Gᴇᴛ ɢʀᴏᴜᴘ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.
/id ➠ Gᴇᴛ ʏᴏᴜʀ ᴜsᴇʀ ID.
/weather ➠ Cʜᴇᴄᴋ ᴛʜᴇ ᴡᴇᴀᴛʜᴇʀ.
/song ➠ Pʟᴀʏ ɴɪɢʜᴛ ᴠɪʙᴇs ᴍᴜsɪᴄ.

/video ➠ Dᴏᴡɴʟᴏᴀᴅ ᴀ ᴠɪᴅᴇᴏ.
"""

ADMIN_TEXT = """
🛡 ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs :

/ban ➠ Bᴀɴ ᴀ ᴜsᴇʀ.
/unban ➠ Uɴʙᴀɴ ᴀ ᴜsᴇʀ.
/kick ➠ Kɪᴄᴋ ᴀ ᴜsᴇʀ.
/mute ➠ Mᴜᴛᴇ ᴀ ᴜsᴇʀ.
/unmute ➠ Uɴᴍᴜᴛᴇ ᴀ ᴜsᴇʀ.
/warn ➠ Wᴀʀɴ ᴀ ᴜsᴇʀ.
/warns ➠ Cʜᴇᴄᴋ ᴜsᴇʀ ᴡᴀʀɴɪɴɢs.
/pin ➠ Pɪɴ ᴀ ᴍᴇsᴀɢᴇ.
/unpin ➠ Uɴᴘɪɴ ᴀ ᴍᴇssᴀɢᴇ.
/purge ➠ Dᴇʟᴇᴛᴇ ᴍᴜʟᴛɪᴘʟᴇ ᴍᴇssᴀɢᴇs.
"""

def load_json(path):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

warns = load_json(WARN_DB)

def start_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ",
                url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
            )
        ],
        [
            InlineKeyboardButton(
                "📚 ᴄᴏᴍᴍᴀɴᴅs",
                callback_data="main_commands"
            )
        ],
        [
            InlineKeyboardButton(
                "✨ ᴄʜᴀɴɴᴇʟ",
                url=CHANNEL_URL
            )
        ],
        [
            InlineKeyboardButton(
                "👑 𝑨𝑵𝑼𝑹𝑨𝑮 𝑩𝑹𝑶 ",
                url="https://t.me/fearlessanurag"
            ),
            InlineKeyboardButton(
                "🎧 sᴜᴘᴘᴏʀᴛ",
                url=SUPPORT_URL
            )
        ]
    ])

def commands_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📚 ᴛᴀɢs",
                callback_data="cmd_tags"
            )
        ],
        [
            InlineKeyboardButton(
                "🎳 ɢᴀᴍᴇs",
                callback_data="cmd_games"
            )
        ],
        [
            InlineKeyboardButton(
                "🗣 ᴏᴛʜᴇʀs",
                callback_data="cmd_other"
            )
        ],
        [
            InlineKeyboardButton(
                "🛡 ᴀᴅᴍɪɴ",
                callback_data="cmd_admin"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ ɢᴏ ʙᴀᴄᴋ",
                callback_data="back_start"
            )
        ]
    ])

def submenu_back():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "⬅️ ɢᴏ ʙᴀᴄᴋ",
                callback_data="back_commands"
            )
        ]
    ])

async def safe_edit(message, text, buttons):
    try:
        await message.edit_text(text, reply_markup=buttons)
    except Exception:
        pass

async def error_group(msg):
    return await msg.reply_text("⚠️ Tʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs.")

async def error_reply(msg):
    return await msg.reply_text("⚠️ Pʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ.")

async def error_admin(msg):
    return await msg.reply_text("❌ Yᴏᴜ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")

async def error_bot_admin(msg):
    return await msg.reply_text("❌ I ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀᴇǫᴜɪʀᴇᴅ ᴘᴇʀᴍɪssɪᴏɴs.")

async def is_admin(chat_id, user_id):
    try:
        member = await app.get_chat_member(chat_id, user_id)
        return member.status in [
            enums.ChatMemberStatus.ADMINISTRATOR,
            enums.ChatMemberStatus.OWNER
        ]
    except Exception:
        return False

async def cleanup():
    while True:
        gc.collect()
        for file in os.listdir("downloads"):
            path = os.path.join("downloads", file)
            try:
                if os.path.isfile(path):
                    if time.time() - os.path.getmtime(path) > 300:
                        os.remove(path)
            except Exception:
                pass
        await asyncio.sleep(120)

@app.on_message(filters.command("start"))
async def start(_, msg):
    asyncio.create_task(cleanup())
    await msg.reply_text(
        START_TEXT.format(msg.from_user.mention),
        reply_markup=start_buttons()
    )

@app.on_callback_query()
async def callbacks(_, cq):
    try:
        if cq.data == "main_commands":
            await safe_edit(cq.message, COMMANDS_TEXT, commands_buttons())
        elif cq.data == "cmd_tags":
            await safe_edit(cq.message, TAG_TEXT, submenu_back())
        elif cq.data == "cmd_games":
            await safe_edit(cq.message, GAME_TEXT, submenu_back())
        elif cq.data == "cmd_other":
            await safe_edit(cq.message, OTHER_TEXT, submenu_back())
        elif cq.data == "cmd_admin":
            await safe_edit(cq.message, ADMIN_TEXT, submenu_back())
        elif cq.data == "back_start":
            await safe_edit(cq.message, START_TEXT.format(cq.from_user.mention), start_buttons())
        elif cq.data == "back_commands":
            await safe_edit(cq.message, COMMANDS_TEXT, commands_buttons())
        elif cq.data == "play_night_vibes":
            await cq.message.delete()
            await app.send_audio(
                chat_id=cq.message.chat.id,
                audio="vibe.mp3",
                caption="🎵 **𝑳𝑶𝑺𝑻𝑬𝑫 — 𝐍𝚰𝚪𝚮𝐓 𝐕𝚰𝚩𝚬𝐒**\n\n✨ @LOSTED_EVERx",
                title="Banjaare - Bairan",
                performer="Night Vibes"
            )
        await cq.answer("⚡")
    except Exception as e:
        LOGGER.error(e)

async def get_users(chat_id, admins=False):
    users = []
    async for member in app.get_chat_members(chat_id):
        if member.user.is_bot:
            continue
        if admins:
            if member.status not in [
                enums.ChatMemberStatus.ADMINISTRATOR,
                enums.ChatMemberStatus.OWNER
            ]:
                continue
        users.append(member.user)
    return users

async def mention_users(msg, users, text="🌿"):
    cid = msg.chat.id
    TAG_STOPS[cid] = False
    chunk = []

    for user in users:
        if TAG_STOPS.get(cid):
            break
        chunk.append(f"{text} [{user.first_name}](tg://user?id={user.id})")
        if len(chunk) == 5:
            try:
                await msg.reply_text("\n".join(chunk))
                await asyncio.sleep(2)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception:
                pass
            chunk = []
    if chunk:
        try:
            await msg.reply_text("\n".join(chunk))
        except Exception:
            pass

def group_only(func):
    async def wrapper(_, msg):
        if msg.chat.type == enums.ChatType.PRIVATE:
            return await error_group(msg)
        return await func(_, msg)
    return wrapper

@app.on_message(filters.command("stop"))
@group_only
async def stop(_, msg):
    TAG_STOPS[msg.chat.id] = True
    await msg.reply_text("🛑 Tᴀɢɢɪɴɢ ᴘʀᴏᴄᴇss sᴛᴏᴘᴘᴇᴅ.")

@app.on_message(filters.command("utag"))
@group_only
async def utag(_, msg):
    users = await get_users(msg.chat.id)
    await mention_users(msg, users, "⚡")

@app.on_message(filters.command("tektag"))
@group_only
async def tektag(_, msg):
    users = await get_users(msg.chat.id)
    await mention_users(msg, users, "🌿")

@app.on_message(filters.command("atag"))
@group_only
async def atag(_, msg):
    users = await get_users(msg.chat.id, admins=True)
    await mention_users(msg, users, "👑")

@app.on_message(filters.command("etag"))
@group_only
async def etag(_, msg):
    emojis = ["🔥", "⚡", "🚀", "💎", "🌿"]
    users = await get_users(msg.chat.id)
    for user in users:
        try:
            await msg.reply_text(f"{random.choice(emojis)} [{user.first_name}](tg://user?id={user.id})")
            await asyncio.sleep(1.5)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            pass

@app.on_message(filters.command("stag"))
@group_only
async def stag(_, msg):
    data = msg.text.split(None, 1)
    if len(data) < 2:
        return await msg.reply_text("⚠️ Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ sᴏᴍᴇ ᴛᴇxᴛ.")
    users = await get_users(msg.chat.id)
    await mention_users(msg, users, data[1])

@app.on_message(filters.command("mtag"))
@group_only
async def mtag(_, msg):
    if not msg.reply_to_message:
        return await error_reply(msg)
    users = await get_users(msg.chat.id)
    text = "\n".join([f"🌿 [{u.first_name}](tg://user?id={u.id})" for u in users[:50]])
    await msg.reply_to_message.copy(msg.chat.id, caption=text)

async def get_target_user(msg):
    if not msg.reply_to_message:
        return None
    return msg.reply_to_message.from_user

@app.on_message(filters.command(["ban", "unban", "kick", "mute", "unmute"]))
@group_only
async def admin_tools(_, msg):
    if not await is_admin(msg.chat.id, msg.from_user.id):
        return await error_admin(msg)
    
    user = await get_target_user(msg)
    if not user:
        return await error_reply(msg)

    try:
        cmd = msg.command[0]
        if cmd == "ban":
            await app.ban_chat_member(msg.chat.id, user.id)
            await msg.reply_text(f"🔨 {user.mention} ʜᴀs ʙᴇᴇɴ ʙᴀɴɴᴇᴅ.")
        elif cmd == "unban":
            await app.unban_chat_member(msg.chat.id, user.id)
            await msg.reply_text(f"♻️ {user.mention} ʜᴀs ʙᴇᴇɴ ᴜɴʙᴀɴɴᴇᴅ.")
        elif cmd == "kick":
            await app.ban_chat_member(msg.chat.id, user.id)
            await app.unban_chat_member(msg.chat.id, user.id)
            await msg.reply_text(f"👢 {user.mention} ᴡᴀs ᴋɪᴄᴋᴇᴅ ғʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ.")
        elif cmd == "mute":
            await app.restrict_chat_member(msg.chat.id, user.id, ChatPermissions())
            await msg.reply_text(f"🔇 {user.mention} ʜᴀs ʙᴇᴇɴ ᴍᴜᴛᴇᴅ.")
        elif cmd == "unmute":
            await app.restrict_chat_member(msg.chat.id, user.id, ChatPermissions(can_send_messages=True))
            await msg.reply_text(f"🔊 {user.mention} ʜᴀs ʙᴇᴇɴ ᴜɴᴍᴜᴛᴇᴅ.")
    except (ChatAdminRequired, UserAdminInvalid):
        return await error_bot_admin(msg)
    except Exception as e:
        LOGGER.error(e)

@app.on_message(filters.command("warn"))
@group_only
async def warn(_, msg):
    if not await is_admin(msg.chat.id, msg.from_user.id):
        return await error_admin(msg)
    user = await get_target_user(msg)
    if not user:
        return await error_reply(msg)
    
    gid, uid = str(msg.chat.id), str(user.id)
    if gid not in warns:
        warns[gid] = {}
    
    warns[gid][uid] = warns[gid].get(uid, 0) + 1
    save_json(WARN_DB, warns)
    await msg.reply_text(f"⚠️ {user.mention} • {warns[gid][uid]} Wᴀʀɴɪɴɢ(s)")

@app.on_message(filters.command("warns"))
@group_only
async def warns_cmd(_, msg):
    user = await get_target_user(msg)
    if not user:
        return await error_reply(msg)
    
    gid, uid = str(msg.chat.id), str(user.id)
    count = warns.get(gid, {}).get(uid, 0)
    await msg.reply_text(f"⚠️ {user.mention} ʜᴀs {count} Wᴀʀɴɪɴɢ(s)")

@app.on_message(filters.command("pin"))
@group_only
async def pin(_, msg):
    if not msg.reply_to_message:
        return await error_reply(msg)
    await msg.reply_to_message.pin()
    await msg.reply_text("📌 Mᴇssᴀɢᴇ ᴘɪɴɴᴇᴅ.")

@app.on_message(filters.command("unpin"))
@group_only
async def unpin(_, msg):
    await app.unpin_all_chat_messages(msg.chat.id)
    await msg.reply_text("📍 Pɪɴ ʀᴇᴍᴏᴠᴇᴅ.")

@app.on_message(filters.command("purge"))
@group_only
async def purge(_, msg):
    if not msg.reply_to_message:
        return await error_reply(msg)
    
    deleted = 0
    for i in range(msg.reply_to_message.id, msg.id):
        try:
            await app.delete_messages(msg.chat.id, i)
            deleted += 1
        except Exception:
            pass
    await msg.reply_text(f"🗑 {deleted} ᴍᴇssᴀɢᴇs ᴅᴇʟᴇᴛᴇᴅ.")

SLAPS = ["🔥 Lᴀɴᴅᴇᴅ ᴀ ʜᴇᴀᴠʏ sʟᴀᴘ ᴏɴ", "⚡ Gᴀᴠᴇ ᴀɴ ᴇᴘɪᴄ sʟᴀᴘ ᴛᴏ", "💥 Sᴍᴀᴄᴋᴇᴅ"]
QUOTES = ["🌿 Life is a beautiful game, play it well.", "⚡ Success requires patience and perseverance.", "🚀 Give your best to win the battles of life."]

@app.on_message(filters.command("slap"))
async def slap(_, msg):
    if not msg.reply_to_message:
        return await error_reply(msg)
    user = msg.reply_to_message.from_user
    await msg.reply_text(f"{random.choice(SLAPS)}\n\n👤 {user.mention}")

@app.on_message(filters.command("kiss"))
async def kiss(_, msg):
    if not msg.reply_to_message:
        return await error_reply(msg)
    user = msg.reply_to_message.from_user
    await msg.reply_text(f"💋 Kɪssᴇᴅ {user.mention}.")

@app.on_message(filters.command("quote"))
async def quote(_, msg):
    await msg.reply_text(random.choice(QUOTES))

@app.on_message(filters.command("dart"))
async def dart(_, msg):
    await app.send_dice(msg.chat.id, emoji="🎯")

@app.on_message(filters.command("slot"))
async def slot(_, msg):
    await app.send_dice(msg.chat.id, emoji="🎰")

@app.on_message(filters.command("basket"))
async def basket(_, msg):
    await app.send_dice(msg.chat.id, emoji="🏀")

@app.on_message(filters.command("bowling"))
async def bowling(_, msg):
    await app.send_dice(msg.chat.id, emoji="🎳")

@app.on_message(filters.command("dice"))
async def dice(_, msg):
    await app.send_dice(msg.chat.id, emoji="🎲")

@app.on_message(filters.command("football"))
async def football(_, msg):
    await app.send_dice(msg.chat.id, emoji="⚽")

@app.on_message(filters.command("admins"))
@group_only
async def admins(_, msg):
    text = "👑 **Gʀᴏᴜᴘ Aᴅᴍɪɴs**\n\n"
    async for member in app.get_chat_members(msg.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        text += f"• {member.user.mention}\n"
    await msg.reply_text(text)

@app.on_message(filters.command("bots"))
@group_only
async def bots(_, msg):
    text = "🤖 **Gʀᴏᴜᴘ Bᴏᴛs**\n\n"
    async for member in app.get_chat_members(msg.chat.id):
        if member.user.is_bot:
            text += f"• {member.user.mention}\n"
    await msg.reply_text(text)

@app.on_message(filters.command("id"))
async def id_cmd(_, msg):
    text = f"🆔 **USER ID:** `{msg.from_user.id}`\n💬 **CHAT ID:** `{msg.chat.id}`"
    await msg.reply_text(text)

@app.on_message(filters.command("ping"))
async def ping(_, msg):
    start = time.time()
    m = await msg.reply_text("🏓")
    end = time.time()
    ms = round((end - start) * 1000)
    await m.edit_text(f"🏓 Pᴏɴɢ! `{ms} ms`")

@app.on_message(filters.command("info"))
@group_only
async def info(_, msg):
    chat = await app.get_chat(msg.chat.id)
    text = f"🌿 **Gʀᴏᴜᴘ Iɴғᴏʀᴍᴀᴛɪᴏɴ**\n\n📛 **Nᴀᴍᴇ:** {chat.title}\n🆔 **ID:** `{chat.id}`\n👥 **Mᴇᴍʙᴇʀs:** {chat.members_count}"
    await msg.reply_text(text)

@app.on_message(filters.command("weather"))
async def weather(_, msg):
    data = msg.text.split(None, 1)
    if len(data) < 2:
        return await msg.reply_text("⚠️ Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴄɪᴛʏ ɴᴀᴍᴇ.")
    
    city = data[1]
    try:
        r = requests.get(f"https://wttr.in/{city}?format=3", timeout=10)
        await msg.reply_text(f"🌦 {r.text}")
    except Exception:
        await msg.reply_text("❌ Cᴏᴜʟᴅ ɴᴏᴛ ғᴇᴛᴄʜ ᴡᴇᴀᴛʜᴇʀ ᴅᴀᴛᴀ.")

@app.on_message(filters.command("video"))
async def video(_, msg):
    data = msg.text.split(None, 1)
    if len(data) < 2:
        return await msg.reply_text("⚠️ Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ʟɪɴᴋ.")
    
    url = data[1]
    wait = await msg.reply_text("📥 Dᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ...")
    file_path = None

    try:
        ydl_opts = {
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "format": "mp4/best",
            "quiet": True,
            "noplaylist": True
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        await msg.reply_video(video=file_path, caption="✅ Vɪᴅᴇᴏ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.")
        await wait.delete()
    except Exception as e:
        LOGGER.error(e)
        await wait.edit_text("❌ Dᴏᴡɴʟᴏᴀᴅ ғᴀɪʟᴇᴅ.")
    finally:
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass

@app.on_message(filters.command("song"))
async def play_song(_, msg):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("▶️ PLAY SONG", callback_data="play_night_vibes")]
    ])
    await msg.reply_text(
        "🎵 **𝑳𝑶𝑺𝑻𝑬𝑫 — 𝐍𝚰𝚪𝚮𝐓 𝐕𝚰𝚩𝚬𝐒**\n\n👇 Cʟɪᴄᴋ ʙᴇʟᴏᴡ ᴛᴏ ᴅʀᴏᴘ ᴛʜᴇ ᴠɪʙᴇ!",
        reply_markup=buttons
    )

LINK_REGEX = r"(https?://|t.me/|telegram.me)"

@app.on_message(filters.text & filters.group)
async def anti_link(_, msg):
    try:
        if not msg.text:
            return
        if re.search(LINK_REGEX, msg.text.lower()):
            if await is_admin(msg.chat.id, msg.from_user.id):
                return
            await msg.delete()
            warn = await msg.reply_text(f"🚫 {msg.from_user.mention}, Lɪɴᴋs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ʜᴇʀᴇ!")
            await asyncio.sleep(5)
            await warn.delete()
    except Exception:
        pass

if __name__ == "__main__":
    LOGGER.info("LOSTED Bot is Online!")
    app.run()
    