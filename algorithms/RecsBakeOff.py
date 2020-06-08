# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 10:41:49 2020

@author: Hassaine
"""
import os, sys,inspect
from surprise import SVD
from surprise import SVDpp
from surprise import   KNNBasic
from dataLoader.MovieLens import MovieLens
from dataLoader.AmazonRating import AmazonRating
from evaluation.Evaluator import Evaluator

from surprise import NormalPredictor
from collections import defaultdict
from surprise.model_selection import cross_validate
# from test.GA import GA
# ga = GA()
# print(ga.getPopulation())


#currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#parentdir = os.path.dirname(currentdir)
#sys.path.append(parentdir)
#sys.path.append(parentdir+"\\evaluation")
#sys.path.append(parentdir+"\\dataLoader")




import random
import numpy as np

def LoadMovieLensData():
    ml = MovieLens()
    print("Loading movie ratings...")
    data = ml.loadMovieLensLatestSmall()
    print("\nComputing movie popularity ranks so we can measure novelty later...")
    rankings = ml.getPopularityRanks()
    return (ml,data, rankings)

def LoadAmazonData():
    azr = AmazonRating()
    print("Loading amazon ratings...")
    data = azr.loadAmazonRating()
    print("\nComputing amazon product popularity ranks so we can measure novelty later...")
    rankings = azr.getPopularityRanks()
    #rankings = defaultdict(int)
    return (azr,data,rankings)

# Load up common data set for the recommender algorithms
(ml,evaluationData, rankings) = LoadMovieLensData()

#(azr,evaluationData, rankings) = LoadAmazonData()

# Construct an Evaluator to, you know, evaluate them




######### our evaluation code #########

evaluator = Evaluator(evaluationData,rankings,doTopN=True)

SVDAlgorithm = SVDpp()
evaluator.AddAlgorithm(SVDAlgorithm, "SVD++")
#SVDppAlgorithm = SVDpp()
#evaluator.AddAlgorithm(SVDppAlgorithm, "SVD++")
evaluator.Evaluate()

#evaluator.SampleTopNRecs(ml)



### buit-in fonction for evaluation #######"

#algo = SVD()

# Run 3-fold cross-validation and print results
#cross_validate(algo, evaluationData, measures=['RMSE', 'MAE'], cv=3, verbose=True)





# Retrieve the trainset.
#trainset = evaluationData.build_full_trainset()

# Build an algorithm, and train it.
#algo = KNNBasic()
#algo.fit(trainset)
#uid = "A3FANY5GOT5X0W"
#iid = "0176496920"
uid = "83"
iid = "31"
 #%%
evaluator.SampleTopNRecs(ml=ml)
##pred=SVDAlgorithm.predict( )
#print(pred)
# get a prediction for specific users and items.
#pred = algo.predict(uid, iid, r_ui=4, verbose=True)
#print(pred)
