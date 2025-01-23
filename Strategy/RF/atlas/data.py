import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted", rc={'figure.figsize':(25,8), "figure.dpi": 500})

class Data:
    def __init__(self, df):
        """
        Initialize the MetricsCalculator with a DataFrame.

        Parameters:
        df (pd.DataFrame): DataFrame containing the data with a 'Datetime' column.
        """
        self.df = df
        self.df['date'] = self.get_date()
        self.grouped = self.df.groupby('date')
        
        self.df = self.run_all_metrics()

    def lag(self, feature, lag=-1):
        return self.grouped[feature].shift(lag).droplevel(0)

    def get_date(self):
        """
        Extract the date from the 'Datetime' column and add it as a new column.

        Returns:
        pd.DataFrame: DataFrame with a new 'date' column.
        """
        return self.df['Datetime'].dt.date

    def calculate_delta(self):
        """
        Calculate the difference in the 'Close' column for each group.

        Returns:
        pd.DataFrame: DataFrame with a new 'delta' column.
        """
        self.df['delta'] = self.grouped['Close'].diff()
        return self.df

    def calculate_rolling_min_max(self, period=14):
        """
        Calculate rolling minimum and maximum for the 'Close' column.

        Parameters:
        period (int): The window size for calculating rolling min and max.

        Returns:
        pd.DataFrame: DataFrame with new 'low_min' and 'high_max' columns.
        """
        self.df['low_min'] = self.grouped['Close'].rolling(window=period).min().droplevel(0)
        self.df['high_max'] = self.grouped['Close'].rolling(window=period).max().droplevel(0)
        return self.df

    def log_return(self):
        """
        Calculate the log return of the 'Close' column.

        Returns:
        pd.Series: Series of log returns.
        """
        return self.grouped.apply(lambda x: np.log(x['Close'] / x['Close'].shift(1))).droplevel(0)

    def volatility(self):
        """
        Calculate the volatility as the absolute value of log returns.

        Returns:
        pd.Series: Series of volatility values.
        """
        return self.log_return().abs()

    def rsi(self, period=14):
        """
        Calculate the Relative Strength Index (RSI).

        Parameters:
        period (int): The window size for calculating RSI.

        Returns:
        pd.Series: Series of RSI values.
        """
        self.calculate_delta()
        gain = self.grouped['delta'].apply(lambda x: x.where(x > 0, 0).rolling(window=period).mean()).droplevel(0)
        loss = self.grouped['delta'].apply(lambda x: -x.where(x < 0, 0).rolling(window=period).mean()).droplevel(0)
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def stochastic_oscillator(self, period=14):
        """
        Calculate the Stochastic Oscillator.

        Parameters:
        period (int): The window size for calculating the oscillator.

        Returns:
        pd.Series: Series of Stochastic Oscillator values.
        """
        self.calculate_rolling_min_max(period)
        return self.grouped.apply(lambda x: ((x['Close'] - x['low_min']) / (x['high_max'] - x['low_min'])) * 100).droplevel(0)

    def williams_r(self, period=14):
        """
        Calculate the Williams %R indicator.

        Parameters:
        period (int): The window size for calculating Williams %R.

        Returns:
        pd.Series: Series of Williams %R values.
        """
        self.calculate_rolling_min_max(period)
        return self.grouped.apply(lambda x: ((x['high_max'] - x['Close']) / (x['high_max'] - x['low_min'])) * -100).droplevel(0)

    def ema(self, span):
        """
        Calculate the Exponential Moving Average (EMA).

        Parameters:
        span (int): The span for calculating EMA.

        Returns:
        pd.Series: Series of EMA values.
        """
        return self.grouped['Close'].apply(lambda x: x.ewm(span=span, adjust=False).mean()).droplevel(0)

    def macd(self, span1=12, span2=26, span_signal=9):
        """
        Calculate the Moving Average Convergence Divergence (MACD) and signal line.

        Parameters:
        span1 (int): The short-term EMA span.
        span2 (int): The long-term EMA span.
        span_signal (int): The signal line EMA span.

        Returns:
        tuple: Tuple containing MACD line and signal line as Series.
        """
        ema1 = self.ema(span1)
        ema2 = self.ema(span2)
        macd_line = ema1 - ema2
        self.df['macd_line'] = macd_line
        self.df['signal_line'] = self.grouped['macd_line'].apply(lambda x: x.ewm(span=span_signal, adjust=False).mean()).droplevel(0)
        return self.df['macd_line'], self.df['signal_line']

    def proc(self, n=9):
        """
        Calculate the Price Rate of Change (PROC).

        Parameters:
        n (int): The number of periods to shift for calculating PROC.

        Returns:
        pd.Series: Series of PROC values.
        """
        return self.grouped.apply(lambda x: (x['Close'] - x['Close'].shift(n)) / x['Close'].shift(n)).droplevel(0)

    def obv(self):
        """
        Calculate the On-Balance Volume (OBV).

        Returns:
        pd.Series: Series of OBV values.
        """
        return (np.sign(self.df['delta']) * self.df['Volume']).fillna(0).cumsum()

    
    def run_all_metrics(self):
        """
        Run all metric calculations and add them to the DataFrame.

        Returns:
        pd.DataFrame: DataFrame with all calculated metrics as new columns.
        """
        self.df['log_return'] = self.log_return()
        self.df['volatility'] = self.volatility()
        self.df['rsi'] = self.rsi()
        self.df['stochastic_oscillator'] = self.stochastic_oscillator()
        self.df['williams_r'] = self.williams_r()
        self.df['macd_line'], self.df['signal_line'] = self.macd()
        self.df['proc'] = self.proc()
        self.df['obv'] = self.obv()

        return self.df
    
    def plot(self, metric, kind, x='date', group=None):
        return eval(f"sns.{kind}(y=self.df[metric], x=self.df[x]).set_title('{metric.upper()}  ({self.df['date'].min()} to {self.df['date'].max()})')")



