# Auto Message Bot

The Auto Message Bot is a Discord bot that can be used to send automated messages at a specified interval in Discord servers by ZaddY

Features:
- Set an automated message to be sent at a specified interval.
- Stop the automated messages anytime.
- Authorization for using the bot limited to a specific user ID.

Prerequisites:
- Python 3.7 or higher
- discord.py library

Installation:
1. Clone the repository or fork it in [replit](https://replit.com/@terimakafan14/AutoMessage-Discord-Self-Bot#)
2. Install the required packages with the following command:
   ```pip install discord.py==1.7.3 asyncio==3.4.3```
3. Replace 'your_token_here' in the main.py file with your Discord bot token.
4. Set the AUTHORIZED_USER_ID variable in the main.py file to the authorized user's ID.

Usage:
1. Run the bot script using the following command:
   python main.py
2. Use the following commands in a text channel where the bot is present:
   - !set_auto_message: Starts the process of setting up an automated message.
   - stop: Stops the automated messages.
   Only the authorized user with the specified user ID can use these commands.

Configuration:
- AUTHORIZED_USER_ID: The Discord user ID of the authorized user allowed to use the commands.
- TOKEN: Your Discord bot token.

Contributing:
Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or a pull request.
