
import csv
from random import randrange

def get_usr_agnts(path = "user_agents.csv"):
    try:
        usr_agnts  = list(csv.DictReader(open(path)))
        user_agent = {'User-Agent': usr_agnts[randrange(0,len(usr_agnts)-1)]['user_agent']}
    except Exception as err:
        print("Error while loading user agent file:", err)
        user_agent = ""
    return user_agent
