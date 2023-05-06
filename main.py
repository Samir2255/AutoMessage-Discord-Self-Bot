import discord
import asyncio

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

AUTHORIZED_USER_ID = YOUR_USER_ID

auto_message_task = None 

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

    elif message.content.lower() == 'stop':
        if message.author.id == AUTHORIZED_USER_ID:
            await stop_auto_message(message)

async def set_auto_message(message):
    global auto_message_task

    if auto_message_task is not None and not auto_message_task.done():
        await message.channel.send("Auto message is already running. Use `stop` to stop it first.")
        return

    # Ask the user for the delay in minutes
    await message.channel.send("Please enter the delay in minutes between each auto message:")
    
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
    await message.channel.send(f"Auto message set. I will send '{content}' every {delay} minute(s) to channel {target_channel.mention}.")
    auto_message_task = asyncio.create_task(send_auto_messages(target_channel, content, delay))

async def send_auto_messages(channel, content, delay):
    while True:
        await asyncio.sleep(delay * 60)  # Convert minutes to seconds
        await channel.send(content)

async def stop_auto_message(message):
    global auto_message_task

    if auto_message_task is None or auto_message_task.done():
        await message.channel.send("Auto message is not running.")
        return

    auto_message_task.cancel()
    try:
        await auto_message_task
    except asyncio.CancelledError:
        pass

    await message.channel.send("Auto message stopped.")

TOKEN = 'token'
client.run(TOKEN, bot=False)