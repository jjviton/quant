# =============================================================================
# Calculate slope of n successive points on a time series
# Author : Mayank Rasu (http://rasuquant.com/wp/)

# Please report bug/issues in the Q&A section
# =============================================================================

# Import necesary libraries
import yfinance as yf
import numpy as np
import datetime as dt
import statsmodels.api as sm

# Download historical data for required stocks
ticker = "AAPL"
ohlcv = yf.download(ticker,dt.date.today()-dt.timedelta(1825),dt.datetime.today())


ser=ohlcv["Adj Close"]   #asignando una simple diension (col or row) creamos una serie

#**********************************************************************************
def slope(ser,n):
    "function to calculate the slope of regression line for n consecutive points on a plot"
    ser = (ser - ser.min())/(ser.max() - ser.min())
    x = np.array(range(len(ser)))   #crea un array con todos los inicializados a un rango
    x = (x - x.min())/(x.max() - x.min())
    slopes = [i*0 for i in range(n-1)]  #crea un array, inicializando los valores con un for !!!
    for i in range(n,len(ser)+1):
        y_scaled = ser[i-n:i]    #va cogiendo los valores desde el final.
        x_scaled = x[i-n:i]
        x_scaled = sm.add_constant(x_scaled)
        model = sm.OLS(y_scaled,x_scaled)   #OLS es una forma de regresion.
        results = model.fit()
        slopes.append(results.params[-1])
    slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))
    return np.array(slope_angle)
#*****************************************************************************************



ohlcv["close_slope"] = slope(ohlcv["Adj Close"],5)
ohlcv.iloc[:,[4,6]].plot()


"""
def slope(ser,n):
    "function to calculate the slope of line connecting a point with n-previous point
     slope assumes a frame with 22 units in the x axis and span of min to max in y axis"
    y_span = ser.max() - ser.min()
    x_span = 22
    slopes = [i*0 for i in range(n-1)]
    for i in range(n-1,len(ser)):
        y2 = ser[i]
        y1 = ser[i-n+1]
        slope = ((y2-y1)/y_span)/(n/x_span)
        slopes.append(slope)
    slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))
    return np.array(slope_angle)

"""