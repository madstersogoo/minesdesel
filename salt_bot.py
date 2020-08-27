import discord
import random
import psycopg2
from collections import Counter 
from discord.ext import commands

def convertTuple(tup):
    str = functools.reduce(operator.add, (tup))
    return str

client = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
    print('bot ready')
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('mining salt'))

@client.command()
async def useradd(ctx, *, user):
    con = psycopg2.connect(
        dbname = "discordbot",
        user = "postgres"
    )
    cur = con.cursor()
    cur.execute(f"select exists(select * from salt_miner where user_id like '{user}')")
    rows = cur.fetchone()
    print (rows[0])
    if rows[0] == False:
        print ("false")
        cur.execute(f"insert into salt_lvl (user_id, salt) values ('{user}', 100)")
        con.commit()
        cur.execute(f"insert into salt_miner (user_id, as_voted, leader, runner_up, last, author_id) values ('{user}', 0, 0, 0, 0,'{ctx.author}')")
        con.commit()
        await ctx.send(f"{user} as been added")
    else:
        print ("True")
        await ctx.send(f"{user} allready in db")
            

    cur.close()
    con.close()

@client.command()
async def vote(ctx, *,user):
    con = psycopg2.connect(
        dbname = "discordbot",
        user = "postgres"
    )
    cur = con.cursor()
    cur.execute(f"select exists(select * from salt_miner where author_id like '{ctx.author}')")
    rows = cur.fetchone()
    print (rows[0])
    if rows[0] == True:
        cur.execute(f"select as_voted from salt_miner where author_id like '{ctx.author}'")
        voted = cur.fetchone()
        print (voted[0])
        if voted != 0:
            print ("as not voted")
            cur.execute(f"update salt_miner set as_voted = 1 where author_id = '{ctx.author}'")
            con.commit()
            cur.execute(f"update salt_miner set vote = '{user}' where author_id = '{ctx.author}'")
            con.commit()
            await ctx.send(f"{ctx.author} voted")
        else:
            print ("as allready voted")
            await ctx.send(f"{ctx.author} as allready voted")
    else:
        await ctx.send(f"{ctx.author} you can't vote against this user")

    cur.close()
    con.close()


@client.command()
async def db(ctx):
    await ctx.send('db up and running')

client.run('Njc0NjAzNjUyODI0MTcwNTA5.Xjq_nA.onfX97fYQG9v1tGj8qcWfyZolao')