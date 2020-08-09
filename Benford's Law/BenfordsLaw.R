---
title: "DSC680"
author: "Nick Miller"
program: "Benford's Law"
---
  
library(ggplot2)


#Create Benford's Law function using log base 10 and plot
benlaw <- function(d) log10(1 + 1 / d)
digits <- 1:9
baseBarplot <- barplot(benlaw(digits), names.arg = digits, xlab = "First Digit", ylim = c(0, .35))


#Explore random integers
# Select first digit of a number
firstDigit <- function(x) substr(gsub('[0.]', '', x), 1, 1)

# Count absolute frequencies of each first digit and calculate relative frequencies
pctFirstDigit <- function(x)
  data.frame(table(firstDigit(x)) / length(x))

# Generate 10000 random integers between 0 and 100 and analyze
N <- 10000
set.seed(1023)
x1 <- runif(N, 0, 100)
df1 <- pctFirstDigit(x1)
head(df1)

# plot observations relative to Benford's Law
lines(x = baseBarplot[,1], y = df1$Freq, col = "red", lwd = 4, type = "b", pch = 23, cex = 1.5, bg = "red")

# Generate 10000 random integers between 0 and 1000 and analyze
x2 <- runif(N, 0, 1000)
df2 <- pctFirstDigit(x2)
lines(x = baseBarplot[,1], y = df2$Freq, col = "violet", lwd = 4, type = "b", pch = 23, cex = 1.5, bg = "violet")

# Generate 10000 random integers between 0 and 10000 and analyze
x3 <- runif(N, 0, 10000)
df3 <- pctFirstDigit(x3)
lines(x = baseBarplot[,1], y = df3$Freq, col = "blue", lwd = 4, type = "b", pch = 23, cex = 1.5, bg = "blue")


#YouTube Video Analysis
# Import data and remove unnecessary columns
youtube <- read.csv("USvideos.csv", header = TRUE)
youtube[c(1, 2, 4, 5, 6, 7, 12, 13, 14, 15, 16)] <- list(NULL)

# Analyze features using built-in Benford functions
bfdViews <- benford(youtube$views, number.of.digits = 1)
bfdLikes <- benford(youtube$likes, number.of.digits = 1)
bfdDislikes <- benford(youtube$dislikes, number.of.digits = 1)
bfdComments <- benford(youtube$comment_count, number.of.digits = 1)

# Using ggplot, plot Benford's predictions
df <- data.frame(x = digits, y = benlaw(digits))
ggBarplot <- ggplot(df, aes(x = factor(x), y = y)) + geom_bar(stat = "identity") + xlab("First Digit") + ylab(NULL)
print(ggBarplot)

# Remove 0s from columns
goodviews <- fun.zero.omit(youtube$views)
goodlikes <- fun.zero.omit(youtube$likes)
gooddislikes <- fun.zero.omit(youtube$dislikes)
goodcomments <- fun.zero.omit(youtube$comment_count)

# create dataframes to use with ggplot
dfviews <- pctFirstDigit(goodviews)
dflikes <- pctFirstDigit(goodlikes)
dfdislikes <- pctFirstDigit(gooddislikes)
dfcomments <- pctFirstDigit(goodcomments)

# Plot views, likes, dislikes, and comments in ggplot
p1 <- ggBarplot + 
  geom_line(data = dfviews, 
            aes(x = Var1, y = Freq, group = 1), 
            colour = "red", 
            size = 2) +
  geom_point(data = dfviews, 
             aes(x = Var1, y = Freq, group = 1), 
             colour = "red", 
             size = 4, pch = 23, bg = "red")
p2 <- p1 +
  geom_line(data = dflikes, 
            aes(x = Var1, y = Freq, group = 1), 
            colour = "violet", 
            size = 2) +
  geom_point(data = dflikes, 
             aes(x = Var1, y = Freq, group = 1), 
             colour = "violet", 
             size = 4, pch = 23, bg = "violet")
p3 <- p2 +
  geom_line(data = dfdislikes, 
            aes(x = Var1, y = Freq, group = 1), 
            colour = "blue", 
            size = 2) +
  geom_point(data = dfdislikes, 
             aes(x = Var1, y = Freq, group = 1), 
             colour = "blue", 
             size = 4, pch = 23, bg = "blue")
p4 <- p3 +
  geom_line(data = dfcomments, 
            aes(x = Var1, y = Freq, group = 1), 
            colour = "green", 
            size = 2) +
  geom_point(data = dfcomments, 
             aes(x = Var1, y = Freq, group = 1), 
             colour = "green", 
             size = 4, pch = 23, bg = "green") + 
  scale_colour_manual(name="Line Color",
                      values=c(Views="red", Likes="blue", Dislikes="purple", Comments="green"))
print(p4)


#Video Game Sales Analysis
# Import data and remove unnecessary columns
games <- read.csv("vgsales.csv", header = TRUE)


# Analyze features using built-in Benford functions
bfdamerica <- benford(games$NA_Sales, number.of.digits = 1)
bfdeurope <- benford(games$EU_Sales, number.of.digits = 1)
bfdjapan <- benford(games$JP_Sales, number.of.digits = 1)

# Using ggplot, plot Benford's predictions
df <- data.frame(x = digits, y = benlaw(digits))
ggBarplot <- ggplot(df, aes(x = factor(x), y = y)) + geom_bar(stat = "identity") + xlab("First Digit") + ylab(NULL)
print(ggBarplot)

# Remove 0s from columns
goodamerica <- fun.zero.omit(games$NA_Sales)
goodeurope <- fun.zero.omit(games$EU_Sales)
goodjapan <- fun.zero.omit(games$JP_Sales)

# create dataframes to use with ggplot
dfamerica <- pctFirstDigit(goodamerica)
dfeurope <- pctFirstDigit(goodeurope)
dfjapan <- pctFirstDigit(goodjapan)

# Plot America, Europe, and Japan sales in ggplot
p1 <- ggBarplot + 
  geom_line(data = dfamerica, 
            aes(x = Var1, y = Freq, group = 1), 
            colour = "red", 
            size = 2) +
  geom_point(data = dfamerica, 
             aes(x = Var1, y = Freq, group = 1), 
             colour = "red", 
             size = 4, pch = 23, bg = "red")
p2 <- p1 +
  geom_line(data = dfeurope, 
            aes(x = Var1, y = Freq, group = 1), 
            colour = "violet", 
            size = 2) +
  geom_point(data = dfeurope, 
             aes(x = Var1, y = Freq, group = 1), 
             colour = "violet", 
             size = 4, pch = 23, bg = "violet")
p3 <- p2 +
  geom_line(data = dfjapan, 
            aes(x = Var1, y = Freq, group = 1), 
            colour = "blue", 
            size = 2) +
  geom_point(data = dfjapan, 
             aes(x = Var1, y = Freq, group = 1), 
             colour = "blue", 
             size = 4, pch = 23, bg = "blue")
print(p3)