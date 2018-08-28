import discord
from discord.ext import commands
@commands.command(pass_context=True)
async def stop(ctx):
	authorN = ctx.message.author
	id = authorN.id
	if int(id) == 341928732602269698:
		try:
			await bot.say('Alright! See ya!')
			await bot.close()
		except Exception as e:
			await bot.say('OOF ```{}```'.format(e))
	else:
		await bot.say("No. You do not have permission to stop me {0.mention}.".format(ctx.message.author))
		print("SOMEONE TRIED TO USE A FORBIDDEN COMMAND!!! {0.name} attempted to stop me in {0.server}!".format(ctx.message.author))
