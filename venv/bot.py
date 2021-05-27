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
    driver.quit()
    return status

def get_stack(position_ID_Input):
    positionID = str(position_ID_Input)
    v3URL = 'https://app.uniswap.org/#/pool/' + positionID
    driver = webdriver.Chrome(".\Lib\site-packages\selenium\webdriver\chrome/chromedriver.exe", options=options)
    driver.get(v3URL)
    time.sleep(7)
    stack = driver.find_element_by_css_selector('sc-kpOJdX jLZfGp.css-1wpqso8').get_attribute("innerText")
    driver.quit()
    return stack


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
async def stack(ctx,arg):
    stack = get_stack(arg)
    await ctx.send(f"Dawg ur stack's at {stack} - {ctx.author.mention}")
bot.add_command(stack)



@commands.command()
async def setAlert(ctx,arg):
    await ctx.send(f"{ctx.author.mention}, I'm watching {arg}")
    start_time = time.time()
    hours = 20
    seconds = hours*60*60
    out = False

    while True:
        status = get_status(arg)
        if status == "Out of range":
           await sendOutRange(ctx,arg,status)
           out = True
        elif status == "Inactive":
            await ctx.send(f"This position is {status} - {ctx.author.mention}")
            break
        elif out == True:
            await ctx.send(f"This position is {status} - {ctx.author.mention}")
            out = False


        time.sleep(180)



        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:

            await ctx.send(f"{ctx.author.mention}, I stopped tracking position: {arg}")
            print("Finished iterating in: " + str(int(elapsed_time)) + " seconds")
            break
bot.add_command(setAlert)


async def sendOutRange(ctx,arg,status):
    response = requests.get(f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={tokenStorage.etherscanKey}")
    gas = response.json()
    await ctx.send(f"Position {arg} is {status}, current gas price: {gas['result']['ProposeGasPrice']} {ctx.author.mention}")




bot.run(tokenStorage.discToken)