Certainly! Here's a README file for your Telegram Appointment Booking Bot project:

# Telegram Appointment Booking Bot

This is a Telegram bot that allows users to book, reschedule, cancel, and check appointments. It's designed for a medical clinic or any service-based business that requires appointment scheduling.

## Features

- Book a new appointment
- Reschedule an existing appointment
- Cancel an appointment
- Check appointment details
- Helper function for support

## Requirements

- Python 3.7 or higher
- `python-telegram-bot` library
- `google-api-python-client` library
- A Telegram Bot Token (obtainable from BotFather on Telegram)
- Google Calendar API credentials (JSON file)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/telegram-appointment-bot.git
   cd telegram-appointment-bot
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install python-telegram-bot google-api-python-client
   ```

4. Set up your Telegram Bot:
   - Talk to [@BotFather](https://t.me/botfather) on Telegram.
   - Create a new bot with the `/newbot` command.
   - Get your bot token and replace `"YOUR_BOT_TOKEN"` in the code with your actual token.

5. Set up Google Calendar API:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Enable the Google Calendar API.
   - Create credentials (Service Account Key) and download the JSON file.
   - Rename the JSON file to `durable-pulsar-419609-8202f7a8b4a4.json` (or update the `SERVICE_ACCOUNT_FILE` in the code).
   - Share your Google Calendar with the service account email.

## Usage

1. Start the bot:
   ```
   python bot.py
   ```

2. Open Telegram and start a chat with your bot.

3. Use the `/start` command to see the available options:
   - Book Appointment
   - Reschedule Appointment
   - Cancel Appointment
   - Check Appointment Details
   - Help

4. To book an appointment:
   - Click on "Book Appointment".
   - Enter your name when prompted.
   - Enter your 10-digit phone number.
   - Select a date from the next 5 available weekdays.
   - Choose a time slot between 9 AM and 6 PM.
   - Confirm your appointment details.

5. Other functionalities (reschedule, cancel, check) require an Appointment ID, which you would typically provide to the user after a successful booking.

## Project Structure

- `bot.py`: Main script containing the bot logic.
- `durable-pulsar-419609-8202f7a8b4a4.json`: Google Calendar API credentials file (you need to provide this).

## Functions

- `start(update, context)`: Handles the `/start` command, displays the main menu.
- `button(update, context)`: Handles the main menu button callbacks.
- `handle_message(update, context)`: Handles text messages for name and phone input.
- `select_date(update, context)`: Displays a keyboard with the next 5 available weekdays.
- `select_date_time(update, context)`: Handles date and time selection, and confirmation.

## Contributing

Feel free to fork this project and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact

For support, contact us at support@medical_jam.com or call 9265745362.

---

This README provides an overview of your project, instructions for setting it up, how to use it, and some basic information about its structure and functionality. You can further customize it based on your specific needs, such as adding more details about error handling, deployment, or any additional features you might implement.