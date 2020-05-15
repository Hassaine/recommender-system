# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 10:40:48 2020

@author: Hassaine
"""

from surprise import Dataset
from surprise import Reader
import os, sys ,csv
from collections import defaultdict
import numpy as np
import pandas as pd


class AmazonRating:
    itemID_to_name = {}
    name_to_itemID = {}
    ratingsPath = '../dataSource/amazon/amazon_rating_reduced_finale.csv'
    itemPath = '../meta.csv'

    def loadAmazonRating(self):

        # Look for files relative to the directory we are running from
        os.chdir(os.path.dirname(sys.argv[0]))

        ratingsDataset = 0
        self.itemID_to_name = {}
        self.name_to_itemID = {}

        reader = Reader(rating_scale=(1, 5))
        #columns = ['asin', 'reviewerID', 'overall']

        df = pd.read_csv(self.ratingsPath)
        #df = df.sample(50000,random_state=42)



        data = Dataset.load_from_df(df[['reviewerID', 'asin', 'overall']], reader)

        return data

    def getPopularityRanks(self):
        df = pd.read_csv(self.ratingsPath)
        rankingitemList = df.groupby('asin')['reviewerID'].count().reset_index().sort_values('reviewerID', ascending=False)[
            'asin'].tolist()
        rankings = defaultdict(int)
        rank = 1
        for asin in rankingitemList:
            rankings[asin] = rank
            rank += 1
        return rankings
    def getUserRating(self,user):
        userRating=[]
        df = pd.read_csv(self.ratingsPath)
        for index, row in df[df.reviewerID == user].T.iteritems():
            userRating.append((row[0], row[2]))
        return userRating

if __name__ == '__main__':
    amazon = AmazonRating()
    #data = amazon.loadAmazonRating()
    ranking = amazon.getPopularityRanks()
    userRating = amazon.getUserRating('A1JB7HFWHRYHT7')



