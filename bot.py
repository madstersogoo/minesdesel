import discord
import random
from collections import Counter 
from discord.ext import commands

client = commands.Bot(command_prefix = "!")

userlist = []
votelist = []
memberlist = []
count = 1
salt = 100

with open('userlist.txt', 'r') as file:
    userlist = [line.strip() for line in file]

with open('vote.txt', 'r') as file:
    votelist = [line.strip() for line in file]

with open('member.txt', 'r') as file:
    memberlist = [line.strip() for line in file]


@client.event
async def on_ready():
    print('bot ready')
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('mining salt'))



@client.command(aliases=['votes'])
async def vote(ctx, *, user):
    if (ctx.author) in memberlist:
        index = memberlist.index(ctx.author)
        memberlist.pop(index)
        votelist.pop(index)
        await ctx.send(f"Et bim ! %s prend un vote" % user)
        votelist.append(user)
        memberlist.append(ctx.author)
        with open('vote.txt', 'w') as f:
            for item in votelist:
                f.write("%s\n" % item)
        with open('member.txt', 'w') as f:
            for item in memberlist:
                f.write("%s\n" % item)
    else :
        if (user) in userlist:
                await ctx.send(f"Et bim ! %s prend un vote" % user)
                votelist.append(user)
                memberlist.append(ctx.author)
                with open('vote.txt', 'w') as f:
                    for item in votelist:
                        f.write("%s\n" % item)
                with open('member.txt', 'w') as f:
                    for item in memberlist:
                        f.write("%s\n" % item)
                print (votelist)
        else :
                    await ctx.send(f"you can't vote against this user")
                

@client.command()
async def db(ctx):
    await ctx.send('db up and running')

@client.command()
async def leaderboard(ctx):
    vote = dict(Counter(votelist))
    await ctx.send(vote)
    print (vote)

@client.command()
async def useradd(ctx, *, user):
    if (user) in userlist:
        await ctx.send('user allready in db')
    else :
        userlist.append(user)
        await ctx.send(f'user: {user} added ')
        with open('userlist.txt', 'w') as f:
            for item in userlist:
                f.write("%s\n" % item)
    print('useradd')
    print(userlist)

@client.command()
async def userslist(ctx):
    await ctx.send(userlist)
    print (userlist)

@client.command()
async def loubier(ctx):
    await ctx.send(f'@everyone fuck le francais')

@client.command()
async def salt(ctx):
    await ctx.send(f'100')



client.run('')
