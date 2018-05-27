import discord
from discord.ext import commands
import os.path
import os
import datetime
import random
from dateutil.relativedelta import relativedelta
import datetime

#https://discordapp.com/oauth2/authorize?&client_id=404097887585304586&scope=bot&

description = '''Hi, I'm the Karma bot!'''
bot = commands.Bot(command_prefix='.', description=description)
bot.remove_command('help')

s = discord.Server

@bot.event
async def on_message(message):

    if (message.author == bot.user):
        return
    
    massage = "I"
    
    if ("thank" in message.content.lower() and "@" in message.content.lower()):
        #print(str(message.content))
        old,kar = message.content.split("@")
        karma,other = kar.split(">")
        karma = karma.replace("!", "")
        rec_name = "<@" + karma + ">"

        if (message.author.id == karma):
            await bot.send_message(message.channel, "Hey now, you can't give karma to yourself.")
            return  
        
        if (os.path.exists("karma_"+str(karma)+".txt") == True):
            rec_file = open("karma_"+str(karma)+".txt", "r")
            rcoins = rec_file.readline()
            rcoins = int(str(rcoins).rstrip())
            rec_file.close()
            
            rec_file = open("karma_"+str(karma)+".txt", "w")
            rec_file.write(str(rcoins+1)+"\n")
            rec_file.close()
        
        if (os.path.exists("karma_"+str(karma)+".txt") == False):
            rec_file = open("karma_"+str(karma)+".txt", "w+")
            rec_file.write(str("1")+"\n")
            rec_file.close()
            
        #helpmen_file = open("hm-file.txt", "w")
        with open("hm-list.txt") as f:
            helpmen_list = f.readlines()
            helpmen_list = [x.strip() for x in helpmen_list]
            
        for i in helpmen_list:
            tfile = open("karma_"+str(i)+".txt", "w+")
            tfile.write("0")
            tfile.close()

        name = str(message.author.nick)

        if (name=="None"):
            name = '{0.name}'.format(message.author)
        massage = str(rec_name) + "'s karma <:upvote:334103035641069568> by 1!"
            
        await bot.send_message(message.channel, massage)
        #await bot.add_reaction('upvote:274492025678856192')
           
    await bot.process_commands(message)
    
@bot.event
async def on_ready():
    print('Logged in as')
    print("karma bot")
    print(bot.user.id)
    print('------')
    chn = bot.get_channel("376573686968221701")
    await bot.send_message(chn, "Reset complete :D")

@bot.command(pass_context = True)
async def help(ctx):
    embed = discord.Embed(title="help ", description="        This Command shows you commands for me", color=0x7abae8)
    embed.add_field(name="view_karma ", value="        Shows you how much karma you have.", inline=False)
    embed.add_field(name="view_all_karma ", value="        Shows you the collective karma of everyone", inline=False)
    embed.add_field(name="take_karma <member> ", value="        Takes 1 karma from a user", inline=False)
    embed.add_field(name="set_karma <member> <amount>", value="        Resets the karma of a user to the desired amount", inline=False)
    await bot.send_message(ctx.message.channel, embed=embed)
    #await bot.say(embed=embed)

@bot.command(pass_context = True)
async def view_all_karma(ctx):
    files = []
    coins = 0
        
    list_of_files = os.listdir(os.getcwd()) #list of files in the current directory
    for each_file in list_of_files:
        if each_file.startswith('karma_'):
            files.append(each_file)
    for x in files:
        my_file = open(x, "r+")
        tcoins = my_file.readline()
        coins += int(tcoins.rstrip())
        my_file.close()
    await bot.say("There is " + str(coins) + " karma that exists.")
     
@bot.command(pass_context = True)
async def view_highest_karma(ctx):
    files = []
    highest_karma = 0
    highest_id = ""

    if ("staff" in [y.name.lower() for y in ctx.message.author.roles]):    
        list_of_files = os.listdir(os.getcwd()) #list of files in the current directory
        for each_file in list_of_files:
            if each_file.startswith('karma_'):
                files.append(each_file)
        for x in files:
            my_file = open(x, "r+")
            tcoins = my_file.readline()
            tcoins = int(tcoins)
            if (tcoins > highest_karma):
                highest_karma = tcoins
                highest_id = x
            my_file.close()
            highest_id = highest_id.replace("karma_","")
            highest_id = highest_id.replace(".txt","")
            highid = "<@"+highest_id+">"
        await bot.say(highid + " has the most karma out of everyone, with an outstanding " + str(highest_karma) + " karma!")
        return
    await bot.say("I'm sorry, you don't have permission to use this.")
    return

@bot.command(pass_context = True)
async def view_top10_karma(ctx):
    files = []
    highest_karma = 0
    highest_id = ""
    i = 0
    big_karma = ""

    if ("staff" in [y.name.lower() for y in ctx.message.author.roles]):    
        list_of_files = os.listdir(os.getcwd()) #list of files in the current directory
        for each_file in list_of_files:
            if each_file.startswith('karma_'):
                files.append(each_file)
        for i in range(10):
            highest_karma = 0
            highest_id = ""
            for x in files:
                my_file = open(x, "r+")
                tcoins = my_file.readline()
                tcoins = int(tcoins)
                if (tcoins > highest_karma):
                    highest_karma = tcoins
                    highest_id = x
                my_file.close()
                highest_id = highest_id.replace("karma_","")
                highest_id = highest_id.replace(".txt","")
                highid = "<@"+highest_id+">"
            i += 1
            xid = "karma_"+highest_id + ".txt"
            print(xid)
            files.remove(xid)
            big_karma += highid + " - Karma " + str(highest_karma) + "\n"
            #return
        await bot.say(big_karma)
        return
    await bot.say("I'm sorry, you don't have permission to use this.")
    return

@bot.command(pass_context=True)
async def view_karma(ctx, name : discord.Member = None):
    giver = str(ctx.message.author.id)
    
    giver = giver.replace("@", "")
    giver = giver.replace("!", "")
    giver = giver.replace("<", "")
    giver = giver.replace(">", "")
    
    if (os.path.exists("karma_"+str(giver)+".txt") == True):
        giv_file = open("karma_"+giver+".txt", "r+")
        gcoins = giv_file.readline()
        gcoins = int(gcoins.rstrip())
        giv_file.close()
        
    if (os.path.exists("karma_"+str(giver)+".txt") == False):
        giv_file = open("karma_"+str(giver)+".txt", "w+")
        giv_file.write(str("0")+"\n")
        giv_file.close()
        gcoins = 0
        
    #print(name + " has " + str(gcoins) + " coins.")
    await bot.say("You have " + str(gcoins) + " karma.")
      
@bot.command(pass_context = True)
async def take_karma(ctx, user : str):
    user = user.replace("@", "")
    user = user.replace("!", "")
    user = user.replace("<", "")
    user = user.replace(">", "")
    if ("staff" in [y.name.lower() for y in ctx.message.author.roles]):
        if (os.path.exists("karma_"+str(user)+".txt") == True):
            giv_file = open("karma_"+user+".txt", "r+")
            gcoins = giv_file.readline()
            gcoins = int(gcoins.rstrip())
            giv_file.close()
        if (gcoins-1 > -1):
            giv_file = open("karma_"+user+".txt", "w")
            giv_file.write(str(gcoins-1)+"\n")
            giv_file.close()
        await bot.say("Karma removed from user.")
        return
    await bot.say("I'm sorry, you don't have permission to use this.")
    return

@bot.command(pass_context = True)
async def set_karma(ctx, user : str, amount : int):
    user = user.replace("@", "")
    user = user.replace("!", "")
    user = user.replace("<", "")
    user = user.replace(">", "")
    if ("staff" in [y.name.lower() for y in ctx.message.author.roles]):
        giv_file = open("karma_"+str(user)+".txt", "w+")
        giv_file.write(str(amount)+"\n")
        giv_file.close()
        await bot.say("User's karma set to " + str(amount) + ".")
        return
    await bot.say("I'm sorry, you don't have permission to use this.")
    return

@bot.command(pass_context = True)
async def sayinchannel(ctx, roomid: str, *, msg_str: str):

    chn = bot.get_channel(roomid)
    
    id = str(ctx.message.author.id)
    
    if (id == "173850040568119296"):

        #await bot.delete_message(ctx.message)
        await bot.send_message(chn, msg_str)
        
    if (id != "173850040568119296"):
        await bot.say("Hey now, you can't use that")

@bot.command()
async def playing(*, mygame : str):
    await bot.change_presence(game=discord.Game(name=str(mygame)))

@bot.command(pass_context = True)
async def reset(ctx):
    id = str(ctx.message.author.id)
    
    if (id == "173850040568119296"):

        #await bot.delete_message(ctx.message)
        await bot.say("Resetting :D")
        exit()
        
    if (id != "173850040568119296"):
        await bot.say("Hey now, you can't use that")

bot.run(os.environ['BOT_TOKEN'])
