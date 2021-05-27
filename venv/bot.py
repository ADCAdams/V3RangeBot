import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time




#executable_path="C:\chromedriver.exe"

def get_status(position_ID_Input):
    positionID = str(position_ID_Input)
    v3URL = 'https://app.uniswap.org/#/pool/' + positionID
    driver = webdriver.Chrome(".\Lib\site-packages\selenium\webdriver\chrome/chromedriver.exe")
    driver.get(v3URL)
    time.sleep(7)

    status = driver.find_element_by_css_selector('div.sc-1bdyhrg-1.tbzPF').get_attribute("innerText")
    print(status)
    driver.quit()
    return status


bot = commands.Bot(command_prefix='-')

@commands.command()
async def test(ctx, *, arg):
    await ctx.send(arg)
bot.add_command(test)

@commands.command()
async def v3Status(ctx,arg):
    status = get_status(arg)
    await ctx.send(status)
    await ctx.send(f"{ctx.author.mention}")
bot.add_command(v3Status)

# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))
#
#
#     # guilds = client.guilds
#     # print("*******************guild is: ")
#     # print(guilds)
#     #
#     # v3Channel = await guilds[0].create_text_channel('v3Status')
#     # await v3Channel.send("new channel1")
#
#
#     # if status == "Out of range":
#     #     .send(status)
#     # else:
#     #     message.channel.send("HunkyDory :)))")
#
#
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('$hello'):
#         await message.channel.send(status)



bot.run('ODQ2NzUzNjQ4NTkxMzcyMzA4.YK0GyQ.m0jNKF6EcVrDL_i_BFQ5_iJNvjg')