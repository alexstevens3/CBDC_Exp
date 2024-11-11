from otree.api import Currency as c, currency_range, expect, Bot
from . import *

class PlayerBot(Bot):
    def play_round(player):
        if player.round_number == 1:
            yield Welcome
        
        yield Treatment

        choice = random.choice([True, False])
        yield CBDCChoice, dict(CBDC_Choice=choice)
    
        if choice:
            # Test submission that should fail (sum not equal to 10)
            yield SubmissionMustFail(PaymentChoice, dict(MOP1=3, MOP2=7, MOP3=2))

            # Generate values that satisfy the sum constraint (sum equals 10)
            while True:
                MOP1 = random.randint(0, 10)
                MOP2 = random.randint(0, 10)
                MOP3 = 10 - MOP1 - MOP2
                # Check if values are within bounds
                if 0 <= MOP3 <= 10:
                    break

            # Successful submission with valid values
            yield PaymentChoice, dict(MOP1=MOP1, MOP2=MOP2, MOP3=MOP3)
        else:
            # Similar logic if `choice` is False (if necessary)
            MOP1 = random.randint(0, 10)
            MOP2 = 10 - MOP1
            yield PaymentChoice, dict(MOP1=MOP1, MOP2=MOP2)

        if 1 < player.round_number < C.NUM_ROUNDS:
            # Fill in values only for rounds 2 through (C.NUM_ROUNDS - 1)
            belief1 = random.randint(0, 10)
            belief2 = random.randint(0, 10)
            belief3 = random.randint(0, 10000)

            # Assert that values are within the specified bounds
            assert 0 <= belief1 <= 10, "belief1 should be between 0 and 10"
            assert 0 <= belief2 <= 10, "belief2 should be between 0 and 10"
            assert 0 <= belief3 <= 10000, "belief3 should be between 0 and 10000"

            yield Beliefs, dict(belief1=belief1, belief2=belief2, belief3=belief3)
        else:
            # Yield the Beliefs page without filling values for rounds 1 and 10
            yield Beliefs

        yield Trading
        yield Total_Payoff
        if player.round_number == 10:
            yield DisplayPayoffs
       

        