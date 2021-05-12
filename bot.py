import discord

from queue import Queue
import random
import os

TOKEN =     os.getenv('TOKEN')
P =         '$'
QUEUE_P =   '-p '
EMOTES =    ['🐈', '🐱', '😼', '😺', '😸', '😻', '🐅']

def random_emote():
    return random.choice(EMOTES)

class QueQue(discord.Client):
    queue = Queue()

    async def cmd_handler(self, message, cmd, args = None):        
        if cmd == f'{P}q' and \
                args is not None and \
                not self.queue.full():
            await message.add_reaction(random_emote())
            final_item = f'{QUEUE_P}{args}'
            self.queue.put(final_item)

        if cmd == f'{P}dq' and \
                not self.queue.empty():
            await message.add_reaction(random_emote())
            channel = message.channel
            while not self.queue.empty():
                item = self.queue.get()
                await channel.send(item)

    async def on_message(self, message):
        content = message.content
        if ' ' in content:
            (cmd, args) = content.split(' ', 1)
            await self.cmd_handler(message, cmd, args)
        else:
            await self.cmd_handler(message, content)

client = QueQue()
client.run(TOKEN)