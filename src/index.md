---
toc: false
---

<div class="hero">
  <h1>Yankees Win % Probability in 2024</h1>
</div>

```js
// import jStat from 'jstat';
import * as aq from 'npm:arquero';
import op from 'npm:arquero';
import {prior, posterior, calculateParameters, calculateCDF, calculateBucketsProbabilities} from './components/beta-distribution.js';
const win_percentage_buckets = [
  [0, 0.45],
  [0.46, 0.5],
  [0.51, 0.55],
  [0.56, 0.6],
  [0.61, 0.65],
  [0.66, 0.7],
  [0.71, 0.75],
  [0.76, 1.0]
];

const data = aq.fromCSV(await FileAttachment("./data/win_loss_records_yankees.csv").text());
const seasonWinPercentage = data
  .groupby("season")
  .rollup({
    max_games: (d) => op.max(d.game_number)
  })
  .ungroup()
  .join_right(data.select("season", "game_number", "winning_pct"))
  .orderby((d) => d.season)
  .filter((d) => d.game_number === d.max_games)
  .select("season", "game_number", "winning_pct")
  .derive({ season: (d) => "" + d.season })
  .reify();
const historical_win_percentages = seasonWinPercentage
  .filter((d) => d.season != "2024")
  .array("winning_pct");
const current_game_number = seasonWinPercentage
  .filter((d) => d.season == 2024)
  .array("game_number")[0];
const current_winning_pct = seasonWinPercentage
  .filter((d) => d.season == 2024)
  .array("winning_pct")[0];
const params = calculateParameters(
  historical_win_percentages,
  current_winning_pct,
  current_game_number
);
const bucketsProbs = calculateBucketsProbabilities(
  win_percentage_buckets,
  params.alpha_posterior,
  params.beta_posterior
);
const probabilities = aq.from(bucketsProbs);
```

<div class="grid grid-cols-1" style="grid-auto-rows: 600px;">
  <div class="card">${
    resize((height) => Plot.plot({
  width: 1200,
  height: 600,
  marginTop: 50,
  marginBottom: 50,
  marks: [
    Plot.axisY({ label: null, ticks: null, tickSize: 0, text: null }),
    Plot.axisX({
      label: "Win % Buckets",
      tickSize: 0,
      fill: "#26547c",
      labelOffset: 40
    }),
    Plot.lineX(probabilities, {
      x: "key",
      y: "value",
      stroke: "#f8f7ff",
      strokeWidth: 2,
      curve: "catmull-rom"
    }),
    Plot.dot(probabilities, {
      x: "key",
      y: "value",
      stroke: "#edf6f9",
      fill: "#ef476f",
      r: "value"
    }),
    Plot.ruleX(probabilities, {
      x: "key",
      y: "value",
      stroke: "#ef476f",
      strokeWidth: 7
    }),
    Plot.text(probabilities, {
      x: "key",
      y: "value",
      text: (d) => `${d.value.toFixed(1)}%`,
      lineAnchor: "bottom",
      dy: -35,
      dx: 5,
      fill: "#26547c",
      fontSize: 18,
      textAnchor: "middle",
      frameAnchor: "middle"
    })
  ]
}))
  }</div>
</div>

---

<style>

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: var(--sans-serif);
  margin: 10px 0 8px;
  text-wrap: balance;
  text-align: center;
}

.hero h1 {
  margin: 10px 0;
  padding: 10px 0;
  max-width: none;
  font-size: 20px;
  font-weight: 500;
  background: linear-gradient(30deg, var(--theme-foreground-focus), currentColor);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

@media (min-width: 640px) {
  .hero h1 {
    font-size: 90px;
  }
}

</style>
