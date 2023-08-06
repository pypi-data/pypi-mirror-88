
import csv
from random import randrange
import pathlib
import os

# First get the absolute path of this file. The 'Data' folder which contains the user_agents.csv can be found relative to this path
file_dir_path = pathlib.Path(__file__).parent.absolute()
csv_file_path = os.path.join(file_dir_path,"Data/","user_agents.csv")

def get_usr_agnts(path = csv_file_path):
    try:
        usr_agnts  = list(csv.DictReader(open(path)))
        user_agent = {'User-Agent': usr_agnts[randrange(0,len(usr_agnts)-1)]['user_agent']}
    except Exception as err:
        print("Error while loading user agent file:", err)
        user_agent = ""
    return user_agent
