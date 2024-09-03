import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import yfinance as yf
from scipy.stats import linregress

class MonteCarlo:

    def __init__(self, user_stocks_input, user_shock, annual_risk_free_rate):
        self.user_stocks_input = user_stocks_input
        self.user_shock = user_shock
        self.annual_risk_free_rate = annual_risk_free_rate
        self.sp500 = None
        # self.bootstraped_sp500 = []
        self.user_stocks_str = []
        self.user_stocks = []
        self.betas_for_portfolio = []
        # self.weights = []
        self.mc_port_returns = []
        self.mc_port_vol = []
        self.mc_port_weights = []
        self.mc_sharpe_ratios = []

    def create_user_stocks_str (self):
        self.user_stocks_str = self.user_stocks_input.strip(" ").split(" ")
    
    def create_user_stocks(self):
        self.user_stocks = []
        for stock in self.user_stocks_str:
            try:
                data = yf.download(stock, start='2006-01-01')
                if data.empty:
                    raise ValueError(f"No data found for stock: {stock}")
                self.user_stocks.append(data)
            except Exception as e:
                raise ValueError(f"Error downloading data for stock {stock}: {e}")

        for stock in self.user_stocks:
            stock['Log Returns'] = np.log(stock['Adj Close'] / stock['Adj Close'].shift(1))
            stock.dropna(inplace=True)    


    # def create_user_stocks (self):
    #     for stock in self.user_stocks_str:
    #         data = yf.download(stock, start='2006-01-01')
    #         self.user_stocks.append(data)

    #     for stock in self.user_stocks:
    #         stock['Log Returns'] = np.log(stock['Adj Close']/stock['Adj Close'].shift(1))
    #         stock.dropna(inplace=True)

    def create_sp500 (self):
        self.sp500 = yf.download("^GSPC", start = '2006-01-01')
        self.sp500['Log Returns'] = np.log(self.sp500['Adj Close']/self.sp500['Adj Close'].shift(1))
        self.sp500.dropna(inplace=True)

    def create_betas_for_portfolio(self):
        for stock in self.user_stocks:
            # stock_start_date = stock.index[0].date()
            # stock_end_date = stock.index[stock.shape[0]-1].date()
            stock_start_date = "2022-01-01"
            beta,_,_,_,_ = linregress(self.sp500['Log Returns'][stock_start_date:],stock['Log Returns'][stock_start_date:])
            self.betas_for_portfolio.append(beta)

        self.betas_for_portfolio = np.array(self.betas_for_portfolio)

    def bootstrap(self):
        data = np.random.choice(self.sp500['Log Returns'], size=630, replace=True)
        return pd.DataFrame(data, columns=['Log Returns'])
    
    def simulate_sp500(self, bootstraped_sp500):
        shock = self.user_shock * 2.5
        daily_shock = (1 + shock) ** (1/630) - 1

        for i in range (0,630):
            bootstraped_sp500.iloc[i] += daily_shock

    def calculate_returns(self, weights):
        past_year_sp500_copy = self.bootstrap()
        self.simulate_sp500(past_year_sp500_copy)
        self.betas_for_portfolio = np.array(self.betas_for_portfolio).reshape(1, len(self.user_stocks_str))
        past_year_sp500_copy = past_year_sp500_copy.values.reshape(630, 1)
        portfolio_returns_after_shock = self.betas_for_portfolio * past_year_sp500_copy 
        portfolio_returns_after_shock = pd.DataFrame(portfolio_returns_after_shock, columns=self.user_stocks_str)
        portfolio_annual_return = (np.sum(portfolio_returns_after_shock.mean() * weights) * 252) - self.annual_risk_free_rate
        return portfolio_annual_return, portfolio_returns_after_shock
    
    def calculate_volatility(self, weights, df_portfolio_returns_after_shock):
        annualized_cov = np.dot(df_portfolio_returns_after_shock.cov()*252, weights)
        vol = np.dot(weights.transpose(),annualized_cov)
        return np.sqrt(vol)
    
    def generate_weights (self, n):
        weights = np.random.random(n)
        return weights / np.sum(weights)
    
    def simulate (self, n):
        self.mc_port_returns = []
        self.mc_port_vol = []
        self.mc_port_weights = []
        self.mc_sharpe_ratios

        for i in range(n):
            sim_weights = self.generate_weights(len(self.user_stocks_str))
            self.mc_port_weights.append(sim_weights)
            sim_returns, sim_port_after_shock = self.calculate_returns(sim_weights)
            self.mc_port_returns.append(sim_returns)
            sim_vol = self.calculate_volatility(sim_weights, sim_port_after_shock)
            self.mc_port_vol.append(sim_vol)

        self.mc_sharpe_ratios = np.array(self.mc_port_returns)/np.array(self.mc_port_vol)

    def create_graph(self):
        fig = plt.figure(dpi=200,figsize=(10,5))
        plt.scatter(self.mc_port_vol,self.mc_port_returns,c=self.mc_sharpe_ratios)
        plt.colorbar(label='SHARPE RATIO')
        plt.xlabel('VOL')
        plt.ylabel('RETURNS')
        return fig
