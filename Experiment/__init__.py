from otree.api import *
import random

doc = """
Experiment CBDC
"""

class C(BaseConstants):
    NAME_IN_URL = 'Experiment'
    PLAYERS_PER_GROUP = 10
    NUM_ROUNDS = 10
    MAXIMUM_EM = cu(10)
    TC_MOP1 = 0.60
    TC_MOP2 = 0.38
    TC_MOP3 = 0.10
    Adoption_MOP3 = 0.40 
     
@staticmethod
def creating_session(subsession):
    player = subsession.get_players()
    for player in subsession.get_players():
        player.prob_MOP2 = random.randint(0,100)   

    import itertools
    if subsession.round_number <=5:
        CBDC = itertools.cycle(['Account', 'Token'])
        for player in subsession.get_players():
            player.CBDC_design = next(CBDC)

    if subsession.round_number > 5:
        CBDC = itertools.cycle(['Token', 'Account'])
        for player in subsession.get_players():
            player.CBDC_design = next(CBDC)
        
@staticmethod
def set_payoffs(player):
    session=player.session
    player.payoff = (player.payoff_MOP1 + player.payoff_MOP2 + player.payoff_MOP3) * session.config['real_world_currency_per_point']

class Subsession(BaseSubsession):
    pass
    
class Group(BaseGroup):
    nb_players_CBDC_Yes = models.FloatField()
    share_players_CBDC_Yes = models.FloatField()
    sum_MOP3 = models.FloatField()
    average_MOP3 = models.FloatField()

class Player(BasePlayer):
    payoff_allMOP = models.CurrencyField()
    payoff_allrounds = models.CurrencyField()
    payoff_anonym = models.CurrencyField()
    payoff_notanonym = models.CurrencyField()
    payoff_anonym_allrounds = models.CurrencyField()
    payoff_notanonym_allrounds = models.CurrencyField()
    payoff_notanonym_euro = models.CurrencyField()

    MOP1 = models.IntegerField(
        min=0,
        max=C.MAXIMUM_EM,
        label="Zahlungsmittel 1:", 
    )
    MOP2 = models.IntegerField(
        min=0,
        max=C.MAXIMUM_EM,
        label="Zahlungsmittel 2:", 
    )
    MOP3 = models.IntegerField(
        min=0,
        max=C.MAXIMUM_EM,
        label="Zahlungsmittel 3:", 
    )
    CBDC_Choice = models.BooleanField(
        label="Möchten Sie Zahlungsmittel 3 nutzen?", 
    )
    
    prob_MOP2 = models.IntegerField()
    CBDC_design = models.StringField()
    MOP2_accept = models.BooleanField()
    MOP3_accept = models.BooleanField()
    transactions_MOP1 = models.CurrencyField()
    transactions_MOP2 = models.CurrencyField()
    transactions_MOP3 = models.CurrencyField()
    payoff_MOP1 = models.CurrencyField()
    payoff_MOP2 = models.CurrencyField()
    payoff_MOP3 = models.CurrencyField()
    CBDC_Choice_Yes = models.IntegerField()
    
    belief1 = models.IntegerField(
        label="",
        min=0,
        max=C.PLAYERS_PER_GROUP,
        doc="Belief about/Expected CBDC_Choice_Yes")
    belief2 = models.IntegerField(
        label="",
        min=0,
        max=C.MAXIMUM_EM,
        doc="Belief about/Expected MOP3")
    belief3 = models.BooleanField(
       label="",
       doc="Belief about prob. acceptance MOP3")
    
    next_round = models.IntegerField()
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
    payoff_MOP3_Token = models.CurrencyField()
    payoff_MOP3_Account = models.CurrencyField()
    
class Treatment(Page):
    timeout_seconds = 30

class CBDCChoice(Page):
    form_model = 'player'
    form_fields = ['CBDC_Choice']

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.CBDC_Choice == 1:
            player.CBDC_Choice_Yes =1
        if player.CBDC_Choice == 0:
            player.CBDC_Choice_Yes =0  

class PaymentChoice(Page):
    form_model = 'player'
    form_fields = ['amount1', 'amount2', 'amount3']

    @staticmethod
    def get_form_fields(player):
        if player.CBDC_Choice == True:
            return ['MOP1', 'MOP2', 'MOP3', 'amount1', 'amount2', 'amount3']
        else:
            return ['MOP1', 'MOP2', 'amount1', 'amount2', 'amount3']

    @staticmethod
    def error_message(player, values):
        print('values is', values)
        if player.CBDC_Choice == True and values['MOP1'] + values['MOP2'] + values['MOP3'] != C.MAXIMUM_EM:
            return 'Die Summe der Zahlungsmittel muss insgesamt 10 ergeben'
        if player.CBDC_Choice == False and values['MOP1'] + values['MOP2'] != C.MAXIMUM_EM:
            return 'Die Summe der Zahlungsmittel muss insgesamt 10 ergeben'

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.MOP2_accept=player.prob_MOP2<=81

    @staticmethod
    def js_vars(player):
        return dict(TC1=C.TC_MOP1, TC2=C.TC_MOP2, TC3=C.TC_MOP3)

class WaitingPage(WaitPage):
    template_name = 'Experiment/WaitingPage.html'
    wait_for_all_players = True

class Beliefs(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        if 1< player.round_number <C.NUM_ROUNDS:
            return ['belief1','belief2', 'belief3']
        
    @staticmethod
    def vars_for_template(player):
        player.next_round = player.round_number + 1
        if player.CBDC_Choice == False:
            player.MOP3 = 0 

        group = player.group
        players = group.get_players()
        
        for player in group.get_players():
            group.nb_players_CBDC_Yes = sum([player.CBDC_Choice_Yes for player in players]) 
            group.share_players_CBDC_Yes = (group.nb_players_CBDC_Yes /  C.PLAYERS_PER_GROUP) *100
          
            group.sum_MOP3 = sum([player.field_maybe_none('MOP3') for player in players if player.CBDC_Choice_Yes ==1 ]) 
            group.average_MOP3 = group.sum_MOP3 / C.PLAYERS_PER_GROUP

    @staticmethod
    def before_next_page(player, timeout_happened):
        group = player.group
        players = group.get_players()

        player.transactions_MOP1 = player.MOP1 
        if player.MOP2_accept == True:
            player.transactions_MOP2 = player.MOP2
        if player.MOP2_accept == False:
            player.transactions_MOP2 = 0
        if player.CBDC_Choice == True and group.share_players_CBDC_Yes >= 50: 
            player.transactions_MOP3 = player.MOP3
        if player.CBDC_Choice == True and group.share_players_CBDC_Yes < 50:
            player.transactions_MOP3 = 0
        if player.CBDC_Choice == False:
            player.transactions_MOP3 = 0

class Welcome(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class WaitingPage2(WaitPage):
    template_name = 'Experiment/WaitingPage2.html'
    wait_for_all_players = True

class Trading(Page):
    @staticmethod
    def before_next_page(player, timeout_happened):
        set_payoffs(player)

        group = player.group
        players = group.get_players()
        
        for player in group.get_players():
            if group.share_players_CBDC_Yes >=50:
                player.MOP3_accept = 1
            if group.share_players_CBDC_Yes < 50:
                player.MOP3_accept = 0

    @staticmethod
    def vars_for_template(player):

        group = player.group
        players = group.get_players()
        
        player.payoff_MOP1 = player.transactions_MOP1 - (player.transactions_MOP1 * 0.6)
        if player.MOP2_accept == True:
            player.payoff_MOP2= player.transactions_MOP2 - (player.transactions_MOP2 * 0.38)
        if player.MOP2_accept == False:
            player.payoff_MOP2 = 0
        if player.CBDC_Choice == True: 
            player.payoff_MOP3= player.transactions_MOP3 - (player.transactions_MOP3 * 0.1) - 0.4

        if player.transactions_MOP3 == 0:
            player.payoff_MOP3 = 0

        if player.CBDC_Choice == False:
            player.payoff_MOP3 = 0

        player.payoff_allMOP = player.payoff_MOP1 + player.payoff_MOP2 + player.payoff_MOP3

        if player.CBDC_design == "Token":
            player.payoff_MOP3_Token = player.payoff_MOP3
        else:
            player.payoff_MOP3_Token = 0
        if player.CBDC_design == "Account":
            player.payoff_MOP3_Account = player.payoff_MOP3
        else:
            player.payoff_MOP3_Account = 0
        player.payoff_anonym = player.payoff_MOP3_Token + player.payoff_MOP1
        player.payoff_notanonym = player.payoff_MOP3_Account + player.payoff_MOP2

    @staticmethod
    def js_vars(player):
        return dict(T2=player.transactions_MOP2, TC1=C.TC_MOP1, TC2=C.TC_MOP2, TC3=C.TC_MOP3)

class Total_Payoff(Page):
    @staticmethod
    def vars_for_template(player):
        if player.round_number > 1:
            player.payoff_allrounds = sum([player.payoff_allMOP for player in player.in_all_rounds()])
        else:
            player.payoff_allrounds = player.payoff_allMOP

        if player.round_number > 1:
            player.payoff_anonym_allrounds = sum([player.payoff_anonym for player in player.in_all_rounds()])
        else:
            player.payoff_anonym_allrounds = player.payoff_anonym

        if player.round_number > 1:
            player.payoff_notanonym_allrounds = sum([player.payoff_notanonym for player in player.in_all_rounds()])
        else:
            player.payoff_notanonym_allrounds = player.payoff_notanonym

        participant=player.participant

        if player.round_number > 1:
            participant.payoff_allrounds = sum([player.payoff_allMOP for player in player.in_all_rounds()])
        else:
            participant.payoff_allrounds = player.payoff_allMOP

        if player.round_number > 1:
            participant.payoff_anonym_allrounds = sum([player.payoff_anonym for player in player.in_all_rounds()])
        else:
            participant.payoff_anonym_allrounds = player.payoff_anonym
        
        if player.round_number > 1:
            participant.payoff_notanonym_allrounds = sum([player.payoff_notanonym for player in player.in_all_rounds()])
        else:
            participant.payoff_notanonym_allrounds = player.payoff_notanonym

        session=player.session
        if player.round_number == C.NUM_ROUNDS:
            player.payoff_notanonym_euro = player.payoff_notanonym_allrounds * session.config['real_world_currency_per_point']

class DisplayPayoffs(Page):
    def vars_for_template(self):
        participant_payoffs = []
        for player in self.group.in_round(10).get_players():
            participant_payoffs.append((player.participant.id_in_session, player.payoff_notanonym_euro))

        return {'participant_payoffs': participant_payoffs}

    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

page_sequence = [Welcome, WaitingPage, Treatment, CBDCChoice, WaitingPage, PaymentChoice, WaitingPage, Beliefs, WaitingPage, Trading, Total_Payoff, WaitingPage, DisplayPayoffs, WaitingPage]
