from otree.api import Currency as c, currency_range, expect, Bot
from . import *
import random
import string

class PlayerBot(Bot):
    def play_round(player):
        yield Welcome
        long_string = ''.join(random.choices(string.ascii_letters + string.digits, k=50))  # Adjust length as needed
        yield CBDC1, dict(cbdc1=long_string)
        risk1_value = random.randint(0, 10)
        yield Risk1, dict(risk=risk1_value)
        
        risk_choices = {
            'risk1': random.choice(['A', 'B']),
            'risk2': random.choice(['A', 'B']),
            'risk3': random.choice(['A', 'B']),
            'risk4': random.choice(['A', 'B']),
            'risk5': random.choice(['A', 'B']),
            'risk6': random.choice(['A', 'B']),
            'risk7': random.choice(['A', 'B']),
            'risk8': random.choice(['A', 'B']),
            'risk9': random.choice(['A', 'B']),
        }
        yield Risk2, risk_choices

        choice_cbdc2 = random.choice([True, False])
        yield CBDC2, dict(cbdc2=choice_cbdc2)

        choices_cbdc3 = random.choice(['sehr wahrscheinlich', 'wahrscheinlich', 'unentschieden', 'unwahrscheinlich', 'sehr unwahrscheinlich' ])
        yield CBDC3, dict(cbdc3=choices_cbdc3)

    
        yield SubmissionMustFail(CBDC4, {
            'rank1_cbdc4': "Anonymität der Zahlungen",
            'rank2_cbdc4': "Anonymität der Zahlungen",  # Deliberate duplication
            'rank3_cbdc4': "Einfache Nutzbarkeit",
            'rank4_cbdc4': "Kostenfreie Nutzung",
        })

        # Correct submission with unique random order of characteristics
        characteristics = [
            "Anonymität der Zahlungen",
            "Sicherheit in Bezug auf Datenschutz",
            "Einfache Nutzbarkeit",
            "Kostenfreie Nutzung"
        ]
        random.shuffle(characteristics)  # Shuffle for random ranking

        yield CBDC4, {
            'rank1_cbdc4': characteristics[0],
            'rank2_cbdc4': characteristics[1],
            'rank3_cbdc4': characteristics[2],
            'rank4_cbdc4': characteristics[3],
        }
        cbdc5_value = random.randint(0, 10)
        yield CBDC5, dict(cbdc5=cbdc5_value)

        yield financial2and3, dict(financial2=102, financial3=True)

        financial1_choice = random.choice(['sehr hoch', 'hoch', 'durchschnittlich', 'niedrig', 'sehr niedrig'])
        yield financial1, dict(financial1=financial1_choice)

        financial4_choice = random.choice(['stimme zu', 'unentschieden', 'stimme nicht zu'])
        yield financial4, dict(financial4=financial4_choice)

        financial5_choices = {
            'Bargeld': random.choice([True, False]),
            'Debitkarte': random.choice([True, False]),
            'Kreditkarte': random.choice([True, False]),
            'Lastschrift_Überweisung': random.choice([True, False]),
            'Internetbezahlverfahren': random.choice([True, False]),
            'mobil': random.choice([True, False])
        }
        yield financial5, financial5_choices

        yield SubmissionMustFail(CBDC6, {
            'rank1_cbdc6': "Bargeld",
            'rank2_cbdc6': "Bargeld",  # Deliberate duplication
            'rank3_cbdc6': "Kontaktlos mit Girocard"
        })

        characteristics_cbdc6 = [
            "Bargeld",
            "Kontaktlos mit Girocard",
            "Einschieben der Girocard in das Terminal und PIN oder Unterschrift",
            "Kontaktlos mit Kreditkarte",
            "Einschieben der Kreditkarte in das Terminal und PIN oder Unterschrift",
            "Bezahlen mit dem Smartphone"
        ]
        random.shuffle(characteristics_cbdc6)  # Shuffle for random ranking and take the top three

        yield CBDC6, {
            'rank1_cbdc6': characteristics_cbdc6[0],
            'rank2_cbdc6': characteristics_cbdc6[1],
            'rank3_cbdc6': characteristics_cbdc6[2]
        }

        financial6_choice = random.choice([
            'habe ich überhaupt keine anderen Optionen in Betracht gezogen,',
            'habe ich mich umgeschaut, aber es gab keine anderen Optionen, die in Frage kamen, ',
            'habe ich verschiedene Optionen von einem Anbieter in Betracht gezogen, ',
            'habe ich mehrere Optionen von verschiedenen Anbietern in Betracht gezogen,'
        ])
        yield financial6, dict(financial6=financial6_choice)

        financial7_choice = random.choice(['stimme zu', 'unentschieden', 'stimme nicht zu'])
        yield financial7, dict(financial7=financial7_choice)

        financial8_choice = random.choice(['volles Vertrauen', 'hohes Vertrauen', 'mittleres Vertrauen', 'geringes Vertrauen', 'kein Vertrauen'])
        yield financial8, dict(financial8=financial8_choice)

        anonymity_choice = random.choice([
            1,  # 'Ich mache mir große Sorgen in Bezug auf die Weitergabe meiner persönlichen Daten.'
            2,  # 'Ich mache mir Sorgen in Bezug auf die Weitergabe meiner persönlichen Daten.'
            3,  # 'Ich mache mir etwas Sorgen in Bezug auf die Weitergabe meiner persönlichen Daten.'
            4   # 'Ich mache mir keine Sorgen in Bezug auf die Weitergabe meiner persönlichen Daten.'
        ])
        yield Anonymity, dict(anonymity=anonymity_choice)

        age = random.randint(15, 125)
        gender = random.choice(['Weiblich', 'Männlich', 'Divers'])
        employment_choices = {
            'Vollzeiterwerbstätig': random.choice([True, False]),
            'Teilzeiterwerbstätig': random.choice([True, False]),
            'Geringfügig_erwerbstätig': random.choice([True, False]),
            'Minijob': random.choice([True, False]),
            'Ruhestand': random.choice([True, False]),
            'Studentin_oder_Student': random.choice([True, False]),
            'Selbstständig': random.choice([True, False]),
            'Nicht_erwerbstätig_und_Arbeitssuchend': random.choice([True, False]),
            'Nicht_erwerbstätig_und_nicht_Arbeitssuchend': random.choice([True, False]),
        }
        education = random.choice(['Keinen Schulabschluss', 'Schulabschluss oder gleichwertiger Abschluss', 'Bachelor', 'Master oder Staatsexamen', 'Promotion'])
        income = random.choice(['unter 500 Euro', '500 bis 999 Euro', '1000 bis 1499 Euro', '1500 bis 1999 Euro', '2000 bis 2499 Euro', '2500 bis 2999 Euro', '3000 bis 3499 Euro', '3500 bis 3999 Euro', '4000 bis 4499 Euro', '4500 bis 4999 Euro', 'über 5000 Euro'])

        yield Demographics, {
            'age': age,
            'gender': gender,
            **employment_choices,
            'education': education,
            'income': income
        }

        if employment_choices['Studentin_oder_Student']:
            degree = random.choice([
                'Volkswirtschaftslehre', 'Betriebswirtschaftslehre', 'Biologie, Biochemie, Chemie oder Physik',
                'Sprachwissenschaften', 'Finanz- und Versicherungsmathematik', 'Geschichte', 'Informatik',
                'Kommunikations- und Medienwissenschaft', 'Mathematik', 'Medizin oder Pharmazie',
                'Politik- oder Sozialwissenschaften', 'Psychologie', 'Rechtswissenschaften', 'Anderer Studiengang'
            ])
            semester = random.choice([None, random.randint(1, 12)])  # Randomly leave blank or set a value
            grade = random.choice([None, round(random.uniform(0.0, 5.0), 2)])  # Randomly leave blank or set a valid grade

            # Prepare the dictionary for submission, omitting fields if they are None
            demographics_degree_data = {
                'degree': degree,
                'semester': semester if semester is not None else '',
                'grade': grade if grade is not None else '',
            }

            yield Demographics_degree, demographics_degree_data
        yield Auszahlungsseite

 