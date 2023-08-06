import pandas as pd

github_repo = 'https://raw.githubusercontent.com/maegm/intro-portfolio-construction/master/'


def drawdown(return_series: pd.Series):
    """Takes a time series of asset returns.
       returns a DataFrame with columns for
       the wealth index, 
       the previous peaks, and 
       the percentage drawdown
    """
    wealth_index = 1000*(1+return_series).cumprod()
    previous_peaks = wealth_index.cummax()
    drawdowns = (wealth_index - previous_peaks)/previous_peaks
    return pd.DataFrame({"Wealth": wealth_index, 
                         "Previous Peak": previous_peaks, 
                         "Drawdown": drawdowns})


def get_ffme_returns(columns=None):
    """
    Load the Fama-French Dataset for the returns of the Top and Bottom Deciles by MarketCap
    """
    if columns is None:
        columns = ['Lo 10', 'Hi 10']
    me_m = pd.read_csv(github_repo + "data/Portfolios_Formed_on_ME_monthly_EW.csv",
                       header=0, index_col=0, na_values=-99.99)
    rets = me_m[columns]
    rets.columns = ['SmallCap', 'LargeCap']
    rets = rets / 100
    rets.index = pd.to_datetime(rets.index, format="%Y%m").to_period('M')
    return rets
