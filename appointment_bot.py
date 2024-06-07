import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Google Calendar API setup
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'durable-pulsar-419609-8202f7a8b4a4.json'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)
calendar_id = 'primary'

# Define the start command handler
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Book Appointment", callback_data='book')],
        [InlineKeyboardButton("Reschedule Appointment", callback_data='reschedule')],
        [InlineKeyboardButton("Cancel Appointment", callback_data='cancel')],
        [InlineKeyboardButton("Check Appointment Details", callback_data='check')],
        [InlineKeyboardButton("Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome! Please choose an option:', reply_markup=reply_markup)

# Define the callback query handler
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == 'book':
        context.user_data['action'] = 'book'
        await query.edit_message_text(text="Please enter your name:")
    elif query.data == 'reschedule':
        context.user_data['action'] = 'reschedule'
        await query.edit_message_text(text="Please enter your Appointment ID:")
    elif query.data == 'cancel':
        context.user_data['action'] = 'cancel'
        await query.edit_message_text(text="Please enter your Appointment ID:")
    elif query.data == 'check':
        context.user_data['action'] = 'check'
        await query.edit_message_text(text="Please enter your Appointment ID:")
    elif query.data == 'help':
        await query.edit_message_text(text="For support, contact us at support@medical_jam.com or call 9265745362.")

# Define the message handler
async def handle_message(update: Update, context: CallbackContext) -> None:
    action = context.user_data.get('action')
    if action == 'book':
        if 'name' not in context.user_data:
            context.user_data['name'] = update.message.text
            await update.message.reply_text("Please enter your 10-digit phone number:")
        elif 'phone' not in context.user_data:
            phone = update.message.text
            if len(phone) == 10 and phone.isdigit():
                context.user_data['phone'] = phone
                await select_date(update, context)
            else:
                await update.message.reply_text("Invalid phone number. Please enter a 10-digit phone number:")
    elif action == 'reschedule':
        # Handle rescheduling logic here
        pass
    elif action == 'cancel':
        # Handle cancellation logic here
        pass
    elif action == 'check':
        # Handle checking appointment details logic here
        pass

# Define the date and time selection handler
async def select_date_time(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data.startswith("date_"):
        context.user_data['date'] = query.data.split("_")[1]
        time_slots = ['09:00 AM', '09:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', 
                     '12:00 PM', '12:30 PM', '01:00 PM', '01:30 PM', '02:00 PM', '02:30 PM', 
                     '03:00 PM', '03:30 PM', '04:00 PM', '04:30 PM', '05:00 PM', '05:30 PM', '06:00 PM']
        keyboard = [
            [InlineKeyboardButton(f"{time_slots[i]} to {time_slots[i+1]}", callback_data=f"time_{time_slots[i]}")] 
            for i in range(len(time_slots)-1)
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Please select a time slot for your appointment:", reply_markup=reply_markup)
    elif query.data.startswith("time_"):
        context.user_data['time'] = query.data.split("_")[1]
        # Confirmation step
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data='confirm_yes')],
            [InlineKeyboardButton("No", callback_data='confirm_no')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"Confirm your appointment:\nName: {context.user_data['name']}\nPhone: {context.user_data['phone']}\nDate: {context.user_data['date']}\nTime: {context.user_data['time']}\n\nIs this correct?", reply_markup=reply_markup)
    elif query.data == 'confirm_yes':
        await query.edit_message_text("Thank you! Your appointment has been confirmed.")
        # Add logic to save the appointment in Google Calendar or your database
    elif query.data == 'confirm_no':
        await query.edit_message_text("Appointment not confirmed. Please start over by typing /start.")

# Define the date selection handler
async def select_date(update: Update, context: CallbackContext) -> None:
    today = datetime.date.today()
    keyboard = []
    for i in range(14):  # Show next 14 days to ensure we have 5 weekdays
        date = today + datetime.timedelta(days=i)
        if date.weekday() < 5:  # Monday to Friday (0 to 4)
            keyboard.append([InlineKeyboardButton(date.strftime("%Y-%m-%d"), callback_data=f"date_{date.strftime('%Y-%m-%d')}")])
            if len(keyboard) == 5:  # Stop after getting 5 weekdays
                break
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select a date for your appointment:", reply_markup=reply_markup)

# Define the main function
def main() -> None:
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("TOEKN").build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(select_date_time, pattern='^(date|time|confirm)_'))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()