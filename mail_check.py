#!/usr/bin/env python
from praw.models import Message
import praw
import subprocess
import time
import os
import config

#daemon core
core = "/home/RonTipsProject/ronpaulcoind"

# bot configuration
apikey = '03LhM59M6BF4pg'
secretkey = 'wN9lCCQla2DRvkQZ60jX0-ImGEY'
botname = 'RonTips4Liberty'
bot_pw = 'Serbialovescrypto2019!'
bot_agent = 'bot by vladan'
# subreddit_name = 'RonTips4Liberty'
mail_log_file = 'mail_log.txt' # log file for mail_check

# look for phrase and reply appropriately
def bot_login():
    print "Logging in..."
    reddit = praw.Reddit(client_id=apikey,
        client_secret=secretkey,
        username=botname,
        password=bot_pw,
        user_agent=bot_agent)
    print "Logged in!"
    return reddit

def run_bot(reddit):
    with open(mail_log_file, "a") as logfile:
        logfile.write("Searching unread messages\n")
        unread_messages = []
        for item in reddit.inbox.unread(limit=None):
            if isinstance(item, Message):
                unread_messages.append(item)
                print item.body
                logfile.write("command message: {0}".format(item.body).encode('utf-8'))
                accountStr = "reddit-{0}".format(item.author.name.lower())
                logfile.write("wallet accountname: {0}".format(accountStr))
                if 'balance' in item.body.lower():
                    if len(item.body.split())==1:
                        # get balance data by running daemon ronpaulcoind
                        balance = subprocess.check_output([core,"getbalance", accountStr])[:-1]
                        reddit.redditor(item.author.name).message('Balance', 'Your balance is {0} RPC'.format(balance))
                        logfile.write('Your balance is {0}RPC\n'.format(balance))
                    else:
                        reddit.redditor(item.author.name).message('Balance error', 'Usage in PM: `balance`')
                        logfile.write('Balance error: \nUsage in PM: `balance`\n')
                elif 'deposit' in item.body.lower():
                    if len(item.body.split())==1:
                        deposit = subprocess.check_output([core,"getaccountaddress", accountStr])[:-1]
                        reddit.redditor(item.author.name).message('Deposit', "Your Ron Paul Coin depositing address is: {0}".format(deposit))
                        logfile.write('Deposit\nYour Ron Paul Coin depositing address is: {0}'.format(deposit))
                    else:
                        reddit.redditor(item.author.name).message('Deposit error', "To deposit your Ron Paul Coin please PM the following: deposit")
                        logfile.write('Deposit error\nUsage in PM: `deposit`')
                elif 'withdraw' in item.body.lower():
                    if len(item.body.split())==3:
                        try:
                            amount = float(item.body.split()[1])
                            address = item.body.split()[2]
                            # accountStr = 'reddit-{0}'.format(item.author.name)
                            balance = float(subprocess.check_output([core,"getbalance", accountStr])[:-1])
                            if balance < amount:
                                reddit.redditor(item.author.name).message('Withdraw error', "You have insufficent funds.")
                                logfile.write('Withdraw error\nYou have insufficent funds.')
                            else:
                                amount = str(amount)
                                # sendfrom <fromaccount> <toronpaulcoinaddress> <amount> [minconf=1] [comment] [comment-to]
                                tx = subprocess.check_output([core,"sendfrom",accountStr,address,amount])[:-1]
                                # {0} has successfully withdrew to address: {1} of {2} RDD"
                                reddit.redditor(item.author.name).message('Withdraw success', "You have successfully withdrawn {0} RPC to address: {1}".format(amount,address))
                                logfile.write('Withdraw success\nYou have successfully withdrawn {0} RPC to address: {1}'.format(amount,address))
                        except ValueError:
                            reddit.redditor(item.author.name).message('Withdraw error', 'To withdraw your Ron Paul Coin please PM the following: withdraw <amount> <address>')
                            logfile.write('Withdraw error\nTo withdraw your Ron Paul Coin please PM the following: withdraw <amount> <address>')
                    else:
                        reddit.redditor(item.author.name).message('Withdraw error', 'To withdraw your Ron Paul Coin please PM the following: withdraw <amount> <address>')
                        logfile.write('Withdraw error\nTo withdraw your Ron Paul Coin please PM the following: withdraw <amount> <address>')
    reddit.inbox.mark_read(unread_messages)
    reddit.inbox.collapse(unread_messages)
    time.sleep(10)

reddit = bot_login()

unread_messages = []
while True:
    run_bot(reddit)
    pass