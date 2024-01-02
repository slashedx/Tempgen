import os
import random
import time
import requests
import discord

from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

driver = webdriver.Edge()
driver.get('https://roblox.com/')

def gen_password():  
    
   lower = "abcdefghijklmnopqrstuvwxyz"
   specialcharacters = "0123456789%#$@&"
   length = random.randint(10,15)
   
   password = "".join(random.sample(lower + specialcharacters, length)) 
   
   return password

def genfunc(username: str, password: str):
    
    driver.get("https://roblox.com/signup")

    BirthdayMonthChosen = driver.find_element(By.XPATH, f'//*[@id="MonthDropdown"]/option[{random.randint(2, 13)}]')
    BirthdayMonthChosen.click()
    
    BirthdayDayChosen = driver.find_element(By.XPATH, f'//*[@id="signup"]/div/div/div[1]/div[1]/div/div[1]/div[2]/select/option[{random.randint(2, 28)}]')
    BirthdayDayChosen.click()

    BirthdayYearChosen = driver.find_element(By.XPATH, f'//*[@id="YearDropdown"]/option[{random.randint(25,101)}]')
    BirthdayYearChosen.click()
    
    UsernameInput = driver.find_element(By.XPATH, '//*[@id="signup-username"]')
    UsernameInput.send_keys(username)
    
    PasswordInput = driver.find_element(By.XPATH, '//*[@id="signup-password"]')
    PasswordInput.send_keys(password)

    FemaleButton = driver.find_element(By.XPATH, '//*[@id="FemaleButton"]')
    MaleButton = driver.find_element(By.XPATH, '//*[@id="MaleButton"]')

    ChoiceGender = random.randint(0,2)

    if ChoiceGender == 1:
        FemaleButton.click()
    elif ChoiceGender == 2:
        MaleButton.click()

    SumitButton = driver.find_element(By.XPATH, '//*[@id="signup-button"]')
    SumitButton.click()

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="FunCaptcha"]')))
        WebDriverWait(driver, 100).until_not(EC.presence_of_element_located((By.XPATH, '//*[@id="FunCaptcha"]')))
    except TimeoutException:
        pass

    with open('accounts.txt', 'a') as file:
        file.write("{}:{}\n".format(username, password))
        file.close()

    with open('cookies.txt', 'a') as file:

        cookie = str(driver.get_cookie('.ROBLOSECURITY')["value"])

        file.write(cookie+"\n")
        file.close()
    
    driver.delete_cookie('.ROBLOSECURITY')
    driver.get('https://www.roblox.com/')

# account gen commands

@bot.command()
async def gen(ctx, username: str):
  
    requestlink = f"https://auth.roblox.com/v2/usernames/validate?request.username={username}&request.birthday=2000-01-01&request.context=Signup"
    robloxdata = requests.get(requestlink).json()
    valid = robloxdata['message']
    if ctx.channel.id == 1183603161278193725: # replace 123 with your channel id  
      if username:

        password = gen_password()

        if valid == 'Username is valid':
            
            GenningEmbed = discord.Embed(title="Vaild", description="This username is vaild so genning...", color=discord.Color.brand_green())

            await ctx.reply(embed=GenningEmbed)
            
            genfunc(password=password, username=username)

            DetailsEmbed = discord.Embed(title="Account Genned", description="", color=discord.Color.brand_green())
            DetailsEmbed.add_field(name="Username", value=f"||{username}||")
            DetailsEmbed.add_field(name="Password", value=f"||{password}||")
            
            await ctx.author.send(embed=DetailsEmbed)
        
        else:
            FailedToGenEmbed = discord.Embed(title="Failled Genning", description="This username is alreay taken or inappropriate for roblox.", color=discord.Color.brand_red())
            await ctx.reply(embed=FailedToGenEmbed)
    else:
        WrongChannelEmbed = discord.Embed(title="Wrong Channel", description="This command only works in <#1181079609375195176>!", color=discord.Color.brand_red())
        await ctx.reply(embed=WrongChannelEmbed)

@bot.command()
async def check(ctx, username: str):
    requestlink = f"https://auth.roblox.com/v2/usernames/validate?request.username={username}&request.birthday=2000-01-01&request.context=Signup"
    robloxdata = requests.get(requestlink).json()
    valid = robloxdata['message']

    if valid == 'Username is valid':
        vaildembed = discord.Embed(title="This Username Is Vaild", description="", color=discord.Color.brand_green())
        await ctx.reply(embed=vaildembed)
    else:
        notvaild = discord.Embed(title="This username is alreay taken or inappropriate for roblox.", description="", color=discord.Color.brand_red())
        await ctx.reply(embed=notvaild)
        
bot.run("YOUR_BOT_TOKEN")
