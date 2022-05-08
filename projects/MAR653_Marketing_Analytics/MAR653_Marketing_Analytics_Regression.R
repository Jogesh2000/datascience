setwd("C:\\Drive D\\WD\\nba")

nba <- read.csv("playerstats.csv", stringsAsFactors = F)

str(nba)
dim(nba)
colnames(nba)

mtcars<- mtcars

d <- density(mtcars$mpg)
plot(d)

polygon(d, col="orange", border="blue")

d <- density(mtcars$mpg)
polygon(d, border="blue")
hist(d)


boxplot( df[ ,2] )

mylogit <- glm(PerAbove20 ~ Pointsper36 + BlocksPer36 + StealsPer36 + AssistsPer36 + Reboundsper36
               + FT + FG3 + FG, data = nba, family = "binomial")

summary(mylogit)

my.letters <- sample(letters[7:9], size = 50, replace =T)
barplot(table(my.letters))

df<- c(1,2,3)
df[2]<- "2"
df

norm(1.96)
dnorm(1.96)
pnorm(1.96)
rnorm(1.96)
pnorm


mtrx <- matrix(c(1,2,3,4,5), )
              
               y<-1:4
               attr(y,"new") <
               