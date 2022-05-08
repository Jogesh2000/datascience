##
## Dataset for Poster
##

library(sqldf)
library(plotly)

setwd("C:\\Drive D\\WD\\Poster\\")

homesales <- read.csv("RDC_Inventory_Core_Metrics_Zip.csv", stringsAsFactors = F, header = T)

stateregion <- read.csv("State with Region - Final.csv", stringsAsFactors = F, header = T)

homesales_joinregion <- sqldf("select a.*, b.Name, b.Region from homesales a
                              left join stateregion b on a.Abb=b.Abbreviation")

homesales<- homesales_joinregion

homesales_joinregion <- NULL

attach(homesales)

boxplot(active_listing_count, col = "orange", main= "Distribution of Active Listing Count across all Zip codes in US",
        ylab= "Active Listing Count")

hist(median_days_on_market, col = "red", main= "Distribution of Days on Market across all Zip codes in US",
        ylab= "Number of Houses", xlab = "Days in the Market")


hist(new_listing_count, col = "Green", main= "Distribution of New Listing Count across all Zip codes in US",
     ylab= "Index", xlab = "New Listings")

hist(median_square_feet, col = "Purple", main= "Distribution of New Listing Count across all Zip codes in US",
     ylab= "Index", xlab = "New Listings")

hist(median_square_feet, col = "Purple", main= "Distribution of Home Sq.ft across all Zip codes in US",
     ylab= "Index", xlab = "Suqare Feet")


price_byregion <- sqldf("select Region, avg(median_listing_price) As Avg_Listing_Price, max(median_listing_price)  as Max_Listing_Price,
       max(median_listing_price)  as Min_Listing_Price from homesales group by Region")

listing_byregion <- sqldf("select Region, round(avg(active_listing_count)) As average_listing_count, max(active_listing_count)  as Max_Listing_Count,
       max(active_listing_count)  as Min_Listing_Count from homesales group by Region")

##write.csv(homesales,"C:\\Drive D\\WD\\Poster\\homesales.csv", row.names = FALSE)

options(scipen=999)

lc<-tapply(active_listing_count,list(Region),mean)
md<-tapply(median_days_on_market,list(Region),mean)
nc<-tapply(new_listing_count,list(Region),mean)

lpc<-tapply(median_listing_price,list(Name),mean)


barplot(lpc)

x<-barplot(lpc, beside=T, main="Avg Price by State",col = brewer.pal(11,"Set3"), xaxt="n",xlab="Region", ylab="Price in")
labs <- paste(names(table(homesales$Name)))
text(cex=1, x=x-.25, y=-25, labs, xpd=TRUE, srt=90)


##par(mfrow = c(2,2))

library(RColorBrewer)

x<-barplot(lc, beside=T, main="Active Listing Count",col = brewer.pal(11,"Set3"), xaxt="n",xlab="Region", ylab="Count of Homes")
labs <- paste(names(table(homesales$Region)))
text(cex=1, x=x-.25, y=-1.25, labs, xpd=TRUE, srt=45)

x<-barplot(md, beside=T, main="Median Days on the Market",col = brewer.pal(11,"Set3"), xaxt="n",xlab="Region", ylab="Count of Homes")
labs <- paste(names(table(homesales$Region)))
text(cex=1, x=x-.25, y=-1.25, labs, xpd=TRUE, srt=45)

x<-barplot(nc, beside=T, main="New Listing Count",col = brewer.pal(11,"Set3"), xaxt="n",xlab="Region", ylab="Count of Homes")
labs <- paste(names(table(homesales$Region)))
text(cex=1, x=x-.25, y=-1.25, labs, xpd=TRUE, srt=45)



library(plotly)

sqldf("select distinct Region from homesales")


ne_mediansqft <- sqldf("select Name as State,avg(median_square_feet) as avg_sq_ft from homesales
                       where Region='Northeast'
                       group by Name
                       ")

south_mediansqft <- sqldf("select Name as State,avg(median_square_feet) as avg_sq_ft from homesales
                       where Region='South'
                       group by Name
                       ")

mw_mediansqft <- sqldf("select Name as State,avg(median_square_feet) as avg_sq_ft from homesales
                       where Region='Midwest'
                       group by Name
                       ")

west_mediansqft <- sqldf("select Name as State,avg(median_square_feet) as avg_sq_ft from homesales
                       where Region='West'
                       group by Name
                       ")

avg_sq_ft <- paste(round(ne_mediansqft$avg_sq_ft), sep = "")

fig1 <- plot_ly(ne_mediansqft, labels = ~State, values = ~avg_sq_ft, type = 'pie',textinfo= "text", text=avg_sq_ft)
fig1 %>% layout(title = 'North East States home Listings - Median Sq Ft',
                      xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
                      yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))


avg_sq_ft <- paste(round(south_mediansqft$avg_sq_ft), sep = "")

fig1 <- plot_ly(south_mediansqft, labels = ~State, values = ~avg_sq_ft, type = 'pie',textinfo= "text", text=avg_sq_ft)
fig1 %>% layout(title = 'South States home Listings - Median Sq Ft',
                xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
                yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))

avg_sq_ft <- paste(round(mw_mediansqft$avg_sq_ft), sep = "")

fig1 <- plot_ly(mw_mediansqft, labels = ~State, values = ~avg_sq_ft, type = 'pie',textinfo= "text", text=avg_sq_ft)
fig1 %>% layout(title = 'Mid west home Listings - Median Sq Ft',
                xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
                yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))

avg_sq_ft <- paste(round(west_mediansqft$avg_sq_ft), sep = "")

fig1 <- plot_ly(west_mediansqft, labels = ~State, values = ~avg_sq_ft, type = 'pie',textinfo= "text", text=avg_sq_ft)
fig1 %>% layout(title = 'Mid west home Listings - Median Sq Ft',
                xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
                yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))



ne_medianprice <- sqldf("select Name as State,round(avg(average_listing_price)) as avg_price from homesales
                       where Region='Northeast'
                       group by Name
                       ")

south_medianprice <- sqldf("select Name as State,round(avg(average_listing_price)) as avg_price from homesales
                       where Region='South'
                       group by Name
                       ")

mw_medianprice <- sqldf("select Name as State,round(avg(average_listing_price)) as avg_price from homesales
                       where Region='Midwest'
                       group by Name
                       ")

west_medianprice <- sqldf("select Name as State,round(avg(average_listing_price)) as avg_price from homesales
                       where Region='West'
                       group by Name
                       ")


avg_price <- paste(round(ne_medianprice$avg_price/1000),"K", sep = "")

fig2 <- plot_ly(ne_medianprice, labels = ~State, values = ~avg_price, 
                type = 'pie',textinfo= "text", text=avg_price)

fig2 %>% layout(title = 'North East States home Listings - Average  Listing Price',
                xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
                yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))
                

fig1

colors <- c('rgb(211,94,96)', 'rgb(128,133,133)', 'rgb(144,103,167)', 'rgb(171,104,87)', 'rgb(114,147,203)')

fig <- plot_ly(ne_medianprice,labels = ~State, values = ~avg_price,
                                  marker = list(colors = colors,
                                  line = list(color = '#FFFFFF', width = 1)),
                                  showlegend = TRUE)
fig <- fig %>% add_pie(hole = 0.6)
fig2_donut <- fig %>% layout(title = "Donut charts using Plotly",  showlegend = T,
                      xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
                      yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))

fig2_donut


orca(fig2_donut, "fig2_donut.pdf")

library(RColorBrewer)
myPalette <- brewer.pal(5, "Set2") 

# You can change the border of each area with the classical parameters:
ggplot(ne_medianprice, aes(x="", y=avg_price, fill=State)) +
        geom_bar(stat="identity", width=1, color="white") +
        coord_polar("y", start=0) +
        theme(legend.position="none") +
        geom_text(aes(y = avg_price, label = State), color = "white", size=6) +
        scale_fill_brewer(palette="RdGy")


avg_price <- paste(round(south_medianprice$avg_price/1000),"K", sep = "")

fig2 <- plot_ly(south_medianprice, labels = ~State, values = ~avg_price, type = 'pie',textinfo= "text", text=avg_price)
fig2 %>% layout(title = 'South States home Listings - Average  Listing Price',
                xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
                yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))

orca(fig2, "fig2.pdf")

colors <- c('rgb(211,94,96)', 'rgb(128,133,133)', 'rgb(144,103,167)', 'rgb(171,104,87)', 'rgb(114,147,203)')

fig <- plot_ly(south_medianprice,labels = ~State, values = ~avg_price,
               marker = list(colors = colors,
                             line = list(color = '#FFFFFF', width = 1)),
               showlegend = TRUE)
fig <- fig %>% add_pie(hole = 0.6)
fig2_donut <- fig %>% layout(title = "Donut charts using Plotly",  showlegend = T,
                             xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
                             yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))

fig2_donut

orca(fig2_donut, "fig2_donut.pdf")

avg_price <- paste(round(mw_medianprice$avg_price/1000),"K", sep = "")

fig3 <- plot_ly(mw_medianprice, labels = ~State, values = ~avg_price, type = 'pie',textinfo= "text", text=avg_price)
fig3 %>% layout(title = 'Mid West States home Listings - Average  Listing Price',
                xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
                yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))


orca(fig3, "fig3.pdf")

colors <- c('rgb(211,94,96)', 'rgb(128,133,133)', 'rgb(144,103,167)', 'rgb(171,104,87)', 'rgb(114,147,203)')

fig <- plot_ly(mw_medianprice,labels = ~State, values = ~avg_price,
               marker = list(colors = colors,
                             line = list(color = '#FFFFFF', width = 1)),
               showlegend = TRUE)
fig <- fig %>% add_pie(hole = 0.6)
fig3_donut <- fig %>% layout(title = "Donut charts using Plotly",  showlegend = T,
                             xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
                             yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))

fig3_donut

orca(fig3_donut, "fig3_donut.pdf")

avg_price <- paste(round(west_medianprice$avg_price/1000),"K", sep = "")

fig4 <- plot_ly(west_medianprice, labels = ~State, values = ~avg_price, type = 'pie',textinfo= "text", text=avg_price)
fig4 %>% layout(title = 'Mid West States home Listings - Average  Listing Price',
                xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
                yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))

orca(fig4, "fig4.pdf")

colors <- c('rgb(211,94,96)', 'rgb(128,133,133)', 'rgb(144,103,167)', 'rgb(171,104,87)', 'rgb(114,147,203)')

fig <- plot_ly(west_medianprice,labels = ~State, values = ~avg_price,
               marker = list(colors = colors,
                             line = list(color = '#FFFFFF', width = 1)),
               showlegend = TRUE)
fig <- fig %>% add_pie(hole = 0.6)
fig4_donut <- fig %>% layout(title = "Donut charts using Plotly",  showlegend = T,
                             xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
                             yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))

fig4_donut

orca(fig4_donut, "fig4_donut.pdf")

#######################

############# Bar charts  - Top 10 ################

listing_yy_desc <- sqldf("select zip_name, active_listing_count_yy from homesales order by active_listing_count_yy desc")


listing_yy_top10 <- sqldf("select zip_name, active_listing_count_yy from homesales where active_listing_count_yy >0 order by active_listing_count_yy desc LIMIT 10")

listing_yy_top10$zip_name <- factor(listing_yy_top10$zip_name, levels = unique(listing_yy_top10$zip_name)[order(listing_yy_top10$active_listing_count_yy, decreasing = TRUE)])

top10cities <- 
        
plot_ly(listing_yy_top10, x = ~zip_name, y = ~active_listing_count_yy, type = 'bar', text = text,
        width = 20,
        marker = list(color = 'rgb(245,137,103)',
                      line = list(color = 'rgb(255,255,255)',
                                  width = 1.5)))

orca(top10cities, "top10citis.pdf")

listing_yy_bottom10 <- sqldf("select zip_name, active_listing_count_yy from homesales where active_listing_count_yy >0 order by active_listing_count_yy asc LIMIT 10")

listing_yy_bottom10$zip_name <- factor(listing_yy_bottom10$zip_name, levels = unique(listing_yy_bottom10$zip_name)[order(listing_yy_bottom10$active_listing_count_yy, decreasing = FALSE)])

bottom10cities <- plot_ly(listing_yy_bottom10, x = ~zip_name, y = ~active_listing_count_yy, type = 'bar', text = text,
                marker = list(color = 'rgb(144,31,91)',
                              line = list(color = 'rgb(255,255,255)',
                                          width = 1.5)))

orca(bottom10cities, "bottom10citis.pdf")

########### map

library(usmap)
library(ggplot2)

sales <-  homesales

sales$state <- sales$Abb

sales_by_state <- sqldf("select state,avg(median_listing_price_yy) as listing_price_yy from sales
                          group by state
                        order by 2 desc")

str(sales_by_state)

plot_usmap(data = sales_by_state, values = "listing_price_yy", color = "purple") + 
        scale_fill_continuous(
                low = "white", high = "red", name = "Listing Price 2020 vs 2019", label = scales::comma
        ) + theme(legend.position = "right") +
        geom_text(data=sales_by_state, aes(long, lat, label = state),
                  color = "blue", size=3) + scale_fill_brewer(palette = "Greens")

library(ggplot2)
library(maps)
library(usmap)
library(data.table)
library(ggsn) # for scale bar `scalebar`


library(ggrepel)

us_map <- usmap::us_map() # used to add map scale

usmap::plot_usmap(data = sales_by_state, values = "listing_price_yy", labels = T)+
        labs(fill = 'Listing Price') + 
        scale_fill_gradientn(colours=c("#901F5B","#F58967","#58516C","#944F3C"),na.value="grey90",
                             guide = guide_colourbar(barwidth = 25, barheight = 0.4,
                                                     #put legend title on top of legend
                                                     title.position = "top")) +
        # map scale
        ggsn::scalebar(data = sales_by_state, dist = 500, dist_unit = "km",
                       border.size = 0.4, st.size = 4,
                       box.fill = c('black','white'),
                       transform = FALSE, model = "WGS84") + 
        # put legend at the bottom, adjust legend title and text font sizes
        theme(legend.position = "bottom",
              legend.title=element_text(size=12), 
              legend.text=element_text(size=10))

summary(homesales$price_increased_count)

mean(homesales$median_square_feet_yy)

sqldf("select avg(median_square_feet_yy) from homesales where median_square_feet_yy>0 or median_square_feet_yy <0")
sqldf("select avg(median_days_on_market_yy) from homesales where median_days_on_market_yy>0 or median_days_on_market_yy <0")
sqldf("select avg(new_listing_count_yy) from homesales where median_square_feet_yy>0 or median_square_feet_yy <0")

mean(homesales$new_listing_count_yy)

##write.csv(homesales,"C:\\Drive D\\homesales.csv", row.names = FALSE)

top10 <- read.csv("Top10.csv", stringsAsFactors = F, header = T)

top10_region <- sqldf("select * from top10 a left join (select distinct Name as source_name, Region from homesales) b on a.Name=b.source_name ") 
top10_south <- sqldf("select * from top10_region where Region = 'South' and [Median.Square.Feet]<>0 and [Median.Listing.Price] <2000000 ")

top10_northeast <- sqldf("select * from top10_region where Region = 'Northeast' and [Median.Square.Feet]<>0")
top10_midwest <- sqldf("select * from top10_region where Region = 'Midwest' and [Median.Square.Feet]<>0 and  [Median.Listing.Price] <2000000 ")
top10_west <- sqldf("select * from top10_region where Region = 'West' and [Median.Square.Feet]<>0 ")


library(RColorBrewer)
n <- 20
qual_col_pals <- brewer.pal.info[brewer.pal.info$category == 'qual',]
colors <- unlist(mapply(brewer.pal, qual_col_pals$maxcolors, rownames(qual_col_pals)))

colors <- c('#4AC6B7', '#1972A4', '#965F8A', '#FF7070', '#C61951')

bubble_south <-  plot_ly(top10_south, x = ~Median.Listing.Price, y = ~Median.Square.Feet, color = ~Name, size =~Active.Listing.Count,colors = colors,
        type = 'scatter', mode = 'markers', 
        marker = list(symbol = 'circle', sizemode = 'diameter',
                      line = list(width = 2, color = '#FFFFFF')),
        text = ~paste('Region:', Name, '<br>City:', zip_name)
)

orca(bubble_south, "bubble_south.pdf")

n <- 20
qual_col_pals = brewer.pal.info[brewer.pal.info$category == 'Dark2',]
colors <- unlist(mapply(brewer.pal, qual_col_pals$maxcolors, rownames(qual_col_pals)))

bubble_northeast <-  plot_ly(top10_northeast, x = ~Median.Listing.Price, y = ~Median.Square.Feet, color = ~Name, size =~Active.Listing.Count,colors = colors,
                         type = 'scatter', mode = 'markers', 
                         marker = list(symbol = 'circle', sizemode = 'diameter',
                                       line = list(width = 2, color = '#FFFFFF')),
                         text = ~paste('Region:', Name, '<br>City:', zip_name)
)

bubble_northeast<- add_trace(bubble_northeast, y = list(7000), name = " ", showlegend = F)

orca(bubble_northeast, "bubble_northeast.pdf")

n <- 20
qual_col_pals = brewer.pal.info[brewer.pal.info$category == 'Spectral',]
colors <- unlist(mapply(brewer.pal, qual_col_pals$maxcolors, rownames(qual_col_pals)))

bubble_midwest <-  plot_ly(top10_midwest, x = ~Median.Listing.Price, y = ~Median.Square.Feet, color = ~Name, size =~Active.Listing.Count,colors = colors,
                             type = 'scatter', mode = 'markers', 
                             marker = list(symbol = 'circle', sizemode = 'diameter',
                                           line = list(width = 2, color = '#FFFFFF')),
                             text = ~paste('Region:', Name, '<br>City:', zip_name)
)

bubble_midwest<- add_trace(bubble_midwest, y = list(7000), name = " ", showlegend = F)

orca(bubble_midwest, "bubble_midwest.pdf")

n <- 20
qual_col_pals = brewer.pal.info[brewer.pal.info$category == 'Set1',]
colors <- unlist(mapply(brewer.pal, qual_col_pals$maxcolors, rownames(qual_col_pals)))

bubble_west <-  plot_ly(top10_west, x = ~Median.Listing.Price, y = ~Median.Square.Feet, color = ~Name, size =~Active.Listing.Count,colors = colors,
                           type = 'scatter', mode = 'markers', 
                           marker = list(symbol = 'circle', sizemode = 'diameter',
                                         line = list(width = 2, color = '#FFFFFF')),
                           text = ~paste('Region:', Name, '<br>City:', zip_name)
)
bubble_west<- add_trace(bubble_west, y = list(7000), name = " ", showlegend = F)

orca(bubble_west, "bubble_midwest.pdf")


top10_south_midwest <- sqldf("select * from top10_region where (Region = 'South' or Region = 'Midwest') and [Median.Square.Feet]<>0")
top10_northeast_west <- sqldf("select * from top10_region where (Region = 'Northeast' or Region='West') and [Median.Square.Feet]<>0")


n <- 20
qual_col_pals <- brewer.pal.info[brewer.pal.info$category == 'qual',]
colors <- unlist(mapply(brewer.pal, qual_col_pals$maxcolors, rownames(qual_col_pals)))

bubble_south_midwest <-  plot_ly(top10_south_midwest, x = ~Median.Listing.Price, y = ~Median.Square.Feet, color = ~Name, size =~Active.Listing.Count,colors = colors,
                        type = 'scatter', mode = 'markers', 
                        marker = list(symbol = 'circle', sizemode = 'diameter',
                                      line = list(width = 2, color = '#FFFFFF')),
                        text = ~paste('Region:', Name, '<br>City:', zip_name)
)


orca(bubble_south_midwest, width = 11 * 96, height = 8 * 96,"bubble_south_midwest_new.pdf")

n <- 40
qual_col_pals <- brewer.pal.info[brewer.pal.info$category == 'qual',]
colors <- unlist(mapply(brewer.pal, qual_col_pals$maxcolors, rownames(qual_col_pals)))

bubble_northeast_west <-  plot_ly(top10_northeast_west, x = ~Median.Listing.Price, y = ~Median.Square.Feet, color = ~Name, size =~Active.Listing.Count,colors = colors,
                                 type = 'scatter', mode = 'markers', 
                                 marker = list(symbol = 'circle', sizemode = 'diameter',
                                               line = list(width = 2, color = '#FFFFFF')),
                                 text = ~paste('Region:', Name, '<br>City:', zip_name)
)



bubble_northeast_west %>% layout(xaxis = list(range = c(1000000,9000000))) %>% orca(file = "plot.pdf")

orca(bubble_northeast_west, width = 11, height = 8,"bubble_northeast_west.pdf")

orca(bubble_northeast_west,width = 11 * 96, height = 8 * 96,"plot1.pdf")


