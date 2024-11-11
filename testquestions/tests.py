from otree.api import Currency as c, currency_range, expect, Bot
from . import *
import random

class PlayerBot(Bot):
    def play_round(player):
        yield Welcome
        yield Welcome2
        

        q1_value = random.randint(0, 1000)  
        q2_value = random.randint(0, 1000)  
        q4_value = random.randint(0, 1000)  
        q5_value = random.randint(0, 1000)  
        q3_value = random.choice(['Akzeptanz', 'Anonymität', 'Transaktionskosten'])
        
        yield Questions, dict(q1=q1_value, q2=q2_value, q3=q3_value, q4=q4_value, q5=q5_value)
        yield Results

