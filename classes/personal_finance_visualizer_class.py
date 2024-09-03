import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calendar

class MyData:
    def __init__(self, sheet_id):
        self.df = pd.read_csv(sheet_id, parse_dates=['Date'])
        self.df["Month"] = self.df["Date"].dt.month_name()
        self.df['Year'] = self.df["Date"].dt.year
        self.months = list(calendar.month_name)[1:]

    def print_df(self):
        return self.df

    def total_expenses_pie(self):
        total_price = [self.df[self.df["Catergory"] == i]['Price'].sum() for i in self.df['Catergory'].unique()]
        fig, ax = plt.subplots()
        ax.pie(total_price, labels=self.df['Catergory'].unique(), autopct='%1.0f%%')
        ax.set_title("Total Expenses Pie Chart")
        return fig

    def expenses_for_year(self, year):
        month_totals = [self.df[(self.df['Month'] == month) & (self.df['Year'] == year)]['Price'].sum() for month in self.months]
        fig, ax = plt.subplots(figsize=(15, 10), dpi=300)
        ax.plot(self.months, month_totals, marker="o", linewidth=2)
        ax.set_title(f"Expenses for {year}", fontsize=18)
        ax.set_xlabel("Months", fontsize=13)
        ax.set_ylabel("Price", fontsize=13)
        for i in range(12):
            if i > 0 and month_totals[i] > month_totals[i-1]:
                ax.annotate(round(month_totals[i], 2), (self.months[i], month_totals[i]), xytext=(self.months[i], month_totals[i] + 12))
            else:
                ax.annotate(round(month_totals[i], 2), (self.months[i], month_totals[i]), xytext=(self.months[i], month_totals[i] - 15), horizontalalignment='right')
        return fig

    def catergorical_expenses_per_month_for_a_year(self, catergories, year):
        fig, ax = plt.subplots(figsize=(15, 10))
        bar_width = 0.2
        x = range(len(self.months))
        for i, catergory in enumerate(catergories):
            monthly_catergory_totals = [self.df[(self.df['Month'] == month) & (self.df['Catergory'] == catergory) & (self.df['Year'] == year)]['Price'].sum() for month in self.months]
            ax.bar([pos + i * bar_width for pos in x], monthly_catergory_totals, width=bar_width, label=catergory)
        ax.legend(catergories, loc="upper right")
        ax.set_xlabel("Months", fontsize=13)
        ax.set_ylabel("Expenditures", fontsize=13)
        ax.set_title("Categorical Expenditures per Month", fontsize=15)
        ax.set_xticks([pos + len(self.df['Catergory'].unique()) * bar_width / 2 for pos in x])
        ax.set_xticklabels(self.months)
        return fig

    def get_years(self):
        return self.df['Year'].unique()

    def unique_catergories(self):
        return self.df['Catergory'].unique()