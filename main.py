import discord
import asyncio
import json

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

AUTHORIZED_USER_ID = YOUR_USER_ID

auto_message_tasks = []
MAX_AUTO_MESSAGES = 3

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')

@client.event
async def on_message(message):
    if message.content.startswith('!set_auto_message'):
        await set_auto_message(message)
    elif message.content.startswith('stop'):
        await stop_auto_message(message)
    else:
        await process_command(message)

async def set_auto_message(message):
    if message.author.id != AUTHORIZED_USER_ID:
        return

    if len(auto_message_tasks) >= MAX_AUTO_MESSAGES:
        await message.channel.send(f"You have reached the maximum limit of {MAX_AUTO_MESSAGES} auto messages.")
        return

    await message.channel.send("Please enter the delay in seconds between each auto message:")

    def check(m):
        return m.author == message.author and m.channel == message.channel

    delay_msg = await client.wait_for('message', check=check)
    delay = int(delay_msg.content)

    await message.channel.send("Please enter the content of the auto message:")
    content_msg = await client.wait_for('message', check=check)
    content = content_msg.content

    await message.channel.send("Please enter the channel ID where the bot should send messages:")
    channel_id_msg = await client.wait_for('message', check=check)
    channel_id = int(channel_id_msg.content)

    target_channel = client.get_channel(channel_id)
    if target_channel is None:
        await message.channel.send(f"Invalid channel ID. Please make sure the bot has access to the specified channel.")
        return

    await message.channel.send(
        f"Auto message set. I will send '{content}' every {delay} second(s) to channel {target_channel.mention}.")
    task = asyncio.create_task(send_auto_messages(target_channel, content, delay))
    auto_message_tasks.append(task)

async def send_auto_messages(channel, content, delay):
    while True:
        try:
            await asyncio.sleep(delay)
            await channel.send(content)
        except asyncio.CancelledError:
            break

async def stop_auto_message(message):
    if message.author.id != AUTHORIZED_USER_ID:
        return
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
        await task.cancel()
        auto_message_tasks.remove(task)
        await message.channel.send(f"Auto message {index + 1} stopped.")
        return

    await message.channel.send("Invalid command. Please specify the auto message number to stop (e.g., 'stop 1', 'stop all').")

async def process_command(message):
    if message.author.id == AUTHORIZED_USER_ID:
        command = message.content.lower()

        if command in config:
            response = config[command]
            await message.channel.send(response)

TOKEN = 'YOUR TOKEN'
client.run(TOKEN, bot=False)