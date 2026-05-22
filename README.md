For this project I wanted to answer whether first dragon or void grubs is the better objective in the LPL, and whether Blue or Red side changes that answer.

I pulled the 2026 Oracle's Elixir dataset into PostgreSQL, wrote SQL views to clean and transform the data, then used Python to run a proper A/B test with chi-squared statistics and confidence intervals. The results were pretty decisive — first dragon carries a +22.3 percentage point win rate swing and is statistically significant on both sides (p<0.001). Void grubs barely move the needle at +4.5pp and don't clear the significance threshold at all.
The most interesting finding was around Blue side specifically. Red side gets first dragon 62% of the time due to map layout, but the win rate impact is identical for both sides — meaning the objective itself is genuinely valuable, not just a byproduct of being in a stronger position. When Blue side does manage to steal it, they win 66% of the time, the highest of any scenario in the data.
I packaged everything into a formatted Excel summary and a three-page Power BI dashboard. If you're drafting for the LPL, prioritise dragon.

<img width="2027" height="1063" alt="image" src="https://github.com/user-attachments/assets/ad08ed78-8061-420f-97b1-8510f2d6c533" />

<img width="1325" height="765" alt="image" src="https://github.com/user-attachments/assets/b16c94b3-2892-4cb5-b183-f026f57dd841" />
