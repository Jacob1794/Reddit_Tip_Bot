#!/usr/bin/env python
import praw
import subprocess
import time
import os
import config
# import requests

#daemon core
core = "/home/RonTipsProject/ronpaulcoind"

# bot configuration
apikey = '03LhM59M6BF4pg'
secretkey = 'wN9lCCQla2DRvkQZ60jX0-ImGEY'
botname = 'RonTips4Liberty'
bot_pw = 'Serbialovescrypto2019!'
bot_agent = 'bot by vladan'
# subreddit_name = 'RonTips4Liberty'

subreddit_list_file = 'subreddit_list.txt' # file name of subreddit's list
comment_log_file = 'comment_log.txt' # file name of comment log

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

def run_bot(reddit, comments_replied_to, subreddits_list):
    with open(comment_log_file, "a") as logfile:
        logfile.write("Searching last 1,000 comments\n")
        print "searching"
        for item in subreddits_list:
            logfile.write("subreddit name: {0}\n".format(item))
            for comment in reddit.subreddit(item).comments(limit=1000):
                if comment.id not in comments_replied_to:
                    try:
                        commandline = comment.body
                        logfile.write('commandline: {0}\n'.format(commandline))
                        # print "tip:"
                        # print "{0}abcdefg".format(commandline.split()[0])
                        if 'tip' in commandline.lower():
                            comments_replied_to.append(comment.id)
                            with open ("comments_replied_to.txt", "a") as f:
                                f.write(comment.id + "\n")
                            print "tip(comment)"
                            tip(reddit, comment, logfile)
                        # elif commandline.split()[0] == 'gild':
                        #     # gild(commandline)
                    except:
                        logfile.write('to frequent\n')
            logfile.write("Sleeping for 10 seconds...\n")
            #Sleep for 10 seconds...
        time.sleep(10)


def tip(reddit, comment, logfile):
    print 'it is inside tip function\n'
    sender = comment.author.name.lower()
    if len(comment.body.split()) == 3:
        amount = comment.body.split()[1]
        try:
            amount = float(amount)
            receiver = comment.body.lower().split()[2]
            if receiver[0]=='/' and receiver[1]=='u' and receiver[2]=='/':
                try:
                    receiver = receiver[3:]
                    print "receiver:"
                    print receiver
                    user = reddit.redditor(receiver)
                    try:
                        if user.id: # if it is valid user
                            senderStr = 'reddit-{0}'.format(sender)
                            receiverStr = 'reddit-{0}'.format(receiver)
                            result = subprocess.check_output([core,"getbalance", senderStr])[:-1]
                            balance = float(result)
                            logfile.write("balance:\n{0}".format(balance))
                            logfile.write("---------------\n")
                            logfile.write("receiver:\n{0}".format(receiverStr))
                            logfile.write("sender:\n{0}".format(senderStr))
                            if balance < amount:
                                reddit.redditor(sender).message('Tip error', "{0}, you have insufficent funds.".format(sender))
                                logfile.write("{0}, you have insufficent funds.".format(sender))
                            elif receiver == sender:
                                # comment.reply("You can't tip yourself silly.")
                                reddit.redditor(sender).message('Tip error', "You can't tip yourself silly.")
                                logfile.write("You can't tip yourself silly.")
                            else:
                                balance = str(balance)
                                amount = str(amount)
                                # check if the receiver has wallet account
                                addresses = subprocess.check_output([core, "getaddressesbyaccount", receiverStr])
                                if len(addresses.split())==2:
                                    subprocess.check_output([core,"getaccountaddress", receiverStr])
                                # send coin to custom reddit user
                                tx = subprocess.check_output([core,"move",senderStr,receiverStr,amount])[:-1]
                                # comment.reply("@{0} tipped @{1}RPC to @{2}".format(sender, amount, receiver))
                                # reddit.redditor(sender).message('Tip', "@{0} tipped @{1}RPC to @{2}".format(sender, amount, receiver))
                                reddit.redditor(receiver).message('Tipped', "{0} tipped you {1} of Ron Paul Coin via the RonTips4Liberty tipping bot. For  instructions on how to withdraw, tip other users & more, visit https://www.reddit.com/r/RonTips4Liberty/wiki/index".format(sender, amount))
                                logfile.write("{0} tipped {1}RPC to {2}".format(sender, amount, receiver))
                    except:
                        reddit.redditor(sender).message('Tip error', "Invalid user error!")
                        logfile.write("Invalid user error!")
                        print "Invalid user error!"
                except Exception as ex:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    logfile.write(message)
            else:
                reddit.redditor(sender).message('Tip accountname format error', "Usage in comment: `tip <amount> /u/<username>`".format(sender))
                logfile.write('Tip error: {0}'.format(comment.body))
        except ValueError:
            reddit.redditor(sender).message('Tip error', "Usage in comment: `tip <amount> /u/<username>`".format(sender))
            logfile.write('Tip amount error: {0}'.format(comment.body))
    else:
        reddit.redditor(sender).message('Tip error', "Usage in comment: `tip <amount> /u/<username>`".format(sender))
        logfile.write('Tip format error: {0}'.format(comment.body))

def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = filter(None, comments_replied_to)
    return comments_replied_to

def get_subreddit_list(filename):
    print "Reading subreddits from {0} file".format(filename)
    if not os.path.isfile(filename):
        subreddits_list = []
    else:
        with open(filename, "r") as f:
            subreddits_list = f.read()
            subreddits_list = subreddits_list.split("\n")
            subreddits_list = filter(None, subreddits_list)
            print subreddits_list
    return subreddits_list

reddit = bot_login()
subreddits_list = get_subreddit_list(subreddit_list_file)
comments_replied_to = get_saved_comments()
# print comments_replied_to

while True:
    run_bot(reddit, comments_replied_to, subreddits_list)