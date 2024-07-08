import pandas as pd
import numpy as np
from scipy.stats import beta
from datetime import datetime
import json
import sys

df = pd.read_csv('../data-repository/retrosheet/win_loss_records_yankees.csv')
df = df.loc[:, ['season', 'game_number', 'winning_pct']]
final_season_win_pct = df.sort_values('season').groupby('season').tail(1)
historical_win_pct = np.array(final_season_win_pct[~final_season_win_pct['season'].isin([2024])]['winning_pct'].tolist())

# Prior estimation
mean_w = np.mean(historical_win_pct)
var_w = np.var(historical_win_pct)
alpha_prior = mean_w * (mean_w * (1 - mean_w) / var_w - 1)
beta_prior = (1 - mean_w) * (mean_w * (1 - mean_w) / var_w - 1)

# Current season data
current_win_percentage = float(final_season_win_pct.loc[final_season_win_pct['season'].isin([2024])]['winning_pct'].iloc[0])  # Example to-date Win %
current_games_played = int(final_season_win_pct.loc[final_season_win_pct['season'].isin([2024])]['game_number'].iloc[0])  # Example games played so far

# Posterior update
alpha_post = alpha_prior + current_win_percentage * current_games_played
beta_post = beta_prior + current_games_played - current_win_percentage * current_games_played

# Define buckets
buckets = [(0, 0.45), (0.45, 0.5), (0.5, 0.55), (0.55, 0.6), (0.6, 0.65), (0.65, 0.7), (0.7, 0.75), (0.75, 1.0)]

# Calculate probabilities for each bucket
bucket_probabilities = []
for a, b in buckets:
    prob = beta.cdf(b, alpha_post, beta_post) - beta.cdf(a, alpha_post, beta_post)
    bucket_probabilities.append(prob)

# Print the probabilities for each bucket
probs_df = {
    'Date': [],
    'Bucket': [],
    'Probability': []
}
for (a, b), prob in zip(buckets, bucket_probabilities):
    today = datetime.today().strftime('%Y-%m-%d')
    print(f"Probability of Win % between {a} and {b}: {prob:.4f}")
    probs_df['Date'].append(today)
    probs_df['Bucket'].append(f'Win % between {a}-{b}')
    probs_df['Probability'].append(prob)

json.dump(probs_df, sys.stdout)