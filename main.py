from statistics import NormalDist
import random
import csv

#CONSTANTS
ITERATIONS = 10000
PRINCIPAL = 100000
START_DATE = 2025
END_DATE = 2040
PHASE_ONE_NUM_HOUSES = 7
PHASE_ONE_COST_PER_HOUSE = 10331
PHASE_TWO_INITIAL_COSTS = 75000
PHASE_TWO_OPERATION_COSTS = 25000
PHASE_ONE_GROWTH_MEAN = 1.12
PHASE_ONE_GROWTH_STD = 0.16
PHASE_TWO_GROWTH_MEAN = 1.06
PHASE_TWO_GROWTH_STD = 0.08


#Portfolio Actions
def compound_year(balance, phase):
    if phase == 1:
        balance *= NormalDist(PHASE_ONE_GROWTH_MEAN, PHASE_ONE_GROWTH_STD).inv_cdf(random.random())
    elif phase == 2:
        balance *= NormalDist(PHASE_TWO_GROWTH_MEAN, PHASE_TWO_GROWTH_STD).inv_cdf(random.random())
    return balance

def ladi_spending(balance, year):
    if year == 2030:
        balance -= PHASE_ONE_NUM_HOUSES * PHASE_ONE_COST_PER_HOUSE
    if year == 2040:
        balance -= PHASE_TWO_INITIAL_COSTS + PHASE_TWO_OPERATION_COSTS
    return balance

#Start Simulation
balances = []
for i in range(ITERATIONS):
    phase = 1
    balance = PRINCIPAL
    for year in range(START_DATE, END_DATE + 1):
        if year == 2031:
            phase = 2
        balance = compound_year(balance, phase)
        balance = ladi_spending(balance, year)
        if(balance <= 0):
            break
    balances.append([max(balance, 0)])

#Write To File
with open('results.csv', 'w', newline="") as results:
    wr = csv.writer(results, quoting=csv.QUOTE_ALL)
    for data in balances:
        wr.writerow(data)