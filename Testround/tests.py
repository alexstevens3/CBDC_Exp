from otree.api import Currency as c, currency_range, expect, Bot
from . import *
import random

class PlayerBot(Bot):
    def play_round(player):
        yield Welcome
        yield Treatment
        choice = random.choice([True, False])
        yield CBDCChoice, dict(testCBDC_Choice=choice)
        if choice:
            # Test submission that should fail (sum not equal to 10)
            yield SubmissionMustFail(PaymentChoice, dict(testMOP1=3, testMOP2=7, testMOP3=2))

            # Generate values that satisfy the sum constraint (sum equals 10)
            while True:
                testMOP1 = random.randint(0, 10)
                testMOP2 = random.randint(0, 10)
                testMOP3 = 10 - testMOP1 - testMOP2
                # Check if values are within bounds
                if 0 <= testMOP3 <= 10:
                    break

            # Successful submission with valid values
            yield PaymentChoice, dict(testMOP1=testMOP1, testMOP2=testMOP2, testMOP3=testMOP3)
        else:
            # Similar logic if `choice` is False (if necessary)
            testMOP1 = random.randint(0, 10)
            testMOP2 = 10 - testMOP1
            yield PaymentChoice, dict(testMOP1=testMOP1, testMOP2=testMOP2)
        #if choice:
         #   yield PaymentChoice, dict(testMOP1=1, testMOP2=6, testMOP3=3)
        #else:
         #   yield PaymentChoice, dict(testMOP1=1, testMOP2=9)
        #yield CBDCChoice, dict(testCBDC_Choice= [True, False] )
        #if player.testCBDC_Choice == True:
        #    yield PaymentChoice, dict(testMOP1 = 1, testMOP2 = 6, testMOP3 = 3)
        #if player.testCBDC_Choice == False:
          #  yield PaymentChoice, dict(testMOP1 = 1, testMOP2 = 9)