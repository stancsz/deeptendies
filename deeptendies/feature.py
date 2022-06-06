class Feature:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def get_x_low(df, x=52, interval='day', **kwargs):
        if interval == 'week':
            x_inter = x * 7
        elif interval == 'day':
            x_inter = x
        df[f'{x}_{interval}_low'] = df['low'].rolling(window=x_inter, min_periods=x_inter).min()
        return df

    @staticmethod
    def get_x_high(df, x=52, interval='day', **kwargs):
        if interval == 'week':
            x_inter = x * 7
        elif interval == 'day':
            x_inter = x
        df[f'{x}_{interval}_high'] = df['high'].rolling(window=x_inter, min_periods=x_inter).max()
        return df

    @staticmethod
    def get_x_ma(df, x=50, interval='day', **kwargs):
        if interval == 'week':
            x_inter = x * 7
        elif interval == 'day':
            x_inter = x
        df[f'{x}_{interval}_ma'] = df['close'].rolling(window=x_inter, min_periods=x_inter).mean()
        return df

    @staticmethod
    def get_diff(df, cols=['high', 'low', 'close', 'volume'], **kwargs):
        for col in cols:
            df[f'{col}_diff'] = df[col].diff()
        return df

    @staticmethod
    def rsi(df, close_col='adj_close', return_format='df', periods=14):
        """
        rsi method for calculating the RSI. Takes a dataframe, default close_col to the
        data retrieved from yahoo via yfinance library.
        usage example:
            df['rsi'] = rsi(df)
        https://www.investopedia.com/terms/r/rsi.asp
        :param return_format: default to df, else return rsi series
        :param df:
        :param close_col:
        :param periods:
        :return:
        """
        diff = df[close_col].diff().dropna()
        gain = diff * 0
        loss = diff * 0
        gain[diff > 0] = diff[diff > 0]
        loss[diff < 0] = diff[diff < 0]
        average_gain = gain.ewm(com=periods - 1, min_periods=periods).mean()
        average_loss = loss.ewm(com=periods - 1, min_periods=periods).mean()
        average_gain_loss_ratio = abs(average_gain / average_loss)
        rsi = 100 - (100 / (1 + average_gain_loss_ratio))
        if return_format == 'df':
            df['rsi'] = rsi
            return df
        return rsi

    @staticmethod
    def macd(df, close_col='adj_close'):
        """
        compute the macd inplace
        :param df:
        :param close_col:
        :return: a df with macd, signal, hist values
        """
        df['ema_12'] = df[close_col].ewm(span=26, adjust=False).mean()
        df['ema_26'] = df[close_col].ewm(span=12, adjust=False).mean()
        df['macd'] = df['ema_26'] - df['ema_12']
        df['macd_9_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        df['macd_hist'] = df['macd'] - df['macd_9_signal']
        return df
