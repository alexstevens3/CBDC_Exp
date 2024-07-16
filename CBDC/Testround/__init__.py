from otree.api import *
import random

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'Testround'
    PLAYERS_PER_GROUP = 10
    NUM_ROUNDS = 1
    MAXIMUM_EM = cu(10)
    TC_MOP1 = 0.60
    TC_MOP2 = 0.38
    TC_MOP3 = 0.10
    Adoption_MOP3 = 0.40 
     

@staticmethod
def creating_session(subsession):
    import itertools
    if subsession.round_number ==1:
        testCBDC = itertools.cycle(['Account', 'Token'])
        for player in subsession.get_players():
            player.testCBDC_design = next(testCBDC)
        

class Subsession(BaseSubsession):
    pass
    
class Group(BaseGroup):
    pass

class Player(BasePlayer):
    testMOP1 = models.IntegerField(
        min=0,
        max=C.MAXIMUM_EM,
        label="Zahlungsmittel 1:", 
    )
    testMOP2 = models.IntegerField(
        min=0,
        max=C.MAXIMUM_EM,
        label="Zahlungsmittel 2:", 
    )
    testMOP3 = models.IntegerField(
        min=0,
        max=C.MAXIMUM_EM,
        label="Zahlungsmittel 3:", 
    )
    testCBDC_Choice = models.BooleanField(
        label="Möchten Sie Zahlungsmittel 3 nutzen?", 
    )
    
    testCBDC_design = models.StringField()
    
    amount1 = models.IntegerField(
        label= 'Zahlungsmittel 1:',
        min=0,
        max=10,
        blank=True)
    amount2 = models.FloatField(
        label= 'Zahlungsmittel 2:',
        min=0,
        max=10,
        blank=True)
    amount3 = models.FloatField(
        label= 'Zahlungsmittel 3:',
        min=0,
        max=10,
        blank=True)

class Treatment(Page):
    timeout_seconds = 30

class CBDCChoice(Page):
    form_model = 'player'
    form_fields = ['testCBDC_Choice'] 

class PaymentChoice(Page):
    form_model = 'player'
    form_fields = ['amount1', 'amount2', 'amount3']

    @staticmethod
    def get_form_fields(player):
        if player.testCBDC_Choice == True:
            return ['testMOP1', 'testMOP2', 'testMOP3', 'amount1', 'amount2', 'amount3']
        else:
            return ['testMOP1', 'testMOP2', 'amount1', 'amount2', 'amount3']

    @staticmethod
    def error_message(player, values):
        print('values is', values)
        if player.testCBDC_Choice == True and values['testMOP1'] + values['testMOP2'] + values['testMOP3'] != C.MAXIMUM_EM:
            return 'Die Summe der Zahlungsmittel muss insgesamt 10 ergeben'
        if player.testCBDC_Choice == False and values['testMOP1'] + values['testMOP2'] != C.MAXIMUM_EM:
            return 'Die Summe der Zahlungsmittel muss insgesamt 10 ergeben'

    @staticmethod
    def js_vars(player):
        return dict(TC1=C.TC_MOP1, TC2=C.TC_MOP2, TC3=C.TC_MOP3)

    
class WaitingPage(WaitPage):
    template_name = 'Experiment\WaitingPage.html'
    wait_for_all_players = True

class Welcome(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

page_sequence = [Welcome, WaitingPage, Treatment, CBDCChoice, WaitingPage, PaymentChoice, WaitingPage]