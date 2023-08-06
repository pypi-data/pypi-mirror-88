# -*- coding: utf-8 -*-

import math

import numpy as np
import pandas as pd

from PyFin.Math.Accumulators.StatefulAccumulators import MovingMaxDrawdown


class PerfCalc:

    def __init__(self, freq="W"):
        if freq.lower() == "w":
            self._time_factor = math.sqrt(52)
        elif freq.lower() == "m":
            self._time_factor = math.sqrt(12)
        elif freq.lower() == "d":
            self._time_factor = math.sqrt(252)
        else:
            raise ValueError(f"wrong freq <{freq}>")

    def calc(self, data: pd.DataFrame, ret_type: str = 'log'):
        data = self._ret_transform(data.copy(), ret_type)
        returns = data.groupby('trade_date')['weighted_return'].sum().fillna(0)
        benchmark_returns = data.groupby('trade_date')['weighted_benchmark_return'].sum().fillna(0)

        portfolio = self._cal_portfolio(returns, benchmark_returns)
        risk_analysis = self._cal_risk_analysis(returns)
        alpha_beta = self._cal_alpha_beta(returns, benchmark_returns)

        results = dict()
        results.update(portfolio)
        results.update(risk_analysis)
        results.update(alpha_beta)
        return results

    @staticmethod
    def _ret_transform(data: pd.DataFrame, ret_type: str):
        if ret_type == 'log':
            data['return'] = np.exp(data['return']) - 1.
            data['benchmark_return'] = np.exp(data['benchmark_return']) - 1.
        data['weighted_return'] = data['weight'] * data['return']
        data['weighted_benchmark_return'] = data['weight'] * data['benchmark_return']
        data['weighted_excess_return'] = data['weighted_return'] - data['weighted_benchmark_return']
        return data

    @staticmethod
    def _cal_portfolio(returns, benchmark_returns):
        portfolio = (returns + 1.).cumprod()
        benchmark_portfolio = (benchmark_returns + 1.).cumprod()
        month_profit = (returns + 1.).resample('M').prod() - 1
        return dict(
            portfolio=portfolio,
            benchmark_portfolio=benchmark_portfolio,
            month_profit=month_profit,
            total_returns=portfolio.values[-1]
        )

    def _cal_risk_analysis(self, returns):

        annual_volatility = returns.std() * self._time_factor
        annual_downside_risk = returns[returns < 0.].std() * self._time_factor

        calculator = MovingMaxDrawdown(len(returns), 'ret')

        for ret in returns:
            calculator.push(dict(ret=np.log(1. + ret)))

        max_drawdown = math.exp(calculator.result()) - 1.

        annual_return = returns.mean() * self._time_factor ** 2
        sharpe = annual_return / annual_volatility
        sortino = annual_return / annual_downside_risk
        return dict(
            annual_downside_risk=annual_downside_risk,
            annual_volatility=annual_volatility,
            max_drawdown=max_drawdown,
            sharpe=sharpe,
            sortino=sortino,
        )

    def _cal_alpha_beta(self, returns, benchmark_returns):
        x = np.concatenate(
            [np.ones((len(benchmark_returns), 1)), benchmark_returns.values.reshape((-1, 1))],
            axis=1)
        y = returns.values.reshape((-1, 1))

        coefs = np.linalg.solve(x.T @ x, x.T @ y)
        alpha, beta = coefs[:, 0]
        resid = coefs[:, 0] @ x.T
        information_ratio = alpha / resid.std() * self._time_factor
        return dict(
            alpha=alpha*self._time_factor**2,
            beta=beta,
            information_ratio=information_ratio
        )


if __name__ == "__main__":

    # Generate random data for example
    np.random.seed()

    trade_dates = pd.date_range("2005-01-01", "2020-07-10", freq="1W")
    security_codes = [f"{i + 1:06d}" for i in range(800)]

    records = []
    for trade_date in trade_dates:
        benchmark_return = np.random.randn() / 10.
        for security_code in security_codes:
            record = (trade_date, security_code, np.random.rand(), np.random.randn() / 10., np.random.randint(1, 20),
                      benchmark_return)
            records.append(record)

    data = pd.DataFrame(records, columns=["trade_date", "security_code", "weight", "return", "industry_code",
                                          'benchmark_return'])
    data['weight'] = data.groupby('trade_date').apply(lambda x: x['weight'] / x['weight'].sum()).values

    # Real calculation for demo
    calculator = PerfCalc(freq='W')
    res = calculator.calc(data, 'log')
    print(res)