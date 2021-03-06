import praw, sys, asyncio
from os import environ, path
sys.path.insert(0,path.dirname(path.dirname(__file__)))
from dotenv import load_dotenv
import shared.calculator.decision_tree as tree

basedir = path.dirname(path.abspath(path.dirname(__file__)))
load_dotenv(path.join(basedir, '.env'))

def reddit_connect():
    r = praw.Reddit(client_id = environ.get('CLIENT_ID'),
                    client_secret = environ.get('CLIENT_SECRET'),
                    redirect_uri = environ.get('REDIRECT_URI'),
                    user_agent = environ.get('USER_AGENT'),
                    refresh_token = environ.get('REFRESH_TOKEN'))
    return(r)

async def validate(item):
    commands = ['pitch','swing','bunt ','steal','throw']
    reddit_name = item.author.name
    message_body = item.body
    # Bunts probably don't work this way yet; will need to strip off whitespace and whatnot
    if message_body.startswith('m!') and message_body[2:7] in commands:
        command = message_body[2:7]
        number = message_body.split(' ')[1]
        try:
            flavor = ' '.join(message_body.split(' ')[2:])
        except:
            flavor = None
        try:
            number = int(number)
        except:
            return("I couldn't parse a number out of that. Please use the format 'm!pitch 123', for example.")
        if number > 0 and number < 1001:
            payload = {'Command':command,'Number':number,'Redditor':reddit_name,'Discord':None,'Flavor':flavor}
            msg = await tree.routing(payload)
            return(msg)
        else:
            return("That number is not between 1 and 1000")
    else:
        return("That isn't a recognizable command. Please use the format 'm!pitch 123', for example.")


async def listener():
    r = reddit_connect()
    for item in r.inbox.stream(skip_existing=True):
        if item.was_comment == False:
            msg = await validate(item)
            item.reply(msg)

if __name__ == "__main__":
    asyncio.run(listener())
