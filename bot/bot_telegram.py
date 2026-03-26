#!/usr/bin/env python
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.bot.secret'))

from handlers.commands import handle_text, start as cmd_start, help as cmd_help, health, labs, scores

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 Labs", callback_data='labs'),
         InlineKeyboardButton("📊 Scores", callback_data='scores')],
        [InlineKeyboardButton("📈 Timeline", callback_data='timeline'),
         InlineKeyboardButton("👥 Groups", callback_data='groups')],
        [InlineKeyboardButton("🔄 Sync", callback_data='sync')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'labs':
        await query.edit_message_text(handle_text("what labs are available"))
    elif query.data == 'scores':
        await query.edit_message_text("Send /scores <lab> (e.g., /scores lab-04)")
    elif query.data == 'timeline':
        await query.edit_message_text("Send /timeline <lab> (e.g., /timeline lab-04)")
    elif query.data == 'groups':
        await query.edit_message_text("Send /groups <lab> (e.g., /groups lab-04)")
    elif query.data == 'sync':
        await query.edit_message_text(handle_text("sync the data"))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(cmd_help())

async def health_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(health())

async def labs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(labs())

async def scores_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    lab = args[0] if args else None
    await update.message.reply_text(scores(lab))

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = handle_text(update.message.text)
    await update.message.reply_text(response)

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("BOT_TOKEN not set", file=sys.stderr)
        return
    
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("health", health_command))
    app.add_handler(CommandHandler("labs", labs_command))
    app.add_handler(CommandHandler("scores", scores_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    print("Bot starting...")
    app.run_polling()

if __name__ == "__main__":
    import sys
    main()
