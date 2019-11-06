# Reddit_Tip_Bot

Reddit RonPaulCoin tipping bot using reddit api in python. Used crytocurrency daemon on ubuntu AWS EC2 Server for crptocurrency tipping.
Updated C++ RPC daemon code and fixed compile error.

# Tippr


Tippr revolutionizes RonPaulCoin tipping by allowing people to tip anyone, even if they don't already have a RonPaulCoin wallet or social account.
---
# Basic Usage
You can summon the bot into any thread. Just post a comment with a comment command (listed below).
You can also PM it directly with commands, but leave out `/u/RonTips4Liberty` and `/u/RonTips4Liberty` if PMing it.
After that, it takes arguments which I'll explain below.

### Balance
Usage in comment: `None`  
Usage in PM: `balance`  [or click here](https://www.reddit.com/message/compose/?to=RonTips4Liberty&subject=Balance&message=balance)

This command will have tippr reply to you with your current balance.
Your balance is a combination of your deposits and received tips, minus your sent tips and withdrawals, and can be both tipped or withdrawn.

### Deposit
Usage in comment: `None`
Usage in PM: `deposit`  [or click here](https://www.reddit.com/message/compose/?to=RonTips4Liberty&subject=Deposit&message=deposit)

With this, tippr will send you a PM with an address to deposit at.
Your deposit will be stored in an intermediary wallet that you can withdraw from at any time.
For reasons, the deposit requires **3 confirmations** before being credited to your account. You'll receive a PM upon successful crediting.

### Tip
Usage in comment: `<amount> /u/RonTips4Liberty`
Usage in PM: You can't use this command in a PM. Sorry.

Example: `tip 0.5 /u/RonTips4Liberty`
This will (internally) transfer the `<amount>` to the user you're replying to.
If they don't have an address registered with tippr, that's okay; it'll notify the recipient and store the tip until the user is ready to claim it.
Received tips can be re-tipped or withdrawn.

### Withdraw
Usage in comment: You can't use this command in a comment. Sorry.
Usage in PM: `withdraw <amount> <address>` [or click here](https://www.reddit.com/message/compose/?to=RonTips4Liberty&subject=Withdrawal&message=withdraw AMOUNT ADDRESS)
