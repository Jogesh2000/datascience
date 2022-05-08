# -*- coding: utf-8 -*-
"""
Spyder Editor

Homework 1 - Jogesh Pugazhendhi
"""
### Importing Pandas and other function
import pandas as pd
import os
import pandasql
from pandasql import sqldf
### Changing default location of files
os.chdir('C:\\py\\Homework1')
os.getcwd()

### Reading Homesales data 
df= pd.read_csv("homesaleshistory2020.csv",low_memory=False)
df_history=pd.DataFrame(df)
df_history['Abb']= df_history['zip_name'].str[-2:]
df_history['Abb'] =df_history['Abb'].str.upper()
last_row_history = len(df_history)-1
df_history = df_history.drop(df_history.index[last_row_history])

### converting df to dataframe
df = pd.DataFrame(df)
df = sqldf("select * from df where month_date_yyyymm=202008")

### Testing the datframe
df.head(10)

### Extracting state abbreviation from Zip name column and changing it to upper case
df['Abb']= df['zip_name'].str[-2:]
df['Abb'] =df['Abb'].str.upper()

#### Delete Last row which does not have any proper records

last_row = len(df)-1
df = df.drop(df.index[last_row])

#### Reading another file to add States and Region based on state abbreviation
state_region = pd.read_csv("state_region.csv")
state_region = pd.DataFrame(state_region)
state_region

#### Merging 2 dataframes to get the state and region to the homesales dataframe
df = df.merge(state_region, on='Abb', how='left')
df

### Merging history dataframe with state and region
df_history = df_history.merge(state_region, on='Abb', how='left')

state_stats_history=sqldf("select month_date_yyyymm as MonthYear, Name as State,Region,avg(median_listing_price_yy) as median_listing_price_yy, avg(median_listing_price) as median_listing_price, sum(active_listing_count) as active_listing_count, sum(price_reduced_count) as price_reduced_count,avg(median_days_on_market) as median_days_on_market from df_history where month_date_yyyymm like '20200%' group by month_date_yyyymm, Name, Region   ")

#### Creating Tables with aggregated reports
region_stats=sqldf("select Region,avg(median_listing_price) as [Median Listing Price], sum(active_listing_count) as [Active Listing Count], avg(median_days_on_market) as [Days in the market] from df group by Region")
region_stats.to_csv("C:\\py\\Homework1\\region_stats.csv")

"""
region_stats.plot(
    x='Region', 
    y='median_listing_price',
    kind='barh',
    figsize=(10, 7),
    title='Median Listing Price by Region')
"""
### using Plotly packages to create Graphs
import plotly
import plotly.graph_objects as go
import plotly.express as px

### Plot for Median Listing price by State with Active Listing Count 
fig = px.bar(region_stats, x="Region", y="Median Listing Price",text = "Active Listing Count", color="Region",title="Median Listing price by Region - June 2020 (Active Listing Count on top of each bar)")
fig.update_traces(texttemplate='Listing Count,%{text:.2s}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
fig.show()

########## Creating Dataset with State Metrics

state_stats=sqldf("select Abb,Name as State,round(avg(median_listing_price),0) as [Median Listing Price], sum(active_listing_count) as active_listing_count, round(avg(median_days_on_market),0) as [Days in the market] from df group by Abb,Name")
state_stats.to_csv("C:\\py\\Homework1\\state_stats.csv")

fig_map = go.Figure(data=go.Choropleth(
    locations=state_stats['Abb'], # Spatial coordinates
    z = state_stats['Median Listing Price'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    text=state_stats['active_listing_count'], # hover text
    marker_line_color='white', # line markers between states
    colorbar_title = "Millions USD",
))

fig_map.update_layout(
    title_text = 'Median Listing Price by State',
    geo_scope='usa', # limite map scope to USA
)

fig_map.show()

########################################################################
####### get the top 10 and bottom 10 states based on listing count as of Aug 2020###

top10=sqldf("select distinct State from state_stats where active_listing_count>20000")
bottom10=sqldf("select distinct State from state_stats where active_listing_count<3500")

############ Pull data from History df only for top and bottom 10 #####

top10_history = sqldf("select *,cast(MonthYear as int) as Month from state_stats_history where State in (select State from top10)" )
top10_history['MonthYear']=pd.to_datetime(top10_history['MonthYear'], format='%Y%m').dt.strftime('%m/%Y')
top10_2020 = sqldf("select State,avg(median_listing_price) as median_listing_price,avg(median_days_on_market) as median_days_on_market,sum(active_listing_count) as active_listing_count, sum(price_reduced_count) as price_reduced_count from top10_history group by State")
bottom10_history = sqldf("select * from state_stats_history where State in (select State from bottom10)")
bottom10_history['MonthYear']=pd.to_datetime(bottom10_history['MonthYear'], format='%Y%m').dt.strftime('%m/%Y')
bottom10_2020 = sqldf("select State,avg(median_listing_price) as median_listing_price,avg(median_days_on_market) as median_days_on_market,sum(active_listing_count) as active_listing_count, sum(price_reduced_count) as price_reduced_count from bottom10_history group by State")

########### Create final month level data ################

history2020 = sqldf("select MonthYear as MonthYear_hs,sum(active_listing_count) as active_listing_count,avg(median_listing_price) as median_listing_price  from state_stats_history group by MonthYear")
history2020['link'] = ['Month1','Month2','Month3','Month4','Month5','Month6','Month7','Month8']

### Top 10 States
import plotly.express as px
fig3 = px.line(top10_history, x="MonthYear", y="median_listing_price", color='State', hover_name="State")
fig3.show()

fig4 = px.line(top10_history, x="MonthYear", y="price_reduced_count", color='State', hover_name="State")
fig4.show()

fig5 = px.line(bottom10_history, x="MonthYear", y="median_listing_price", color='State', hover_name="State")
fig5.show()

fig6 = px.line(bottom10_history, x="MonthYear", y="price_reduced_count", color='State', hover_name="State")
fig6.show()

### top 10 analysis
fig5 = px.scatter(top10_2020, x="median_listing_price", y="median_days_on_market", color="State",
                 size='active_listing_count', hover_data=['median_days_on_market'])
fig5.show()

## bottom 10 analysis
fig6 = px.scatter(bottom10_2020, x="median_listing_price", y="median_days_on_market", color="State",
                 size='active_listing_count', hover_data=['median_days_on_market'])
fig6.show()

################################ End of Listings Analysis #################

### Importing Pandas and other function
import pandas as pd
import os
import pandasql
from pandasql import sqldf
### Changing default location of files
os.chdir('C:\\py\\Homework2')
os.getcwd()

### Loading Covid Data loaded in my PC
covid= pd.read_csv("covid_confirmed_usafacts.csv")
covid.columns=['CountyFIPS','County Name','State','StateFIPS','Jan2020','Feb2020','Mar2020','Apr2020','May2020','Jun2020','Jul2020','Aug2020']
covid_final = sqldf("select 'Jan2020' as MonthYear,sum(Jan2020) as covid_cases from covid union all select 'Feb2020' as MonthYear,sum(Feb2020) as covid_cases from covid union all select 'Mar2020' as MonthYear,sum(Mar2020) as covid_cases from covid union all select 'Apr2020' as MonthYear,sum(Apr2020) as covid_cases from covid  union all select 'May2020' as MonthYear,sum(May2020) as covid_cases from covid union all select 'Jun2020' as MonthYear,sum(Jun2020) as covid_cases from covid union all select 'Jul2020' as MonthYear,sum(Jul2020) as covid_cases from covid union all select 'Aug2020' as MonthYear,sum(Aug2020) as covid_cases from covid")

############## Scraping mortgage data from the below website
table1 = pd.read_html("https://ycharts.com/indicators/30_year_mortgage_rate")

### assiging each column to a variable 
df1 = table1[0]
df2 = table1[1]

df1.columns = ['date', 'percentage']
df1

df2.columns = ['date', 'percentage']
df2

## concatenating 2 columns to create the final dataset for Mortgage Rate
concat_two_columns = [df1, df2]
result = pd.concat(concat_two_columns)
result

### removing extra spaces from the columns and created final dataset with aggregation on MonthYear
mortgage_rates = sqldf("select replace(substr(date,1,3),' ','')||replace(substr(date,length(date)-4),' ','') as MonthYear,replace(percentage,'%','') as percent from result")
mortgage_rates_final = sqldf("select MonthYear, avg(percent) as rate_percent from mortgage_rates group by MonthYear")

###################### Reading Sale of cars for the year 2020 from the below website

from requests import get
url = 'https://www.goodcarbadcar.net/2020-us-vehicle-sales-figures-by-brand/'
response = get(url)

from bs4 import BeautifulSoup
import pandas as pd
#lxml_soup = BeautifulSoup(response.text, 'lxml')
html_soup = BeautifulSoup(response.content, 'html.parser')

tables = html_soup.find_all("table")

# Table 3 : US Automotive Brand Sales by Month
tables = html_soup.find_all("table")
table = tables[2]
tab_data = [[cell.text for cell in row.find_all(["th","td"])] for row in table.find_all("tr")]
df = pd.DataFrame(tab_data)
df

# Result
# Remove last two unwanted rows
df = df.iloc[:-2]
df
## assigning df to carsales df
carsales = df

## assigning columns to carsales data frame
carsales.columns=['Brand','Jan2020','Feb2020','Mar2020','Apr2020','May2020','Jun2020','Jul2020','Aug2020','Sep2020','Oct2020','Nov2020','Dec2020']

## Removing commas in the numbers as scraped from the website
carsales = sqldf("select Brand,replace(Jan2020,',','') as Jan2020, replace(Feb2020,',','') as Feb2020 , replace(Mar2020,',','') as Mar2020, replace(Apr2020,',','') as Apr2020, replace(May2020,',','') as May2020, replace(Jun2020,',','') as Jun2020,replace(Jul2020,',','') as Jul2020, replace(Aug2020,',','') as Aug2020  from carsales where Brand<>'Brand'")
carsales_final=sqldf("select Brand,'Jan2020' as MonthYear, Jan2020 as sales from carsales union all select Brand,'Feb2020' as MonthYear, Feb2020 as sales from carsales union all select Brand,'Mar2020' as MonthYear, Mar2020 as sales from carsales union all select Brand,'Apr2020' as MonthYear, Apr2020 as sales from carsales  union all select Brand,'May2020' as MonthYear, May2020 as sales from carsales union all select Brand,'Jun2020' as MonthYear, Jun2020 as sales from carsales union all select Brand,'Jul2020' as MonthYear, Jul2020 as sales from carsales ")
### created aggregated dataset on Monthyear level with overall car sales
carsales_agg=sqldf("select MonthYear,round(sum(sales),0) as car_sales from carsales_final group by MonthYear ")
carsales_final.to_csv("C:\\py\\Homework2\\carsales_brand.csv")
################# Combine all datasets - covid, mortgage rates and car sales into 1 dataset for final analysis
df_tmp1 = covid_final.merge(mortgage_rates_final, on='MonthYear', how='left')
df2_tmp2 = df_tmp1.merge(carsales_agg,on='MonthYear', how='left')

final_dataset = df2_tmp2
final_dataset['link'] = ['Month1','Month2','Month3','Month4','Month5','Month6','Month7','Month8']

final_dataset=final_dataset.merge(history2020,on='link', how='left')
### writing the final dataframe report to csv
final_dataset.to_csv("C:\\py\\Homework2\\final_covid_Home_mortgage_carsales.csv")

### Importing plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#### Plot 1 - Covid Cases Vs Mortgage Rate
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(x=final_dataset.MonthYear, y=final_dataset.covid_cases, name="Covid Cases"), row=1, col=1, secondary_y=False)
fig.add_trace(go.Scatter(x=final_dataset.MonthYear, y=final_dataset.rate_percent, name="Mortgage Rate"),row=1, col=1, secondary_y=True, )
fig.update_layout(height=800,title_text='USA Covid Cases vs Mortgage Rate(%) in 2020')

### Plot 2 - Covid Cases Vs Car Sales
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Scatter(x=final_dataset.MonthYear, y=final_dataset.covid_cases, name="Covid Cases"), row=1, col=1, secondary_y=False)
fig2.add_trace(go.Scatter(x=final_dataset.MonthYear, y=final_dataset.car_sales, name="Number of Cars Sold"),row=1, col=1, secondary_y=True, )
fig2.update_layout(height=800,title_text='USA Covid Cases vs Car Sales in 2020')

### Plot 3: Car sales trend by Brand in 2020
import plotly.express as px
fig3 = px.line(carsales_final, x="MonthYear", y="sales", color='Brand', hover_name="Brand")
fig3.show()

####

fig4 = make_subplots(specs=[[{"secondary_y": True}]])
fig4.add_trace(go.Scatter(x=final_dataset.MonthYear, y=final_dataset.covid_cases, name="Covid Cases"), row=1, col=1, secondary_y=False)
fig4.add_trace(go.Scatter(x=final_dataset.MonthYear, y=final_dataset.median_listing_price, name="Median Listing prices of houses listed"),row=1, col=1, secondary_y=True, )
fig4.update_layout(height=800,title_text='USA Covid Cases vs Home sale listings 2020')

