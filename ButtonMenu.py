
#---------------------------------------------------------------------------SETUP----------------------------------------------------------------------------------------#

### IMPORTS ###

from discord.ui import View
from discord import ui
import discord
from typing import Optional,List

### BUTTON MENU ###

class ButtonMenu(View):
    def __init__(self,pages:list,timeout:float,user:Optional[discord.Member]=None,page=0) -> None:
        super().__init__(timeout=timeout)
        self.pages = pages
        self.user = user
        self.update(page)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------------------------------#

    ### GENERAL ###

    def update(self,page:int):
        self.current_page = page
        self.children[0].disabled = page==0
        self.children[1].disabled = page==0
        self.children[-1].disabled = page==len(self.pages)-1
        self.children[-2].disabled = page==len(self.pages)-1
    
    async def get_page(self,page):
        if isinstance(page,str):
            return page,[],[]
        elif isinstance(page,discord.Embed):
            return None,[page],[]
        elif isinstance(page,discord.File):
            return None,[],[page]
        elif isinstance(page,List):
            if all(isinstance(x, discord.Embed) for x in page):
                return None, page, []
            elif all(isinstance(x, discord.File) for x in page):
                return NOne, [], page
            else:
                raise TypeError("Lists must contain either ALL embeds or ALL files, not a mix, and no other types.")
        else:
            raise TypeError("Must provide a string, embed, file, list of all embeds, or list of all files.")
    
    async def show_page(self,page:int,interaction:discord.Interaction):
        self.update(page)
        content, embeds, files = await self.get_page(self.pages[page])
        
        await interaction.response.edit_message(
            content = content,
            embeds = embeds,
            attachments = files or [],
            view = self
        )
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.user:
            if interaction.user != self.user:
                await interaction.response.send_message("You cannot interact with someone elses message.",ephemeral=True)
                return False
        return True
    
    ### BUTTONS ###
    
    @ui.button(emoji="⏪",style=discord.ButtonStyle.blurple)
    async def first_page(self,interaction,button):
        await self.show_page(0,interaction)
    
    @ui.button(emoji="⬅️",style=discord.ButtonStyle.blurple)
    async def prev_page(self,interaction,button):
        await self.show_page(self.current_page-1,interaction)
    
    #@ui.button(emoji="⏹️",style=discord.ButtonStyle.blurple)
    #async def stop_page(self,interaction,button):
        #for i in self.children:
            #i.disabled = True
        #await interaction.response.edit(view=self)
        #self.stop()
    
    @ui.button(emoji="➡️",style=discord.ButtonStyle.blurple)
    async def next_page(self,interaction,button):
        await self.show_page(self.current_page+1,interaction)
    
    @ui.button(emoji="⏩",style=discord.ButtonStyle.blurple)
    async def last_page(self,interaction,button):
        await self.show_page(len(self.pages)-1,interaction)
        