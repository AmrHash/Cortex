from plotly import graph_objs as go
from datetime import date
import ta
import yfinance as yf
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tempfile
import io
from datetime import datetime, timedelta
plt.style.use('fivethirtyeight')

#Main part  
st.title("Cortex AI Enhanced With TA 😃")

#Geting the dataframe of selected ETH or BTC

start = '2022-01-01'
today = datetime.now().strftime("%Y-%m-%d")

st.title('Stock selection')
stocks = ("BTC-USD", "ETH-USD")
selected_stock= st.selectbox("Select Stock for Analysis", stocks)

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, start, today)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text('Load data ...')
data = load_data(selected_stock)
data_load_state.text('Loading Data... Done!')



st.subheader('Raw Data')
st.write(data.tail())

#Showing the first plot of the Closing chart


fig = go.Figure()
fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
fig.layout.update(title='Time Series data',xaxis_rangeslider_visible=True)
st.plotly_chart(fig)


######################################################################################
############## Trying TA here  ##########################################

from ta import add_all_ta_features

data = add_all_ta_features(data, open="Open", high="High", low="Low", close="Close", volume="Volume")
st.write(data)


#############################################################################

st.header('Volume Indicators')
st.header("Accumulation/Distribution Index (Acc/Dist) Visualization")


adi_indicator = ta.volume.AccDistIndexIndicator(high=data['High'], low=data['Low'], close=data['Close'], volume=data['Volume']).acc_dist_index()


st.line_chart(adi_indicator)

st.subheader("DataFrame with Acc/Dist Index")
st.write(data)


#######################################################################################################

st.header('Chaikin Money Flow')
st.text('It measures the amount of Money Flow Volume over a specific period.')
# Calculate Chaikin Money Flow (CMF)
cmf_indicator = ta.volume.ChaikinMoneyFlowIndicator(high=data['High'], low=data['Low'], close=data['Close'], volume=data['Volume']).chaikin_money_flow()

st.title("Chaikin Money Flow (CMF) Visualization")

st.line_chart(cmf_indicator)

st.subheader("DataFrame with CMF Indicator")
st.write(data)

#############################################################################################

# Calculate Ease of Movement (EoM) Indicator
eom_indicator = ta.volume.EaseOfMovementIndicator(high=data['High'], low=data['Low'], volume=data['Volume']).ease_of_movement()

st.title("Ease of Movement Indicator (EoM) Visualization")

st.header("Ease Of Movement Indicator")
st.text("The Ease of Movement Indicator (EoM) measures the relationship between price change and volume.")

st.line_chart(eom_indicator)

st.subheader("DataFrame with EoM Indicator")
st.write(data)


#######################################################################################################

# Calculate Force Index
force_index_indicator = ta.volume.ForceIndexIndicator(close=data['Close'], volume=data['Volume']).force_index()

st.title("Force Index Indicator Visualization")

st.header("Force Index Indicator")
st.text("The Force Index measures the strength behind a price move based on volume.")

st.line_chart(force_index_indicator)

st.subheader("DataFrame with Force Index Indicator")
st.write(data)


######################################################################################


# Calculate Money Flow Index (MFI)
mfi_indicator = ta.volume.MFIIndicator(high=data['High'], low=data['Low'], close=data['Close'], volume=data['Volume']).money_flow_index()

st.title("Money Flow Index (MFI) Visualization")

st.header("MFIIndicator")
st.text("The Money Flow Index (MFI) measures the strength and direction of a trend based on money flow.")

# Plot MFI
st.line_chart(mfi_indicator)

# Display the DataFrame (optional)
st.subheader("DataFrame with MFI Indicator")
st.write(data)

#########################################################################################33

# Calculate Negative Volume Index (NVI)

nvi_indicator = ta.volume.NegativeVolumeIndexIndicator(close=data['Close'], volume=data['Volume']).negative_volume_index()

st.title("Negative Volume Index (NVI) Visualization")

st.header("Negative Volume Index Indicator")
st.text("The Negative Volume Index (NVI) measures the strength of a downtrend based on negative volume changes.")

st.line_chart(nvi_indicator)

st.subheader("DataFrame with NVI Indicator")
st.write(data)


################################################################################################
# Calculate On-Balance Volume (OBV)
obv_indicator = ta.volume.OnBalanceVolumeIndicator(close=data['Close'], volume=data['Volume']).on_balance_volume()

st.title("On-Balance Volume (OBV) Visualization")

st.header("On-Balance Volume Indicator")
st.text("The On-Balance Volume (OBV) measures the strength of a trend based on the cumulative volume flow.")


st.line_chart(obv_indicator)
st.subheader("DataFrame with OBV Indicator")
st.write(data)


################################################################################################
# Calculate Volume Price Trend (VPT)
vpt_indicator = ta.volume.VolumePriceTrendIndicator(close=data['Close'], volume=data['Volume']).volume_price_trend()

st.title("Volume Price Trend (VPT) Visualization")

st.header("Volume Price Trend Indicator")
st.text("The Volume Price Trend (VPT) measures the strength of a trend based on the relationship between price and volume changes.")

st.line_chart(vpt_indicator)

st.subheader("DataFrame with VPT Indicator")
st.write(data)

################################################################################################

# Calculate Volume Weighted Average Price (VWAP)
data['VWAP'] = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()

st.title("Volume Weighted Average Price (VWAP) Visualization")

st.header("Volume Weighted Average Price (VWAP)")
st.text("The Volume Weighted Average Price (VWAP) is a measure of the average price at which a security has traded throughout the day, based on both volume and price.")

st.line_chart(data['VWAP'])

st.subheader("DataFrame with VWAP")
st.write(data)

#####################################################################################################

# Calculate Volume Price Trend (VPT)
vpt_indicator = ta.volume.VolumePriceTrendIndicator(close=data['Close'], volume=data['Volume']).volume_price_trend()

# Streamlit app for VPT
st.title("Volume Price Trend (VPT) Visualization")

# Display header and text for VPT
st.header("Volume Price Trend Indicator")
st.text("The Volume Price Trend (VPT) measures the strength of a trend based on the relationship between price and volume changes.")

# Plot VPT
st.line_chart(vpt_indicator)

# Display the DataFrame for VPT (optional)
st.subheader("DataFrame with VPT Indicator")
st.write(data)

#############################################################################33


st.title('Volatility Indicators')
##################################################################################
st.text('1')
# Calculate Average True Range (ATR)
atr_indicator = ta.volatility.AverageTrueRange(high=data['High'], low=data['Low'], close=data['Close'], window=14).average_true_range()

st.title("Average True Range (ATR) Visualization")

st.header("ta.volatility.AverageTrueRange")
st.text("The Average True Range (ATR) measures market volatility by considering price ranges.")

st.line_chart(atr_indicator)

st.subheader("DataFrame with ATR Indicator")
st.write(data)

##########################################################################################
st.text('2')
# Calculate Bollinger Bands
bb_indicator = ta.volatility.BollingerBands(close=data['Close'], window=20, window_dev=2)

st.title("Bollinger Bands Visualization")

st.header("Bollinger Bands")
st.text("Bollinger Bands consist of a middle band being an N-period simple moving average, an upper band at K times an N-period standard deviation above the middle band, and a lower band at K times an N-period standard deviation below the middle band.")

st.line_chart(bb_indicator.bollinger_mavg())
st.line_chart(bb_indicator.bollinger_hband())
st.line_chart(bb_indicator.bollinger_lband())

st.subheader("DataFrame with Bollinger Bands Indicator")
st.write(data)
###############################################################################################333
st.text('3')

# Calculate Donchian Channel
donchian_channel = ta.volatility.DonchianChannel(high=data['High'], low=data['Low'], close=data['Close'], window=20)

st.title("Donchian Channel Visualization")

st.header("Donchian Channel")
st.text("The Donchian Channel consists of three lines: the upper channel line (highest high over a given period), the lower channel line (lowest low over a given period), and the midline (average of upper and lower channel lines).")

st.line_chart(donchian_channel.donchian_channel_hband())
st.line_chart(donchian_channel.donchian_channel_lband())
st.line_chart(donchian_channel.donchian_channel_mband())

st.subheader("DataFrame with Donchian Channel Indicator")
st.write(data)
#####################################################################################################
st.text('4')
# Streamlit app for Keltner Channel
st.title("Keltner Channel Visualization")
# Calculate Keltner Channel
keltner_channel = ta.volatility.KeltnerChannel(high=data['High'], low=data['Low'], close=data['Close'], window=20, window_atr=10)


st.header("ta.volatility.KeltnerChannel")
st.text("The Keltner Channel consists of three lines: the middle line (Exponential Moving Average of closing prices), the upper channel line (EMA + ATR * multiplier), and the lower channel line (EMA - ATR * multiplier).")

st.line_chart(keltner_channel.keltner_channel_hband())
st.line_chart(keltner_channel.keltner_channel_lband())
st.line_chart(keltner_channel.keltner_channel_mband())

st.subheader("DataFrame with Keltner Channel Indicator")
st.write(data)

###################################################################
st.text('5')

# Calculate Ulcer Index
ulcer_index = ta.volatility.UlcerIndex(close=data['Close'], window=14)

# Streamlit app for Ulcer Index
st.title("Ulcer Index Visualization")

# Display header and text for Ulcer Index
st.header("ta.volatility.UlcerIndex")
st.text("The Ulcer Index measures the downside volatility and market risk based on the percentage drawdown.")

# Plot Ulcer Index
st.line_chart(ulcer_index.ulcer_index())

# Display the DataFrame for Ulcer Index (optional)
st.subheader("DataFrame with Ulcer Index Indicator")
st.write(data)

###################################################################
##################################################################
#################################################################
#######################################################################


st.title('Trend Indicators')


# Calculate Average Directional Index (ADX)
adx_indicator = ta.trend.ADXIndicator(high=data['High'], low=data['Low'], close=data['Close'], window=14)

st.title("Average Directional Index (ADX) Visualization")

st.header("ADX Indicator")
st.text("The Average Directional Index (ADX) measures the strength of a trend. It is part of the Directional Movement System.")

st.line_chart(adx_indicator.adx())

st.subheader("DataFrame with ADX Indicator")
st.write(data)

######################################################################


# Calculate Aroon Indicator
aroon_indicator = ta.trend.AroonIndicator(high=data['High'], low=data['Low'], window=14)

st.title("Aroon Indicator Visualization")

st.header("ta.trend.AroonIndicator")
st.text("The Aroon Indicator identifies the strength of a trend and helps to determine whether a stock is trending or in a range-bound market condition.")

st.line_chart(aroon_indicator.aroon_up())
st.line_chart(aroon_indicator.aroon_down())

st.subheader("DataFrame with Aroon Indicator")
st.write(data)

##########################################################################

# Calculate CCI Indicator
cci_indicator = ta.trend.CCIIndicator(high=data['High'], low=data['Low'], close=data['Close'], window=20)

st.title("Commodity Channel Index (CCI) Visualization")

st.header("CCI Indicator")
st.text("The Commodity Channel Index (CCI) measures the current price level relative to an average price level over a given period of time.")

st.line_chart(cci_indicator.cci())

st.subheader("DataFrame with CCI Indicator")
st.write(data)


#############################################################3

# Calculate DPO Indicator
dpo_indicator = ta.trend.DPOIndicator(close=data['Close'], window=20)

st.title("Detrended Price Oscillator (DPO) Visualization")

st.header("DPO Indicator")
st.text("The Detrended Price Oscillator (DPO) filters out the overall trend from the price and helps identify cycles in the market.")

st.line_chart(dpo_indicator.dpo())

st.subheader("DataFrame with DPO Indicator")
st.write(data)

################################################################33

# Calculate Exponential Moving Average (EMA)
ema_indicator = ta.trend.EMAIndicator(close=data['Close'], window=20)

st.title("Exponential Moving Average (EMA) Visualization")

st.header("EMA Indicator")
st.text("The Exponential Moving Average (EMA) gives more weight to recent prices, making it more responsive to short-term price movements.")

st.line_chart(ema_indicator.ema_indicator())

st.subheader("DataFrame with EMA Indicator")
st.write(data)

##########################################################################
# Calculate KST Indicator
kst_indicator = ta.trend.KSTIndicator(close=data['Close'], roc1=10, roc2=15, roc3=20, roc4=30, window1=10, window2=10, window3=10, window4=15)

# Streamlit app for KST Indicator
st.title("Know Sure Thing (KST) Visualization")

# Display header and text for KST Indicator
st.header("KST Indicator")
st.text("The Know Sure Thing (KST) is a momentum indicator that combines rate of change (ROC) values over different periods to provide a smoothed and more reliable trend signal.")

# Plot KST Indicator
st.line_chart(kst_indicator.kst())

# Display the DataFrame for KST Indicator (optional)
st.subheader("DataFrame with KST Indicator")
st.write(data)

######################################################################333

# Calculate MACD
macd_indicator = ta.trend.MACD(close=data['Close'], window_fast=12, window_slow=26, window_signal=9)

st.title("Moving Average Convergence Divergence (MACD) Visualization")

st.header("MACD")
st.text("The Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security's price.")

st.line_chart(macd_indicator.macd())
st.line_chart(macd_indicator.macd_signal())
st.line_chart(macd_indicator.macd_diff())

st.subheader("DataFrame with MACD Indicator")
st.write(data)
###############################################################################
# Mass Index
mass_index = ta.trend.MassIndex(high=data['High'], low=data['Low'], window_fast=9, window_slow=25)

st.title("Mass Index Visualization")

st.header("Mass Index")
st.text("The Mass Index identifies trend reversals based on changes in the trading ranges of a security. It helps to identify potential trend reversal points.")

# Plot Mass Index
st.line_chart(mass_index.mass_index())

# Display the DataFrame for Mass Index (optional)
st.subheader("DataFrame with Mass Index Indicator")
st.write(data)
##############################################################################

# Calculate Parabolic SAR
psar_indicator = ta.trend.PSARIndicator(high=data['High'], low=data['Low'], acceleration=0.02, max_acceleration=0.2)

st.title("Parabolic SAR Visualization")

st.header("ta.trend.PSARIndicator")
st.text("The Parabolic SAR (Stop and Reverse) is a trend-following indicator that provides potential reversal points for the price movement.")

st.line_chart(psar_indicator.psar())

st.subheader("DataFrame with Parabolic SAR Indicator")
st.write(data)


#######################################################################################33
######################################################################################
##################################################################################3
################# End of TREND INDICATORS ###########################################




####################################################################################33
#############3333   Start Other Indicators ####################################

st.title('Other Indicators')

# Calculate Cumulative Return
cumulative_return_indicator = ta.others.CumulativeReturnIndicator(close=data['Close'])

st.title("Cumulative Return Visualization")

st.header("Cumulative Return Indicator")
st.text("The Cumulative Return Indicator calculates the cumulative return of a financial instrument over time.")

st.line_chart(cumulative_return_indicator.cumulative_return())

st.subheader("DataFrame with Cumulative Return Indicator")
st.write(data)

#######################################################################################3

# Calculate Daily Log Return
daily_log_return_indicator = ta.others.DailyLogReturnIndicator(close=data['Close'])

# Streamlit app for Daily Log Return
st.title("Daily Log Return Visualization")

# Display header and text for Daily Log Return
st.header("ta.others.DailyLogReturnIndicator")
st.text("The Daily Log Return Indicator calculates the logarithmic daily return of a financial instrument.")

# Plot Daily Log Return
st.line_chart(daily_log_return_indicator.daily_log_return())

# Display the DataFrame for Daily Log Return (optional)
st.subheader("DataFrame with Daily Log Return Indicator")
st.write(data)


######################################################################################3

st.title('Momentum Technical Analysis')



st.header('Kaufmans Adaptive Moving Average (KAMA)')
st.text('Moving average designed to account for market noise or volatility. KAMA will closely follow prices when the price swings are relatively small and the noise is low. KAMA will adjust when the price swings widen and follow prices from a greater distance. This trend-following indicator can be used to identify the overall trend, time turning points and filter price movements.')




# Calculate KAMA
kama_indicator = ta.momentum.KAMAIndicator(close=data['Close'], window=10, pow1=2, pow2=30).kama()

# Streamlit app
st.title("KAMA Indicator Visualization")

# Plot KAMA
st.line_chart(kama_indicator)

st.subheader("DataFrame with KAMA Indicator")
st.write(data)


