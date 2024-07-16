from os import environ

SESSION_CONFIGS = [
     dict(
         name='CBDC_Experiment',
         app_sequence=['testquestions','Testround','Experiment','survey', 'payment' ],
         num_demo_participants=10,
       
       display_name="CBDC_Experiment",
       
       expShortName="Pilotsession", # Replace with your values
       expId=17, # Replace with your values
       sessId=0000000000, # Replace with your values
       
    )]  

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.07, participation_fee=6.00, doc=""
)

PARTICIPANT_FIELDS = ['payoff_euro','payoff_allrounds', 'payoff_euro_fee_survey', 'payoff_anonym_allrounds','payoff_notanonym_allrounds', 'payoff_anonym_euro', 'payoff_notanonym_euro' ]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'

ROOMS = [
    dict(
        name='DiceLab',
        display_name='DiceLab',
        participant_label_file='C:/CBDC/CBDC/dicelab_otree_labels.txt'
    )
]


# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = ''
USE_POINTS = False
POINTS_CUSTOM_NAME =  'Taler'

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5723496014656'
