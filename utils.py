from statistics import NormalDist
from math import ceil

#Gets the number of places paid based on the number of players in the field (assumed PDGA standard 40% cash)
def get_spots_paid(n):
  return ceil(0.4*n)

#Gets the Standard Deviation from a series of ratings
def get_std(rtgs):

  mean = sum(rtgs) / len(rtgs) 
  variance = sum([((x - mean) ** 2) for x in rtgs]) / len(rtgs)
  res = variance ** 0.5
  return res

#Calculates a result of a given simulated tournament given players standard deviation and rating
def calculate_result (rounds, players, dists):

  current_best = 0
  current_winner = ""
  results = []
  for p in players:
    s = sum(dists[p].samples(rounds))/rounds
    results.append(s)
    if (current_best < s):
      current_best = s
      current_winner = p
  results.sort(reverse=True)
  players_paid = get_spots_paid(len(players))

  return current_winner, current_best, results[players_paid-1]

#Calculates the result of N tournaments with a specified number of rounds and specified players
def calculate_tournament (N, rounds, players):

  win_percentage = {}
  dists = {}

  for p in players:
    win_percentage[p]=0
    dists[p] = NormalDist(mu=players[p][0], sigma=players[p][1])

  winner_rating_sum = 0
  cash_rating_sum = 0
  for n in range(N):

    winner_number, winner_rating, cash_rating = calculate_result(rounds, players, dists)

    win_percentage[winner_number]+=100/N
    winner_rating_sum+=winner_rating/N
    cash_rating_sum+=cash_rating/N

  return winner_rating_sum, cash_rating_sum, win_percentage

#Returns sorted/prettified version of the results
def simulate_tournament(players, rounds, N):

  avg, cash_avg, win_percentage = calculate_tournament(N, rounds, players)

  sorted_win_percentage = sorted(win_percentage.items(), key=lambda item: item[1], reverse=True)
  for i in range(len(sorted_win_percentage)):
    sorted_win_percentage[i] = (players[sorted_win_percentage[i][0]][2],round(sorted_win_percentage[i][1],2))

  return round(avg,2), round(cash_avg,2), sorted_win_percentage
