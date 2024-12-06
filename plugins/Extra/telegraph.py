import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegraph import upload_file


@Client.on_message(filters.command("telegraph") & filters.private)
async def telegraph_upload(bot, update):
    # Ask the user to send a photo or video
    t_msg = await bot.ask(chat_id=update.from_user.id, text="Now send me your photo or video under 5MB to get a Telegraph link.")

    # Check if a valid file is sent
    if not t_msg.media:
        await update.reply_text("Please send a valid photo or video under 5MB!")
        return

    # Start downloading the file
    text = await update.reply_text(
        text="<code>Downloading to my server...</code>", disable_web_page_preview=True
    )
    media = await t_msg.download()  # This downloads the file to the current directory

    if not media:
        await text.edit_text("Failed to download the file!")
        return

    # Upload to Telegraph
    await text.edit_text(
        text="<code>Downloading completed. Now uploading to telegra.ph...</code>",
        disable_web_page_preview=True,
    )

    try:
        response = upload_file(media)  # Upload the file to Telegraph
    except Exception as error:
        print(error)
        await text.edit_text(f"Error: {error}")
        return

    # Remove the file after upload
    try:
        os.remove(media)
    except Exception as error:
        print(error)

    # Send the link to the user
    await text.edit_text(
        text=f"<b>Link:</b>\n\n<code>https://graph.org{response[0]}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Open Link", url=f"https://graph.org{response[0]}"
                    ),
                    InlineKeyboardButton(
                        text="Share Link",
                        url=f"https://telegram.me/share/url?url=https://graph.org{response[0]}",
                    ),
                ],
                [InlineKeyboardButton(text="✗ Close ✗", callback_data="close")],
            ]
        ),
    )