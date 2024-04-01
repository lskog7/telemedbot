from bot_requests import *
from db_model import *
import datetime

q = Questions.select()
for q in q: print(q.text)