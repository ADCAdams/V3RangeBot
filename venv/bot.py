import discord
import tokenStorage
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time



options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')


def get_status(position_ID_Input):
    positionID = str(position_ID_Input)
    v3URL = 'https://app.uniswap.org/#/pool/' + positionID
    driver = webdriver.Chrome(".\Lib\site-packages\selenium\webdriver\chrome/chromedriver.exe", options=options)
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

@commands.command()
async def setAlert(ctx,arg):
    await ctx.send(f"{ctx.author.mention}, I'm watching {arg}")
    start_time = time.time()
    hours = 20
    seconds = hours*60

    while True:
        status = get_status(arg)
        if status == "Out of range":
            await ctx.send(f"{status} {ctx.author.mention}")

        time.sleep(180)

        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            await ctx.send(f"{ctx.author.mention}, I stopped tracking position: {arg}")
            print("Finished iterating in: " + str(int(elapsed_time)) + " seconds")
            break
bot.add_command(setAlert)



bot.run(tokenStorage.discToken)