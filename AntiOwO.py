# https://discordapp.com/oauth2/authorize?client_id=664602312261500947&scope=bot&permissions=8

import discord, asyncio
from colr import color
from emoji import demojize

UwUTerms = ["uwu", "owo"] # add more UwU terms
UwUUsers = {
	408785106942164992: "Default OwO bot"
}

TOKEN = "no lol"
client = discord.AutoShardedClient()


def detectUwU(m):
	m = m.replace(" ", "")

	for synonym in UwUTerms:
		if synonym in m.lower():
			# return the exact capsulation of the phrase used
			index = m.lower().index(synonym)
			return m[index:index+len(synonym)]

	return False

async def action(message):
	# for the bot to not reply to itself
	if message is None or message.author == client.user:
		return None


	# message contains an UwU
	if UwUVariant := detectUwU(message.content):
		try:
			await message.delete()
			reply = "Successfully terminated the '{0}' :white_check_mark:".format(UwUVariant)
		except:
			reply = "'{0}' detected, please grant permission to terminate...".format(UwUVariant)

	# message is from a blacklisted user
	if message.author.id in UwUUsers or detectUwU(message.author.name):
		try:
			await message.delete()
			reply = "Successfully terminated message from a known perpetrator :white_check_mark:"
		except:
			pass#reply = "Perpetrator detected, please grant permission to terminate...".format(UwUVariant)




	if "reply" in locals():
		try:
			# reply in the same text chat
			await message.channel.send(reply)
			print("{0}:{1}:{2}: {3} -> {4}".format(
				color(message.channel.guild.name, fore="salmon"), 
				color(message.channel.name, fore="red"), 
				color(message.author.name, fore="salmon"), 
				message.content, 
				color(reply, fore="green")))
		except:
			try:
				print("Failed to send messages in {0}".format(color(message.channel.guild.name, fore="red")))
			except Exception as e:
				print(color("Failed to fail: "+str(e), fore="red"))



@client.event
async def on_message_edit(before, after):
	return await action(after)

@client.event
async def on_message(message):
	return await action(message)




@client.event
async def on_raw_reaction_add(payload):
	if demojize(str(payload.emoji)).strip() == ":wheelchair:":
		channel = client.get_channel(payload.channel_id)
		msg = await channel.fetch_message(payload.message_id)
		try:
			await msg.delete()
			print("hippopotamus terminatus!")
		except Exception as e:
			print(e)


@client.event
async def on_ready():
	print(f"Username: {client.user.name}")
	print(f"UserID: {client.user.id}")
	print()

client.run(TOKEN)
