# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 16:13:03 2021

@author: jpugazhendhi
"""


import pandas as pd
import numpy as np
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt  # 2D plotting
from bs4 import BeautifulSoup
import requests
import ssl
import difflib as dfl
import re
import statsmodels.formula.api as smf
from pandasql import sqldf  
import itertools

shipping = pd.read_csv("C:\py\Logistics.csv")

shipping['dispatch_month'] = pd.to_datetime(shipping['dispatch_date']).dt.strftime('%b')
shipping['dispatch_year'] = pd.to_datetime(shipping['dispatch_date']).dt.strftime('%Y')
shipping['dispatch_date'] = pd.to_datetime(shipping['dispatch_date'])
shipping['estimated_ship_date'] = pd.to_datetime(shipping['estimated_ship_date'])
shipping['delivered_date'] = pd.to_datetime(shipping['delivered_date'])


##### Adding Season to disptah date #####

#def season_of_date(date):
#    year = str(date.year)
#    seasons = {'spring': pd.date_range(start='21/03/'+year, end='20/06/'+year),
#               'summer': pd.date_range(start='21/06/'+year, end='22/09/'+year),
#               'autumn': pd.date_range(start='23/09/'+year, end='20/12/'+year)}
#    if date in seasons['spring']:
#        return 'spring'
#    if date in seasons['summer']:
#        return 'summer'
#    if date in seasons['autumn']:
#        return 'autumn'
#    else:
#        return 'winter'

# Assuming df has a date column of type `datetime`
##shipping['season'] = shipping.dispatch_date.map(season_of_date)


### Reading from website for crude prices ###
table1 = pd.read_html("https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=RWTC&f=M")

crude_prices = table1[5]
crude_prices.dropna(axis=0, how='any', inplace=True)
crude_prices=sqldf('select * from crude_prices where Year>2014')
crude_prices_new=crude_prices.melt(id_vars=["Year"])
crude_prices_new.columns=['Year','Month','crude_price']


##### reading from website for inflation
table2=pd.read_html("https://www.usinflationcalculator.com/inflation/current-inflation-rates/")
inflation=table2[0]

inflation.columns = inflation.iloc[0]
inflation = inflation.iloc[1: , :]

inflation_new=inflation.melt(id_vars=["Year"])
inflation_new = inflation_new.rename(columns={'Year': 'Year', 'O': 'Month', 'value':'rate'})
inflation_new.columns=['Year','Month','inflation_rate']
inflation_new.dropna(axis=0, how='any', inplace=True)




##### joining all 3 datasets ###

shipping_final1=sqldf('select a.*,b.crude_price from shipping a left join crude_prices_new b on a.dispatch_year=b.Year and a.dispatch_month=b.Month  ')
shipping_final2=sqldf('select a.*,b.inflation_rate from shipping_final1 a left join inflation_new b on a.dispatch_year=b.Year and a.dispatch_month=b.Month  ')
shipping_final=sqldf('select * from shipping_final2')

shipping.dtypes
shipping_final.dtypes

shipping_final['dispatch_date'] = pd.to_datetime(shipping_final['dispatch_date'])
shipping_final['estimated_ship_date'] = pd.to_datetime(shipping_final['estimated_ship_date'])
shipping_final['delivered_date'] = pd.to_datetime(shipping_final['delivered_date'])



shipping_final['days_delayed'] = (shipping_final['dispatch_date'] - shipping_final['estimated_ship_date']).dt.days
shipping_final['shipping_days'] = (shipping_final['delivered_date'] - shipping_final['dispatch_date']).dt.days



shipping_final=sqldf('select *,case when days_delayed<0 then 0 else days_delayed end as days_delayed_final from shipping_final ')

shipping_zip_metrics_2021=sqldf('select to_zipcode,avg(cost_after_adjustment) as cost_after_adjustment,max(shipping_days) as max_shipping_days,avg(shipping_days) as shipping_days,avg(pallets) as pallets, avg(crude_price) as crude_price, avg(inflation_rate) as inflation_rate,avg(layover_duration) as layover_duration,avg(days_delayed_final) as days_delayed from shipping_final where dispatch_year=2021 group by to_zipcode ')
shipping_zip_metrics_2020=sqldf('select to_zipcode,avg(cost_after_adjustment) as cost_after_adjustment,max(shipping_days) as max_shipping_days,avg(shipping_days) as shipping_days,avg(pallets) as pallets, avg(crude_price) as crude_price, avg(inflation_rate) as inflation_rate,avg(layover_duration) as layover_duration,avg(days_delayed_final) as days_delayed from shipping_final where dispatch_year=2020 group by to_zipcode ')


shipping_final['dispatch_month_year'] = pd.to_datetime(shipping_final['dispatch_date']).dt.strftime('%b-%Y')
#shipping_final['dispatch_year'] = pd.to_datetime(shipping_final['dispatch_date']).dt.strftime('%Y')
shipping_final['dispatch_month_date'] = pd.to_datetime(shipping_final['dispatch_date']).dt.strftime('%Y-%m-'+'01')

distinct=sqldf('select to_zipcode,count(distinct dispatch_month_year),count(dispatch_month_year) from shipping_final where dispatch_year>=2018 and dispatch_year<=2021 group by to_zipcode order by 2,3 '  )

#shipping_new=sqldf('select * from shipping_final where to_zipcode in (77040,76548,98346,44305,77833,30004,78602,77073,55433) and dispatch_year>=2018 and dispatch_year<=2021 ')
shipping_new=shipping_final
#####################################################################

###################### Exploratory analysis #####
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


import plotly.express as px

fig = px.choropleth(shipping_final, geojson=counties, locations='to_zipcode', color='days_delayed',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           scope="usa",
                           labels={'Days delayed by destinatin zip'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

fig = px.choropleth(shipping_zip_metrics_2021, geojson=counties, locations='to_zipcode', color='days_delayed',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           scope="usa",
                           labels={'Days delayed by destinatin zip'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

fig = px.choropleth(shipping_final, geojson=counties, locations='to_zipcode', color='cost_after_adjustment',
                           color_continuous_scale="Viridis",
                           ##range_color=(0, 2000),
                           scope="usa",
                           labels={'Cost by Destination Zip'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

fig = px.choropleth(shipping_final, geojson=counties, locations='to_zipcode', color='shipping_days',
                           color_continuous_scale="Viridis",
                           range_color=(0, 60),
                           scope="usa",
                           labels={'shipping days '}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


########################## Trends ####

shipping_final['dispatch_month_year'] = pd.to_datetime(shipping['dispatch_date']).dt.strftime('%b-%Y')
shipping['dispatch_year'] = pd.to_datetime(shipping['dispatch_date']).dt.strftime('%Y')
shipping_final['dispatch_month'] = pd.to_datetime(shipping['dispatch_date']).dt.strftime('%Y-%m-'+'01')

ordered_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


delay_inf_crude=sqldf('select dispatch_year,dispatch_month,avg(days_delayed_final) as days_delayed,avg(cost_after_adjustment) as cost_after_adjustment,max(shipping_days) as max_shipping_days,avg(shipping_days) as shipping_days,avg(pallets) as pallets, avg(crude_price) as crude_price, avg(inflation_rate) as inflation_rate,avg(layover_duration) as layover_duration from shipping_final group by dispatch_year,dispatch_month order by dispatch_year asc')

delay_inf_crude['to_sort']=delay_inf_crude['dispatch_month'].apply(lambda x:ordered_months.index(x))
delay_inf_crude = delay_inf_crude.sort_values('to_sort')

## Crude Price Trend
fig = px.line(delay_inf_crude, x='dispatch_month', y="crude_price", color='dispatch_year')
fig.show()

## INflation
fig = px.line(delay_inf_crude, x='dispatch_month', y="inflation_rate", color='dispatch_year')
fig.show()

## shipping days
fig = px.line(delay_inf_crude, x='dispatch_month', y="shipping_days", color='dispatch_year')
fig.show()

## Max shipping days
fig = px.line(delay_inf_crude, x='dispatch_month', y="max_shipping_days", color='dispatch_year')
fig.show()

## Max shipping days
fig = px.line(delay_inf_crude, x='dispatch_month', y="cost_after_adjustment", color='dispatch_year')
fig.show()

#### Trend metrics for year 2021 ##### 

metrics_2020=sqldf('select * from delay_inf_crude where dispatch_year=2020')
fig = px.line(metrics_2020, x='dispatch_month', y=metrics_2020.columns[3:8])
fig.show()

#################### Time Series Models #####################


df=sqldf('select dispatch_month_date as Date,avg(cost_after_adjustment) as Orders from shipping_new group by dispatch_month_date order by dispatch_month_date asc')

#df=sqldf('select dispatch_month_date as Date,count(1) as Orders from shipping_new group by dispatch_month_date order by dispatch_month_date asc')
#costs=sqldf('select dispatch_month_date as date,to_zipcode,avg(cost_after_adjustment) as avg_cost from shipping_final group by dispatch_date,to_zipcode order by dispatch_date asc')

df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')

import warnings
import matplotlib.pyplot as plt
y = df['Orders']
fig, ax = plt.subplots(figsize=(20, 6))
ax.plot(y,marker='.', linestyle='-', linewidth=0.5, label='Monthly')
ax.set_ylabel('Orders')
ax.legend();


import statsmodels.api as sm

# graphs to show seasonal_decompose
def seasonal_decompose (y):
    decomposition = sm.tsa.seasonal_decompose(y, model='additive',extrapolate_trend='freq')
    fig = decomposition.plot()
    fig.set_size_inches(14,7)
    plt.show()


seasonal_decompose(y)


def test_stationarity(timeseries, title):
    
    #Determing rolling statistics
    rolmean = pd.Series(timeseries).rolling(window=12).mean() 
    rolstd = pd.Series(timeseries).rolling(window=12).std()
    
    fig, ax = plt.subplots(figsize=(16, 4))
    ax.plot(timeseries, label= title)
    ax.plot(rolmean, label='rolling mean');
    ax.plot(rolstd, label='rolling std (x10)');
    ax.legend()

pd.options.display.float_format = '{:.8f}'.format
test_stationarity(y,'raw data')

# Augmented Dickey-Fuller Test
from statsmodels.tsa.stattools import adfuller
def ADF_test(timeseries, dataDesc):
    print(' > Is the {} stationary ?'.format(dataDesc))
    dftest = adfuller(timeseries.dropna(), autolag='AIC')
    print('Test statistic = {:.3f}'.format(dftest[0]))
    print('P-value = {:.3f}'.format(dftest[1]))
    print('Critical values :')
    for k, v in dftest[4].items():
        print('\t{}: {} - The data is {} stationary with {}% confidence'.format(k, v, 'not' if v<dftest[0] else '', 100-int(k[:-1])))
        
ADF_test(y,'raw data')

# Detrending
y_detrend =  (y - y.rolling(window=12).mean())/y.rolling(window=12).std()

test_stationarity(y_detrend,'de-trended data')
ADF_test(y_detrend,'de-trended data')

# Differencing
y_12lag =  y - y.shift(12)

test_stationarity(y_12lag,'12 lag differenced data')
ADF_test(y_12lag,'12 lag differenced data')

# Detrending + Differencing

y_12lag_detrend =  y_detrend - y_detrend.shift(12)

test_stationarity(y_12lag_detrend,'12 lag differenced de-trended data')
ADF_test(y_12lag_detrend,'12 lag differenced de-trended data')

y_to_train = y[:'2019-12-01'] # dataset to train
y_to_val = y['2021-01-01':] # last X months for test  
predict_date = len(y) - len(y[:'2021-01-01']) # the number of data points for the test set

###########################################################################



from statsmodels.tsa.api import Holt

def holt(y,y_to_train,y_to_test,smoothing_level,smoothing_slope, predict_date):
    y.plot(marker='o', color='black', legend=True, figsize=(14, 7))
    
    fit1 = Holt(y_to_train).fit(smoothing_level, smoothing_slope, optimized=False)
    fcast1 = fit1.forecast(predict_date).rename("Holt's linear trend")
    mse1 = ((fcast1 - y_to_test) ** 2).mean()
    print('The Root Mean Squared Error of Holt''s Linear trend {}'.format(round(np.sqrt(mse1), 2)))

    fit2 = Holt(y_to_train, exponential=True).fit(smoothing_level, smoothing_slope, optimized=False)
    fcast2 = fit2.forecast(predict_date).rename("Exponential trend")
    mse2 = ((fcast2 - y_to_test) ** 2).mean()
    print('The Root Mean Squared Error of Holt''s Exponential trend {}'.format(round(np.sqrt(mse2), 2)))
    
    fit1.fittedvalues.plot(marker="o", color='blue')
    fcast1.plot(color='blue', marker="o", legend=True)
    fit2.fittedvalues.plot(marker="o", color='red')
    fcast2.plot(color='red', marker="o", legend=True)

    plt.show()
from statsmodels.tsa.api import Holt

def holt(y,y_to_train,y_to_test,smoothing_level,smoothing_slope, predict_date):
    y.plot(marker='o', color='black', legend=True, figsize=(14, 7))
    
    fit1 = Holt(y_to_train).fit(smoothing_level, smoothing_slope, optimized=False)
    fcast1 = fit1.forecast(predict_date).rename("Holt's linear trend")
    mse1 = ((fcast1 - y_to_test) ** 2).mean()
    print('The Root Mean Squared Error of Holt''s Linear trend {}'.format(round(np.sqrt(mse1), 2)))

    fit2 = Holt(y_to_train, exponential=True).fit(smoothing_level, smoothing_slope, optimized=False)
    fcast2 = fit2.forecast(predict_date).rename("Exponential trend")
    mse2 = ((fcast2 - y_to_test) ** 2).mean()
    print('The Root Mean Squared Error of Holt''s Exponential trend {}'.format(round(np.sqrt(mse2), 2)))
    
    fit1.fittedvalues.plot(marker="o", color='blue')
    fcast1.plot(color='blue', marker="o", legend=True)
    fit2.fittedvalues.plot(marker="o", color='red')
    fcast2.plot(color='red', marker="o", legend=True)

    plt.show()

holt(y, y_to_train,y_to_val,0.6,0.2,predict_date)

################

import itertools

def sarima_grid_search(y,seasonal_period):
    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2],seasonal_period) for x in list(itertools.product(p, d, q))]
    
    mini = float('+inf')
    
    
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(y,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)

                results = mod.fit()
                
                if results.aic < mini:
                    mini = results.aic
                    param_mini = param
                    param_seasonal_mini = param_seasonal

#                 print('SARIMA{}x{} - AIC:{}'.format(param, param_seasonal, results.aic))
            except:
                continue
    print('The set of parameters with the minimum AIC is: SARIMA{}x{} - AIC:{}'.format(param_mini, param_seasonal_mini, mini))
    

sarima_grid_search(y,52)
#sarima_grid_search(y,18)

# Call this function after pick the right(p,d,q) for SARIMA based on AIC               
def sarima_eva(y,order,seasonal_order,seasonal_period,pred_date,y_to_test):
    # fit the model 
    mod = sm.tsa.statespace.SARIMAX(y,
                                order=order,
                                seasonal_order=seasonal_order,
                                enforce_stationarity=False,
                                enforce_invertibility=False)

    results = mod.fit()
    print(results.summary().tables[1])
    
    #results.plot_diagnostics(figsize=(16, 8))
    #plt.show()
    
    # The dynamic=False argument ensures that we produce one-step ahead forecasts, 
    # meaning that forecasts at each point are generated using the full history up to that point.
    pred = results.get_prediction(start=pd.to_datetime(pred_date), dynamic=False)
    pred_ci = pred.conf_int()
    y_forecasted = pred.predicted_mean
    mse = ((y_forecasted - y_to_test) ** 2).mean()
    print('The Root Mean Squared Error of SARIMA with season_length={} and dynamic = False {}'.format(seasonal_period,round(np.sqrt(mse), 2)))

    ax = y.plot(label='observed')
    y_forecasted.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.2)

    ax.set_xlabel('Date')
    ax.set_ylabel('Sessions')
    plt.legend()
    plt.show()

    # A better representation of our true predictive power can be obtained using dynamic forecasts. 
    # In this case, we only use information from the time series up to a certain point, 
    # and after that, forecasts are generated using values from previous forecasted time points.
    pred_dynamic = results.get_prediction(start=pd.to_datetime(pred_date), dynamic=True, full_results=True)
    pred_dynamic_ci = pred_dynamic.conf_int()
    y_forecasted_dynamic = pred_dynamic.predicted_mean
    mse_dynamic = ((y_forecasted_dynamic - y_to_test) ** 2).mean()
    print('The Root Mean Squared Error of SARIMA with season_length={} and dynamic = True {}'.format(seasonal_period,round(np.sqrt(mse_dynamic), 2)))

    ax = y.plot(label='observed')
    y_forecasted_dynamic.plot(label='Dynamic Forecast', ax=ax,figsize=(14, 7))
    ax.fill_between(pred_dynamic_ci.index,
                    pred_dynamic_ci.iloc[:, 0],
                    pred_dynamic_ci.iloc[:, 1], color='k', alpha=.2)

    ax.set_xlabel('Date')
    ax.set_ylabel('Sessions')

    plt.legend()
    plt.show()
    
    return (results)

model = sarima_eva(y,(0, 0, 0),(0, 1, 1, 52),52,'2021-01-01',y_to_val)
#model = sarima_eva(y,(0, 0, 0),(1, 1, 1, 18),18,'2021-01-01',y_to_val)
##################################

def forecast(model,predict_steps,y):
    
    pred_uc = model.get_forecast(steps=predict_steps)

    #SARIMAXResults.conf_int, can change alpha,the default alpha = .05 returns a 95% confidence interval.
    pred_ci = pred_uc.conf_int()

    ax = y.plot(label='observed', figsize=(14, 7))
#     print(pred_uc.predicted_mean)
    pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.25)
    ax.set_xlabel('Date')
    ax.set_ylabel(y.name)

    plt.legend()
    plt.show()
    
    # Produce the forcasted tables 
    pm = pred_uc.predicted_mean.reset_index()
    pm.columns = ['Date','Predicted_Mean']
    pci = pred_ci.reset_index()
    pci.columns = ['Date','Lower Bound','Upper Bound']
    final_table = pm.join(pci.set_index('Date'), on='Date')
    
    return (final_table)

final_table = forecast(model,18,y)
final_table.head()
