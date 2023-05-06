import discord
import asyncio

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

AUTHORIZED_USER_ID = USERID

auto_message_tasks = []  # Stores the tasks for sending auto messages
MAX_AUTO_MESSAGES = 3  # Maximum number of auto messages

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')

@client.event
async def on_message(message):
    if message.content.startswith('!set_auto_message'):
        if message.author.id == AUTHORIZED_USER_ID:
            await set_auto_message(message)
        else:
            await message.channel.send("Not authorized to use this command.")

    elif message.content.startswith('stop'):
        if message.author.id == AUTHORIZED_USER_ID:
            await stop_auto_message(message)

async def set_auto_message(message):
    if len(auto_message_tasks) >= MAX_AUTO_MESSAGES:
        await message.channel.send(f"You have reached the maximum limit of {MAX_AUTO_MESSAGES} auto messages.")
        return

    # Ask the user for the delay in seconds
    await message.channel.send("Please enter the delay in seconds between each auto message:")
    
    def check(m):
        return m.author == message.author and m.channel == message.channel

    delay_msg = await client.wait_for('message', check=check)
    delay = int(delay_msg.content)

    # Ask the user for the message content
    await message.channel.send("Please enter the content of the auto message:")
    content_msg = await client.wait_for('message', check=check)
    content = content_msg.content

    # Ask the user for the channel ID where the bot should send messages
    await message.channel.send("Please enter the channel ID where the bot should send messages:")
    channel_id_msg = await client.wait_for('message', check=check)
    channel_id = int(channel_id_msg.content)

    target_channel = client.get_channel(channel_id)
    if target_channel is None:
        await message.channel.send(f"Invalid channel ID. Please make sure the bot has access to the specified channel.")
        return

    # Schedule the auto message loop
    await message.channel.send(f"Auto message set. I will send '{content}' every {delay} second(s) to channel {target_channel.mention}.")
    task = asyncio.create_task(send_auto_messages(target_channel, content, delay))
    auto_message_tasks.append(task)

async def send_auto_messages(channel, content, delay):
    while True:
        await asyncio.sleep(delay)
        await channel.send(content)

async def stop_auto_message(message):
    global auto_message_tasks

    command_parts = message.content.split()
    if len(command_parts) == 1:
        await message.channel.send("Please specify the auto message number to stop (e.g., 'stop 1', 'stop all').")
        return

    if command_parts[1] == 'all':
        for task in auto_message_tasks:
            task.cancel()
        auto_message_tasks = []
        await message.channel.send("All auto messages stopped.")
        return

    if len(command_parts) == 2 and command_parts[1].isdigit():
        index = int(command_parts[1]) - 1
        if index < 0 or index >= len(auto_message_tasks):
            await message.channel.send(f"Invalid auto message number. Please specify a valid auto message number (1-{len(auto_message_tasks)}).")
            return

        task = auto_message_tasks[index]
        task.cancel()
        auto_message_tasks.remove(task)
        task.cancel()
        auto_message_tasks.remove(task)
        await message.channel.send(f"Auto message {index + 1} stopped.")
        return

    await message.channel.send("Invalid command. Please specify the auto message number to stop (e.g., 'stop 1', 'stop all').")

TOKEN = 'your_token_here'
client.run(TOKEN, bot=False)
