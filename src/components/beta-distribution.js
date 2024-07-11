import jStat from 'jstat';
import * as d3 from 'npm:d3';

export function prior(historical_win_pct) {
    const mean_w = d3.mean(historical_win_pct);
    const var_w = d3.variance(historical_win_pct);
    return {
      alpha: mean_w * (mean_w * (1 - mean_w) / var_w - 1),
      beta: (1 - mean_w) * (mean_w * (1 - mean_w) / var_w - 1)
    }
  }
export function posterior(
    alpha_prior,
    beta_prior,
    current_wp,
    current_games_played
  ) {
    return {
      alpha_posterior: alpha_prior + current_wp * current_games_played,
      beta_posterior:
        beta_prior + current_games_played - current_wp * current_games_played
    };
  }
export function calculateParameters(historical, current_wp, curremt_games_played) {
    return {
      alpha_prior: prior(historical).alpha,
      beta_prior: prior(historical).beta,
      alpha_posterior: posterior(
        prior(historical).alpha,
        prior(historical).beta,
        current_wp,
        curremt_games_played
      ).alpha_posterior,
      beta_posterior: posterior(
        prior(historical).alpha,
        prior(historical).beta,
        current_wp,
        curremt_games_played
      ).beta_posterior
    };
  }
export function calculateCDF(lower, upper, alpha, beta) {
    const lowerFloat = parseFloat(lower);
    const upperFloat = parseFloat(upper);
    return (
      jStat.beta.cdf(upperFloat, alpha, beta) -
      jStat.beta.cdf(lowerFloat, alpha, beta)
    );
  }
export function calculateBucketsProbabilities(buckets, alpha, beta) {
    const probabilitiesBuckets = new Object();
    for (const elem in buckets) {
      probabilitiesBuckets[`${buckets[elem][0]} - ${buckets[elem][1]}`] =
        calculateCDF(buckets[elem][0], buckets[elem][1], alpha, beta) * 100;
    }
  
    return probabilitiesBuckets;
  }