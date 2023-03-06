import discord
from discord.ext import commands
import os
from datetime import datetime
from dotenv import load_dotenv
from bot_lib.BotHelp import CommandsHelp
from bot_lib.ApiInterface import ApiInterface
from bot_lib.BotExceptions import *

load_dotenv()
API_KEY = os.getenv("API_KEY")
TOKEN = os.getenv("TOKEN")
if not API_KEY or not TOKEN:
    raise Exception('Environment variable not set')

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=CommandsHelp())
api_inter = ApiInterface(API_KEY)


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name='Servidor de teste')
    channel = discord.utils.get(guild.text_channels, name='geral')
    await channel.send('O bot está online!')


@commands.dm_only()
@bot.command(help="Sends a link to the github repo")
async def source(ctx):
    """
    Command that sends the link for the bot's source code on github.
    """
    embed = discord.Embed(title="Link do repositório no github")
    embed.url = "https://github.com/RicardoRibeiroRodrigues/NLP-DiscordBot"
    embed.description = "https://github.com/RicardoRibeiroRodrigues/NLP-DiscordBot"
    embed.set_image(url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
    await ctx.send(embed=embed)


@commands.dm_only()
@bot.command(help="Sends the bot author's info")
async def author(ctx):
    """
    Sends a embed with bot author's name, github profile and email.
    """
    embed = discord.Embed()
    embed.title = 'Autor'
    embed.description = (
        """
            [Ricardo Ribeiro Rodrigues](https://github.com/RicardoRibeiroRodrigues) - ricardorr7@al.insper.edu.br
        """
    )
    await ctx.send(embed=embed)

@commands.dm_only()
@bot.command(help="Command to list info on a specific cryptocurrency.")
async def run(ctx, symbol: str, interval: str=None):
    """
    This command uses the coincap API to fetch data on a specific cryptocurrency.
    The data is then to the user on a discord embed with a historical price graph and basic info on the crypto.

    Parameters:
        :symbol: The symbol of the cryptocurrency to fetch data on, must be on the crypto typical format (e.g. BTC, ETH, XRP, etc.)
        :interval: The interval of the historical price graph. This parameter is optional and defaults to the last one year.
        The format must be YYYY-MM-DD.YYYY-MM-DD, where the first date is the start date and the second is the end date, separated by a dot.
    
    **Example usage:**
        !run BTC 2020-01-01.2021-01-01
    This command will fetch data on BTC from the 1st of January 2020 to the 1st of January 2021.
    """
    embed = discord.Embed(title=f"Information on {symbol}")

    if api_inter.validate_symbol(symbol):
        first_date = None
        second_date = None
        if interval and api_inter.validate_interval(interval):
            first, second = interval.split('.')
            first_date = datetime.strptime(first, "%Y-%m-%d")
            second_date = datetime.strptime(second, "%Y-%m-%d")

            if first_date > second_date:
                first_date, second_date = second_date, first_date
        try:
            basic_info, img_path = await api_inter.fetch_data(symbol, first_date, second_date)

            market_cap_usd = f"${float(basic_info['marketCapUsd']):,.2f}"
            volume_usd = f"${float(basic_info['volumeUsd24Hr']):,.2f}"
            change = f"{float(basic_info['changePercent24Hr']):.2f} %"
            price = float(basic_info['priceUsd'])
            if price > 1:
                price = f"${price:,.3f}"
            else:
                price = f"${price:,.6f}"

            embed.add_field(name="Crypto rank", value=basic_info['rank'])
            embed.add_field(name="Price", value=price)
            embed.add_field(name="Market Cap", value=market_cap_usd, inline=False)
            embed.add_field(name="Volume in 24h", value=volume_usd)
            embed.add_field(name="Change in 24h", value=change)
            embed.set_image(url=f"attachment://{img_path}")

            await ctx.send(embed=embed, file=discord.File(img_path))
            os.remove(img_path)
        except InvalidCrypto as e:
            await ctx.send(f"{e}")
        except FetchError as e:
            await ctx.send(f"{e}")
    else:
        await ctx.send("Invalid symbol, see the usage of the command with !help run")



@bot.event
async def on_command_error(ctx, exception):
    if isinstance(exception, commands.MissingRequiredArgument):
        command_name = ctx.message.content.split(" ")[0].replace("!", "")
        await ctx.send(f"Command missing argument, please use **!help {command_name}** to see how to use it.")

    print(
        f"""Error:
            {exception}
        """
    )

bot.run(TOKEN)