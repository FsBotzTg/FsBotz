from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from info import STREAM_MODE, URL, LOG_CHANNEL
from urllib.parse import quote_plus
from database.users_chats_db import db
from FsBotz.util.file_properties import get_name, get_hash, get_media_file_size
from FsBotz.util.human_readable import humanbytes
import humanize
import random

@Client.on_message(filters.private & filters.command("stream"))
async def stream_start(client, message):
#    if await db.has_premium_access(message.from_user.id):
    if STREAM_MODE == False:
        return 
    msg = await client.ask(message.chat.id, "**Now send me your file/video to get stream and download link**")
    if not msg.media:
        return await message.reply("**Please send me supported media.**")
    if msg.media in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
        file = getattr(msg, msg.media.value)
        filename = file.file_name
        filesize = humanize.naturalsize(file.file_size) 
        fileid = file.file_id
        user_id = message.from_user.id
        username =  message.from_user.mention 

        log_msg = await client.send_cached_media(
            chat_id=LOG_CHANNEL,
            file_id=fileid,
        )
        fileName = {quote_plus(get_name(log_msg))}
        stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        download = f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"

        await log_msg.reply_text(
            text=f"•• ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ꜰᴏʀ ɪᴅ #{user_id} \n•• ᴜꜱᴇʀɴᴀᴍᴇ : {username} \n\n•• ᖴᎥᒪᗴ Nᗩᗰᗴ : {fileName}",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Fast Download 🚀", url=download),  # we download Link
                                                InlineKeyboardButton('🖥️ Watch online 🖥️', url=stream)]])  # web stream Link
        )
                    
        rm=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("sᴛʀᴇᴀᴍ 🖥", url=stream),
                    InlineKeyboardButton('ᴅᴏᴡɴʟᴏᴀᴅ 📥', url=download)
                ]
            ] 
        )
        msg_text = """<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i>\n\n<b>📂 Fɪʟᴇ ɴᴀᴍᴇ :</b> <i>{}</i>\n\n<b>📦 Fɪʟᴇ ꜱɪᴢᴇ :</b> <i>{}</i>\n\n<b>📥 Dᴏᴡɴʟᴏᴀᴅ :</b><a href='{}' >ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>\n\n<b> 🖥ᴡᴀᴛᴄʜ  :</b> <a href='{}' >ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>\n\n<b>🚸 Nᴏᴛᴇ : ʟɪɴᴋ ᴡᴏɴ'ᴛ ᴇxᴘɪʀᴇ ᴛɪʟʟ ɪ ᴅᴇʟᴇᴛᴇ</b>"""

        await message.reply_text(text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(msg)), download, stream), quote=True, disable_web_page_preview=True, reply_markup=rm)
#    if not await db.has_premium_access(message.from_user.id):
#        return await message.reply("𝕐𝕠𝕦𝕣 𝕟𝕠𝕥 𝕒 𝕡𝕣𝕖𝕞𝕚𝕦𝕞 𝕦𝕤𝕖𝕣 ")