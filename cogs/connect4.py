#!/usr/bin/env python3
# encoding: utf-8
# © 2017 Benjamin Mintz <bmintz@protonmail.com>
#
# Using code from SourSpoon under the MIT License
# https://github.com/SourSpoon/Discord.py-Template

import discord
from discord.ext import commands

from game import Connect4Game


class Connect4:

	DIGITS = [str(digit) + '\N{combining enclosing keycap}' for digit in range(1, 8)]

	def __init__(self, bot):
		self.bot = bot
		self.games = {}

	@commands.command()
	async def play(self, ctx, player2: discord.Member):
		"""
		Play connect4 with another player
		"""
		game = Connect4Game()
		self.games[ctx.message.author] = game

		game.message = await ctx.send(str(game))

		for digit in self.DIGITS:
			await game.message.add_reaction(digit)

		def check(reaction, user):
			return user == ctx.message.author and str(reaction) in self.DIGITS

		while game.whomst_won() == game.NO_WINNER:
			reaction, user = await self.bot.wait_for(
				'reaction_add',
				check=check
			)

			await game.message.remove_reaction(reaction, user)

			# convert the reaction to a 0-indexed int and move in that column
			game.move(self.DIGITS.index(str(reaction)))

			await game.message.edit(content=str(game))
			self.games[ctx.message.author] = game

		await game.message.clear_reactions()
		await game.message.edit(content=str(game))
		await self.delete_game(ctx.message.author)

	@commands.command()
	async def leave(self, ctx):
		try:
			await game.message.edit(
				content='Player 2 won (Player 1 forfeited)'
				+ '\n'.join('\n'.split(str(game))[1:]) # all lines after 1st
			)
			await self.delete_game(ctx.message.author)
		except KeyError:
			await ctx.send("You don't have a game to leave!")

	async def delete_game(self, author):
		del self.games[author]


def setup(bot):
	bot.add_cog(Connect4(bot))