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


def pad0(values, n):
    return np.pad(values, (n, 0), 'constant', constant_values=0)


def n_rsi(price, rsi_n, rsi_sma_n):
    rsi_values = ta.wrapper.RSIIndicator(close=price, window=rsi_n).rsi()
    return ta.wrapper.SMAIndicator(rsi_values, window=rsi_sma_n).sma_indicator()


def n_cci(price, cci_n, cci_sma_n):
    cci_values = ta.wrapper.CCIIndicator(high=price, low=price, close=price, window=cci_n).cci()
    return ta.wrapper.SMAIndicator(cci_values, window=cci_sma_n).sma_indicator()


def n_adx(high, low, close, adx_n):
    return ta.wrapper.ADXIndicator(high=high, low=low, close=close, window=adx_n).adx()


def n_wt(high, low, close, rsi_n, wt_sma_n, hlc3_func=HLC3.hlc3_hlc):
    hlc3 = hlc3_func(high, low, close)
    rsi = ta.wrapper.RSIIndicator(close=hlc3, window=rsi_n).rsi()
    rsi_smooth = ta.wrapper.SMAIndicator(close=rsi, window=wt_sma_n).sma_indicator()
    rsi_double_smooth = ta.wrapper.SMAIndicator(close=rsi_smooth, window=wt_sma_n).sma_indicator()
    wt = rsi_double_smooth - rsi_smooth
    return ta.wrapper.SMAIndicator(close=wt, window=wt_sma_n).sma_indicator()
