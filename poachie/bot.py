__author__ = "Drew (Orvyx)"
__version__ = "1.0.3"

import discord
import config
client = discord.Client()

@client.event
async def on_ready():
    print("Poachie Bot logged in as " + client.user.name + " #" + client.user.id)
    return

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!invite'):
        await client.send_message(message.channel, config.LINK_INVITE)
    if message.content.startswith('!rules'):
        ruleNum = 1;
        for val in config.RULES:
            await client.send_message(message.channel, str(ruleNum) + ") " + val)
            ruleNum = ruleNum + 1
    return

@client.event
async def on_voice_state_update(before, after):
    if after.voice.voice_channel == client.get_channel(config.CHANNEL_BOT):
        if str(after.nick) == 'None':
            channelName = str(after) + "\'s Channel"
        else:
            channelName = str(after.nick) + "\'s Channel"
        newChannel = await client.create_channel(after.server, channelName, type=discord.ChannelType.voice)
        await client.move_member(after, newChannel)
    if len(before.voice.voice_channel.voice_members) == 0 and not channel_exception(before.voice.voice_channel.id):
        await client.delete_channel(before.voice.voice_channel)
    return

def channel_exception(channel_id):
    if channel_id == config.CHANNEL_BOT or channel_id == config.CHANNEL_AFK:
        return True
    elif len(config.CHANNELS_EXCEPTION) > 0:
        for temp_id in config.CHANNELS_EXCEPTION:
            if channel_id == temp_id:
                return True
    return False
client.run(config.BOT_TOKEN)
