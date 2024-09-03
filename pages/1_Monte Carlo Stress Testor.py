import sys
import os
import streamlit as st

sys.path.append("/Users/tharun/Documents/Personal/Coding")

from my_app.classes.monte_carlo_class import MonteCarlo

st.title("Monte Carlo Project")
user_stocks = st.text_input("Enter stock codes with a space: ")
user_shock = st.number_input("Enter the shock you would like: ")
risk_free_rate = st.number_input("Enter the risk free rate: ")
simulations = st.number_input("Enter the number of simulations you would like to run (1000 sims takes approximately 30 seconds): ", format="%d", step=1)
simulations = int(simulations)

if st.button("Run Simulation"):
    if not user_stocks:
        st.error("Stock codes are required.")
    elif risk_free_rate < 0:
        st.error("Risk free rate must be non-negative.")
    else:
        try:
            mc = MonteCarlo(user_stocks, user_shock, risk_free_rate)
            mc.create_user_stocks_str()
            mc.create_user_stocks()
            mc.create_sp500()
            mc.create_betas_for_portfolio()
            mc.simulate(simulations)
            st.pyplot(mc.create_graph())
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.markdown("---")
st.subheader("Ongoing Development")
st.write('''
Currently developing an algorithm that allows users to select a desired volatility level, and the program will calculate
          and output the optimal portfolio weights to achieve the highest Sharpe ratio.

''')
