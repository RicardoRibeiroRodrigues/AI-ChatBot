import discord
from discord.ext import commands
import os
from datetime import datetime
from dotenv import load_dotenv
from bot_lib.BotHelp import CommandsHelp
from bot_lib.ApiInterface import ApiInterface
from bot_lib.scrapper import Scrapper
from bot_lib.NlpTools import NlpTools
from bot_lib.BotExceptions import *

load_dotenv()
API_KEY = os.getenv("API_KEY")
TOKEN = os.getenv("TOKEN")
if not API_KEY or not TOKEN:
    raise Exception('Environment variable not set')

N_RESULTS_SEARCH = 12
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=CommandsHelp())
api_inter = ApiInterface(API_KEY)
scrapper = Scrapper(max_downloads=25)
nlp_tools = NlpTools()


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name='Servidor de teste')
    channel = discord.utils.get(guild.text_channels, name='geral')
    await channel.send('O bot está online!')


@commands.dm_only()
@bot.command(help="Sends a link to the github repo", usage="!source")
async def source(ctx):
    """
    Command that sends the link for the bot's source code on github.
    This command is DM only.
    """
    embed = discord.Embed(title="Link do repositório no github")
    embed.url = "https://github.com/RicardoRibeiroRodrigues/NLP-DiscordBot"
    embed.description = "https://github.com/RicardoRibeiroRodrigues/NLP-DiscordBot"
    embed.set_image(url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
    await ctx.send(embed=embed)


@commands.dm_only()
@bot.command(help="Sends the bot author's info", usage="!author")
async def author(ctx):
    """
    Sends a embed with bot author's name, github profile and email.
    This command is DM only.
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
@bot.command(help="Command to list info on a specific cryptocurrency.", usage="!run BTC 2020-01-01.2021-01-01")
async def run(ctx, symbol: str, interval: str=None):
    """
    This command uses the **coincap API** to fetch data on a specific cryptocurrency.
    The data is then to the user on a discord embed with a historical price graph and basic info on the crypto.
    This command is DM only.

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
            async with ctx.typing():
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
            embed = discord.Embed(title=e)
            valid_crypto_str = ", ".join(e.get_valid_cryptos())
            embed.add_field(name="Valid cryptos:", value=valid_crypto_str)
            await ctx.send(embed=embed)
        except FetchError as e:
            await ctx.send(f"{e}")
    else:
        await ctx.send("Invalid symbol, see the usage of the command with !help run")

@commands.dm_only()
@bot.command(help="Command to crawl internet and save the content of a site in the database", usage="!crawl <url>")
async def crawl(ctx, url: str):
    """
    This command receives a url and fetches the content of the page.
    The content is then processed and saved in the database.
    This command is DM only.

    Parameters:
        :url: The url of the page to be crawled.
    
    **Example usage:**
        !crawl https://github.com/tiagoft/NLP/blob/main/APS.md
    """
    if scrapper.url_in_db(url):
        await ctx.send("This url has already been added to the database")
        return

    contents = [] 
    async for title, content in scrapper.scrape(url):
        await ctx.send(f"Content of <{title}> fetched!")
        contents.append(content)
    nlp_tools.fit_transform(scrapper.contents)
    for content in contents:
        nlp_tools.add_document(content)
    await ctx.send(f"Finished crawling, crawled {len(contents)} pages!")
    


@commands.dm_only()
@bot.command(help="Command to search for a specific word in the database", usage="!search <query>")
async def search(ctx, *query):
    """
    This command receives a query and searches for it in the database.
    Returns the documents where the query was found.
    This command is DM only.

    Parameters:
        :query: The query to be searched.
    
    **Example usage:**
        !search cloud computing 
    """
    docs = nlp_tools.search(" ".join(query))
    if not docs:
        await ctx.send(f"The query {query} was not found in the database, please try another query or try using wn_search.")
        return

    embed = discord.Embed(title=f"Best matches for {' '.join(query)}")
    docs = sorted(docs, key=lambda x: docs[x], reverse=True)

    for i, doc in enumerate(docs):
        if i >= N_RESULTS_SEARCH:
            break
        embed.add_field(name=f"{scrapper.titles[int(doc)]}", value=scrapper.urls[int(doc)])
    await ctx.send(embed=embed)
    

@commands.dm_only()
@bot.command(help="Command to search for a term using wordnet", usage="!wnsearch <word>")
async def wn_search(ctx, word: str):
    """
    This receives a word and searches for it in the database, using the wup_similarity for searching for similar terms.
    Returns the most similar term and the document where it was found.
    This command is DM only.

    Parameters:
        :word: The word to be searched.
    
    **Example usage:**
        !wnsearch pc
    """
    match, docs = nlp_tools.wn_search(word)
    if not match or not docs:
        await ctx.send(f"The word {word} was not found in the wordnet, please try another word.")
        return
    
    embed = discord.Embed(title=f"Found matches for {match}")
    docs = sorted(docs, key=lambda x: docs[x], reverse=True)

    for i, doc in enumerate(docs):
        if i >= N_RESULTS_SEARCH:
            break
        embed.add_field(name=f"Document {scrapper.titles[int(doc)]}", value=scrapper.urls[int(doc)])
    await ctx.send(embed=embed)


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