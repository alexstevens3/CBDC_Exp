from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'testquestions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    q1_true= 3
    q2_true= 1
    q3_true = 'Anonymität'
    q4_true = 81
    q5_true = 50



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.IntegerField(
        label= 'Wie viele Zahlungsmittel gibt es im Experiment?'
    )
    q2 = models.IntegerField(
        label= 'Welches Zahlungsmittel hat die höchsten Transaktionskosten?'
    )
    q3 = models.StringField(
        label= 'Wodurch unterscheiden sich die Gruppen „grün“ und „blau“?',
        choices = ['Akzeptanz', 'Anonymität', 'Transaktionskosten'],
        widget=widgets.RadioSelect,
    )
    q4 = models.IntegerField(
        label= 'Wie hoch ist die Wahrscheinlichkeit, dass Zahlungsmittel 2 vom Verkäufer akzeptiert wird? (in %)'
    )
    q5 = models.IntegerField(
        label= 'Wie hoch muss der Anteil der Käufer mindestens sein, die 0.40 Taler für die Nutzung von Zahlungsmittel 3 zahlen, damit Zahlungsmittel 3 vom Verkäufer akzeptiert wird? (in %)'
    )
    q1_answer = models.IntegerField()
    q2_answer = models.IntegerField()
    q3_answer = models.IntegerField()
    q4_answer = models.IntegerField()
    q5_answer = models.IntegerField()
    all_answers_right = models.BooleanField()
    

    


class Welcome(Page):
    pass


class Welcome2(Page):
    pass


class Questions(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4', 'q5']

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.q1 == C.q1_true:
            player.q1_answer =1
        else: player.q1_answer = 0
        if player.q2 == C.q2_true:
            player.q2_answer = 1
        else: player.q2_answer = 0
        if player.q3 == C.q3_true:
            player.q3_answer = 1
        else: player.q3_answer = 0
        if player.q4 == C.q4_true:
            player.q4_answer = 1
        else: player.q4_answer = 0
        if player.q5 == C.q5_true:
            player.q5_answer = 1
        else: player.q5_answer = 0
        

class WaitingPage(WaitPage):
    template_name = 'testquestions/WaitingPage.html'
    wait_for_all_players = True

class Results(Page):
    @staticmethod
    def vars_for_template(player):
        if player.q1_answer ==1 and player.q2_answer ==1 and  player.q3_answer ==1 and  player.q4_answer ==1 and  player.q5_answer ==1:
            player.all_answers_right = 1
        else: player.all_answers_right = 0


page_sequence = [Welcome, Welcome2, WaitingPage, Questions, WaitingPage, Results]
