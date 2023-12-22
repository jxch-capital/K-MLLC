import ta.wrapper
import numpy as np


class HLC3:
    @staticmethod
    def hlc3_hlc(high, low, close):
        return (high + low + close) / 3

    @staticmethod
    def hlc3_lc(high, low, close):
        return (high + 2 * low + 2 * close) / 5

    @staticmethod
    def hlc3_c(high, low, close):
        return (high + low + 2 * close) / 4


class FeaturesX:
    def __init__(self, name, values):
        self.name = name
        self.values = values


class FeaturesDefinition:
    def __init__(self, features=None):
        if features is None:
            self.features = []
        else:
            self.features = features

    def add_feature(self, name, values):
        self.features.append(FeaturesX(name, values))

    def all_features(self):
        return self.features

    def features_names(self):
        return [f.name for f in self.features]

    def features_num(self):
        return len(self.features)

    @staticmethod
    def default(high=None, low=None, close=None, open=None, vol=None):
        features_definition = FeaturesDefinition()
        features_definition.add_feature('WT-10-11-hlc', n_wt(high, low, close, 10, 11, HLC3.hlc3_c))
        features_definition.add_feature('ADX-20', n_adx(high, low, close, 20, 2))
        features_definition.add_feature('RSI-14', n_rsi(close, 14, 1))
        features_definition.add_feature('RSI-9', n_rsi(close, 9, 1))
        features_definition.add_feature('CCI-20', n_cci(close, 20, 1))
        # features_definition.add_feature('MACD-26-12-9', n_macd_diff(close, 26, 12, 9))
        # features_definition.add_feature('MACD-52-24-18', n_macd_diff(close, 52, 24, 18))
        # features_definition.add_feature('OBV-3', n_obv(close, vol, 3))
        return features_definition

    def calculate(self, df):
        for feature in self.all_features():
            df[feature.name] = feature.values
        df.dropna(axis=0, how='any', inplace=True)
        return df


def pad0(values, n):
    return np.pad(values, (n, 0), 'constant', constant_values=0)


def n_rsi(price, rsi_n, rsi_sma_n):
    rsi_values = ta.wrapper.RSIIndicator(close=price, window=rsi_n).rsi()
    return ta.wrapper.SMAIndicator(rsi_values, window=rsi_sma_n).sma_indicator()


def n_cci(price, cci_n, cci_sma_n):
    cci_values = ta.wrapper.CCIIndicator(high=price, low=price, close=price, window=cci_n).cci()
    return ta.wrapper.SMAIndicator(cci_values, window=cci_sma_n).sma_indicator()


def n_adx(high, low, close, adx_n, adx_sma_n):
    adx_values = ta.wrapper.ADXIndicator(high=high, low=low, close=close, window=adx_n).adx()
    return ta.wrapper.SMAIndicator(adx_values, window=adx_sma_n).sma_indicator()


def n_wt(high, low, close, rsi_n, wt_sma_n, hlc3_func=HLC3.hlc3_hlc):
    hlc3 = hlc3_func(high, low, close)
    rsi = ta.wrapper.RSIIndicator(close=hlc3, window=rsi_n).rsi()
    rsi_smooth = ta.wrapper.SMAIndicator(close=rsi, window=wt_sma_n).sma_indicator()
    rsi_double_smooth = ta.wrapper.SMAIndicator(close=rsi_smooth, window=wt_sma_n).sma_indicator()
    wt = rsi_double_smooth - rsi_smooth
    return ta.wrapper.SMAIndicator(close=wt, window=wt_sma_n).sma_indicator()


def n_macd_diff(price, window_slow=26, window_fast=12, window_sign=9):
    return ta.wrapper.MACD(close=price, window_slow=window_slow, window_fast=window_fast,
                           window_sign=window_sign).macd_diff().values


def n_obv(close, vol, n_obv):
    obv_values = ta.wrapper.OnBalanceVolumeIndicator(close=close, volume=vol).on_balance_volume()
    return ta.wrapper.SMAIndicator(obv_values, window=n_obv).sma_indicator()

