import discord
from discord.ext import commands


class CommandsHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        """Override the default behavior for displaying the bot's help message"""

        # Command is DM only!
        if not isinstance(self.get_destination(), discord.DMChannel):
            return

        # Create a new embed to display the help message
        embed = discord.Embed(title="Help", description="List of available commands:")

        # Iterate over each cog and command in the bot's command tree
        for commands in mapping.values():

            # Add a field to the embed for each command in the category
            for command in commands:
                if command.name != "help":
                    embed.add_field(
                        name=command.name, value=command.usage, inline=False
                    )

        embed.add_field(
            name="Help on a specific command",
            value="Use !help <command> to get more info on a specific command",
            inline=False,
        )
        # Send the embed to the user
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        """Override the default behavior for displaying detailed help for a command"""

        # Command is DM only!
        if not isinstance(self.get_destination(), discord.DMChannel):
            return

        # Create a new embed to display the detailed help message
        embed = discord.Embed(
            title=f"Help for command: {command.name}", description=command.help
        )
        # Add a field to the embed for the command's usage and parameters

        # Add a field to the embed for the command's brief description
        func_docstring = command.callback.__doc__
        if func_docstring:
            embed.add_field(name="Description", value=func_docstring, inline=False)

        # Add a field to the embed for the command's detailed description
        if command.description:
            embed.add_field(name="Details", value=command.description, inline=False)

        usage = f"{command.signature}"
        embed.add_field(name="Usage", value=usage, inline=False)

        # Send the embed to the user
        await self.get_destination().send(embed=embed)
