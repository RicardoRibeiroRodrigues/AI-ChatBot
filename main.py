import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# To use .env files.
load_dotenv()

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError('TOKEN não encontrado!')

intents = discord.Intents().all()
intents.members = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name='Servidor de teste')
    channel = discord.utils.get(guild.text_channels, name='geral')
    await channel.send('O bot está online!')


@bot.command(help="Envia o link para o repositório contendo o código fonte do bot.")
async def source(ctx):
    await ctx.send("Link do repositório: https://github.com/RicardoRibeiroRodrigues/NLP-DiscordBot")


@bot.command(help="Envia as informações do autor do bot.")
async def author(ctx):
    embed = discord.Embed()
    embed.title = 'Autor'
    embed.description = (
        """
            [Ricardo Ribeiro Rodrigues](https://github.com/RicardoRibeiroRodrigues) - ricardorr7@al.insper.edu.br
        """
    )
    await ctx.send(embed=embed)



@bot.command(help='Responde com oi.')
async def oi(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("Oi em mensagem privada!")
    else:
        await ctx.send("Oi em servidor!")


bot.run(TOKEN)
