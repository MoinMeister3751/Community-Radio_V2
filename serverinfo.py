import nextcord
from nextcord.ext import commands
from nextcord import ButtonStyle
from nextcord.ui import Button, View

BOT_OWNER_ID = "Your Owner ID"

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="server", description="Zeige denn Discord Link von MoinMeister3751")
    async def server(self, interaction: nextcord.Interaction):
        if interaction.user.id != BOT_OWNER_ID:
            await interaction.response.send_message("## Hier ist der [Invite-Link](https://discord.gg/pB2Zwst7qb) zu meinem Server!", ephemeral=True)
            return

        guilds = self.bot.guilds
        if not guilds:
            await interaction.response.send_message("Der Bot ist auf keinem Server.", ephemeral=True)
            return

        pages = [guilds[i:i + 20] for i in range(0, len(guilds), 20)]

        async def create_embed(page_num):
            page = pages[page_num]
            server_list = []

            for guild in page:
                owner = guild.owner.mention  
                server_list.append(f"**{guild.name}** - {guild.member_count} Mitglieder\nEigentümer: {owner}")

            description = "\n".join(server_list)
            embed = nextcord.Embed(
                title=f"Server, auf denen der Bot ist ({len(guilds)} Server) - Seite {page_num + 1}/{len(pages)}",
                description=description,
                color=nextcord.Color.blue()
            )
            return embed

        current_page = 0
        embed = await create_embed(current_page)

        async def previous_page_callback(interaction):
            nonlocal current_page
            if current_page > 0:
                current_page -= 1
                embed = await create_embed(current_page)
                await interaction.response.edit_message(embed=embed, view=view)

        async def next_page_callback(interaction):
            nonlocal current_page
            if current_page < len(pages) - 1:
                current_page += 1
                embed = await create_embed(current_page)
                await interaction.response.edit_message(embed=embed, view=view)

        previous_button = Button(label="Zurück", style=ButtonStyle.primary)
        next_button = Button(label="Weiter", style=ButtonStyle.primary)

        previous_button.callback = previous_page_callback
        next_button.callback = next_page_callback

        view = View()
        view.add_item(previous_button)
        view.add_item(next_button)

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

def setup(bot):
    bot.add_cog(ServerInfo(bot))
