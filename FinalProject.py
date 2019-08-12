# -*- coding: utf-8 -*-
"""
Created on Sat August 10 16:51:43 2019
DSC530 Final Project
Nick Miller
"""

from __future__ import print_function, division

import pandas as pd
import numpy as np
import thinkplot
import thinkstats2
import statsmodels.formula.api as smf


class DiffMeansPermute(thinkstats2.HypothesisTest):

    def TestStatistic(self, data):
        group1, group2 = data
        test_stat = abs(group1.mean() - group2.mean())
        return test_stat

    def MakeModel(self):
        group1, group2 = self.data
        self.n, self.m = len(group1), len(group2)
        self.pool = np.hstack((group1, group2))

    def RunModel(self):
        np.random.shuffle(self.pool)
        data = self.pool[:self.n], self.pool[self.n:]
        return data
        
        
class HypothesisTest(object):

    def __init__(self, data):
        self.data = data
        self.MakeModel()
        self.actual = self.TestStatistic(data)

    def PValue(self, iters=1000):
        self.test_stats = [self.TestStatistic(self.RunModel()) 
                           for _ in range(iters)]

        count = sum(1 for x in self.test_stats if x >= self.actual)
        return count / iters

    def TestStatistic(self, data):
        raise UnimplementedMethodException()

    def MakeModel(self):
        pass

    def RunModel(self):
        raise UnimplementedMethodException()
        
        
df = pd.read_csv(r'FinalProjectDataset.csv')

#Cleaning data
#Removing rows with blank entries
df['Year'].replace('', np.nan, inplace=True)
df.dropna(subset=['Year'], inplace=True)
df['Age'].replace('', np.nan, inplace=True)
df['Age'].replace('Unknown', np.nan, inplace=True)
df.dropna(subset=['Age'], inplace=True)
df['Sex'].replace('', np.nan, inplace=True)
df['Sex'].replace('Unknown', np.nan, inplace=True)
df.dropna(subset=['Sex'], inplace=True)
df['Race'].replace('', np.nan, inplace=True)
df['Race'].replace('Unknown', np.nan, inplace=True)
df['Race'].replace('Other', np.nan, inplace=True)
df.dropna(subset=['Race'], inplace=True)
df['Drug'].replace('', np.nan, inplace=True)
df['Drug'].replace('Unknown', np.nan, inplace=True)
df.dropna(subset=['Drug'], inplace=True)
#change data types
df['Year'] = df['Year'].astype(int)
df['Age'] = df['Age'].astype(int)

#create histograms and report characterisitics
histYear = thinkstats2.Hist(df.Year)
thinkplot.Hist(histYear)
print("mean is", df.Year.mean())
print("mode is", max(df.Year.mode()))
print("variance is", df.Year.var())
print("standard deviation is", df.Year.std())
histAge = thinkstats2.Hist(df.Age)
thinkplot.Hist(histAge, width = 1)
print("mean is", df.Age.mean())
print("mode is", max(df.Age.mode()))
print("variance is", df.Age.var())
print("standard deviation is", df.Age.std())
histSex = thinkstats2.Hist(df.Sex)
thinkplot.Hist(histSex)
histRace = thinkstats2.Hist(df.Race)
thinkplot.Hist(histRace)
histDrug = thinkstats2.Hist(df.Drug)
thinkplot.Hist(histDrug)

#creates PMFs
#divide out subjects by sex
male = df[df.Sex == 'Male']
female = df[df.Sex == 'Female']
#perform pmf
male_pmf = thinkstats2.Pmf(male.Drug, label='Male')
female_pmf = thinkstats2.Pmf(female.Drug, label='Female')
#plot pmf
width = 0.45
thinkplot.PrePlot(2)
thinkplot.Hist(male_pmf, width = width, align='left', color='blue')
thinkplot.Hist(female_pmf, width = width, align='right', color='red')
thinkplot.Config(ylabel='Probability')

#plot CDF
cdf = thinkstats2.Cdf(df.Age)
thinkplot.Cdf(cdf)
thinkplot.Config(xlabel='Age', ylabel='CDF')

#plot normal distribution
mean = df.Age.mean()
std = df.Age.std()
xs = [-4, 4]
fxs, fys = thinkstats2.FitLine(xs, inter=mean, slope=std)
thinkplot.Plot(fxs, fys, color='gray', label='model')
xs, ys = thinkstats2.NormalProbability(df.Age)
thinkplot.Plot(xs, ys, label='Age')

#scatter plots and correlation
#year vs. age
year = thinkstats2.Jitter(df.Year, .25)
thinkplot.Scatter(year, df.Age)
thinkplot.Show(xlabel='Year', ylabel='Age')
thinkstats2.Corr(df.Year, df.Age)
#drug vs. age 
thinkplot.Scatter(df.Age, df.Drug)
thinkplot.Show(xlabel='Age', ylabel='Drug')

#testing a difference in gender
data = male.Age.values, female.Age.values
ht = DiffMeansPermute(data)
pvalue = ht.PValue()
print(pvalue)
ht.PlotCdf()
thinkplot.Config(xlabel='test statistic',
                   ylabel='CDF')
