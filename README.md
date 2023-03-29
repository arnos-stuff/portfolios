# Installation

## Requirements

- [Python 3.8](https://python.org) or higher
- Any computer with a decent CPU
- Access to a terminal (if you're on Windows please download [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?activetab=pivot:overviewtab))

## Installation

If you just want to run the code, you can install the dependencies with:

```bash
pip install portfolios
```

If you want to contribute to the project, you can install the whole thing with:

```bash
git clone 


# Portfolio Optimization Experiments

I've been interested in finance for a long time, but I've never had the
opportunity to learn about it in a structured way. This idea came to me
after a twitter mutual mentioned that french state pensions had to be better
in terms of revenue for middle class people compared to S&P 500. I was curious
about how to compare the two, and I started to learn about financial concepts
such as volatility, risk, and return. I also wanted to learn about how to compare
metrics such as the IRR via the Sharpe ratio, and how to compare risk-free assets
such as french pensions to risky assets such as S&P 500.

The experiments can be found on [GitHub](https://github.com/arnos-stuff/portfolios),
and the results are published in sections of [my optimization book](https://optim.arnov.dev)
(which is also open source).

## Main tools (for now)

- [Pandas](https://pandas.pydata.org/)
- [Numpy](https://numpy.org/)
- [CVXPY](https://www.cvxpy.org/)
- [Plotly](https://plotly.com/python/)

## Upcoming experiments

- Model the french pension system as an asset & compare it to S&P 500
- Estimate risk aversion from historical data
- Calculate the tradeoff curve for the french pension system

## Contributors

- [Arno](https://twitter.com/arno_shae)
- [Max](https://twitter.com/max_oikonomikos)
