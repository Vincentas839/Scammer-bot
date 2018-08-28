import asyncio
import discord
from discord.ext import commands
import random
import time
import regex
import re
import datetime
import botkey
from os import listdir
from os.path import isfile, join

description = '''This bot is built to serve as a number bot that will be able to manage numbers for scambaiting communities'''
bot = commands.Bot(command_prefix='=', description=description)
client = discord.Client()

cmd_dir = "commands"

if __name__ == "__main__":
    for extension in [f.replace('.py', '') for f in listdir(cmd_dir) if isfile(join(cmd_dir, f))]:
        try:
            bot.load_extension(cmd_dir + "." + extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()


@bot.command(pass_context=True)
async def number(ctx):
	Scamlist = open('Scamlist.lst', 'r')
	Numbers = Scamlist.read().splitlines()
	print(Numbers)
	random.seed()
	RandNum = Numbers[random.randint(0,len(Numbers-1))]
	#TODO: CHANGE TO DM
	await bot.say('{} try: {}'.format(ctx.message.author.mention,RandNum))



@bot.command(pass_context=True)
async def submit(ctx):
	number = ctx.message.content[8:]
	if len(number) == 0:
		await bot.say('No number submitted. Please add a number')
		return	
	print("{}, {}".format(len(number), number))
	if len(number) == 14:
		if re.match(r'18[0-8]{2}-[0-9]{3}-[0-9]{4}',number) == None:
			print('Error')
			await bot.say('Sorry, that number does not match our filter, if this is a scam number, please dm <@341928732602269698> to improve the filter.')
			return
		else:
			print('MATCH!')
	if len(number) == 13:
		if re.match(r'8[0-8]{2}-[0-9]{3}-[0-9]{4}',number) == None:
			print('Error')
			await bot.say('Sorry, that number does not match our filter, if this is a scam number, please dm <@341928732602269698> to improve the filter.')
			return
		else:
			print('MATCH!')
	if len(number) == 11:
		if re.match(r'18[0-8]{2}[0-9]{3}[0-9]{4}',number) == None:
			print('Error')
			await bot.say('Sorry, that number does not match our filter, if this is a scam number, please dm <@341928732602269698> to improve the filter.')
			return
		else:
			print('MATCH!')
	if len(number) == 10:
		if re.match(r'8[0-8]{2}[0-9]{7}',number) == None:
			print('Error')
			await bot.say('Sorry, that number does not match our filter, if this is a scam number, please dm <@341928732602269698> to improve the filter.')
			return
		else:
			print('MATCH!')
	print("Opening List")
	currentList = open('Scamlist.lst', 'r')
	print("Reading list")
	list = currentList.read().splitlines()
	if number in list:
		print('In DB')
		await bot.say('This number is already in our database, but thank you for contributing!')
		currentList.close()
		return
	currentList.close()
	print("Opening list in append mode")
	Scam = open('Scamlist.lst', 'a')
	print("Writing to list")
	Scam.write(number+'\n')
	await bot.say('Number written.')
	Scam.close()


@bot.command(pass_context=True)
async def report(ctx):
	return

@commands.command(pass_context=True, name="help", aliases=["Help", "HELP", "cmd", "Cmd", "CMD", "cmds", "Cmds", "CMDS", "commands", "Commands", "COMMANDS"])
@commands.cooldown(1, 10, commands.BucketType.user)
async def help(ctx):
	author = ctx.message.author
	help=discord.Embed(colour=discord.Colour(value=0xFFDFF0))
	help.add_field(name="Submit", value="Allows you to submit a number", inline=True)
	help.add_field(name="Number", value="Gives you a random number from the list", inline=True)
	help.add_field(name="Report", value="Reports a number as not working", inline=True)
	#help.add_field(name="", value="", inline=True)
	await bot.send_message(ctx.message.channel, embed=help)

import discord
from discord.ext import commands
@bot.event
async def on_command_error(error, ctx):
	author = ctx.message.author
	authorm = ctx.message.author.mention
	if isinstance(error, commands.CommandOnCooldown):
		response = await bot.send_message(ctx.message.channel, content="**:x: This command is on a %.2fs cooldown {}**".format(author) % error.retry_after)
		time.sleep(3)
		await bot.delete_message(response)
		return
	if isinstance(error, commands.CommandNotFound):
		response = await bot.send_message(ctx.message.channel, content="**:x: {} Command not found**".format(authorm))
		time.sleep(3)
		await bot.delete_message(response)
		return
	if isinstance(error, commands.MissingRequiredArgument):
		response = await bot.send_message(ctx.message.channel, content="**:x: {} Missing Arguments**".format(authorm))
		time.sleep(3)
		await bot.delete_message(response)
		return
	print(error)
	error=discord.Embed(description="**:x: Got an Error**\n```py\n{}\n```".format(error), colour=discord.Colour(value=0xff0707))
	error.add_field(name="User", value="{}".format(authorm), inline=True)
	error.add_field(name="Command+Content", value="{}".format(ctx.message.content), inline=True)
	await bot.send_message(ctx.message.channel, embed=error)
	return

@bot.event
async def on_message(message):
	server = message.server.name
	channel = message.channel.name
	await bot.process_commands(message)

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('-'*18)

bot.run(botkey.getToken())
