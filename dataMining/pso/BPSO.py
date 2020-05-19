
from Particule import Particule
from random import random
import pandas as pd
import time
import math
import numpy as np

class BPSO:
    def __init__(self,df, particule_count=5000,v_max=20, C1=2,C2=2,w_coef=0.4,max_iter=500,n=200,mesure="confidence"):
        """":arg mesure='confidence', 'lift','leverage', 'conviction' """
        self.population = [Particule(n=n,v_max=v_max,mesure=mesure) for _ in range(particule_count)]
        self.mesure="confidence"
        self.df=df
        self.size=n
        self.v_max=v_max
        self.gBest = 0
        self.gBestfitness = 0
        self.max_iter = max_iter
        self.C1 = C1
        self.C2 = C2
        self.r1=random()
        self.r2 = random()
        self.w_coef=w_coef
        self.particule_count=particule_count
        for i  in range(0,particule_count):
            p = self.population[i]
            p.pbestFitness=p.fitness(df=df,postion=False)

            if(p.pbestFitness > self.gBestfitness):
                self.gBest=i
                self.gBestfitness = p.pbestFitness

    def getGbest(self):
        return self.population[self.gBest]
    def run(self):
        for k in range(self.max_iter):
            #print("itiration :{}".format(k))
            for i in range(self.particule_count):
                p = self.population[i]
                vid=p.Vid
                p.Vid=self.w_coef * vid + self.C1 * self.r1 * self.hamming_distance(p.pBest,p.position) + self.C2 * self.r2 * self.hamming_distance(self.getGbest().pBest,p.position)

#                if (p.Vid > self.v_max):
#                    p.Vid =self.v_max
                if(random() > self.sigmoid(p.Vid)):
                    #print("iter = {}, done".format(k))
                    p.Vid=1
                    p.updatePosition(self.df)
                if ( p.pbestFitness > self.gBestfitness):
                    self.gBest = i
                    self.gBestfitness = p.pbestFitness


    def hamming_distance(self,p1,p2):
        return ((p1 != p2) == True).sum()

    def sigmoid(self,x):
        return 1 / (1 + math.exp(-x))



def association_rule_mining(df,particule_count=5000,v_max=20, C1=2,C2=2,w_coef=0.4,max_iter=500,mesure="confidence",m=10):
    particules=[]
    i=0
    while(i<m):
        instance = BPSO(df=df,n=2*len(df.columns),particule_count=particule_count,max_iter=max_iter,mesure=mesure)
        instance.run()
        gbest = instance.getGbest()
        exist = False
        for particule in particules:
            if particule.equal(gbest):
                exist=True
                break
        if not exist:
            particules.append(gbest)
            i += 1
    output = []
    for particule in particules:
        particule.getRule(columns=df.columns)
        if(particule.confidence>0):
            output.append([particule.premis,particule.conclusion,particule.support,particule.confidence,particule.lift,particule.leverage,particule.conviction])
        #print(" confidence = {}, support = {} lift = {}, leverage  = {}, conviction = {}".format(particule.confidence,particule.support,particule.lift,particule.leverage,particule.conviction))
    columns=["antecedents","consequents","support","confidence","lift","leverage","conviction"]
    output_df = pd.DataFrame(output,columns=columns)
    return output_df



if __name__ == '__main__':

    df= pd.read_csv('../../dataSource/market/marketBool.csv')
    df=df.sample(n=3000, replace=False)
    start_time = time.time()
    output = association_rule_mining(df=df,particule_count=1000,max_iter=10,mesure="lift", m=15)
    print("--- %s seconds ---" % (time.time() - start_time))

     #%%
    #print(output.to_string())
    output.to_csv('../../output/dataMining/BPSO_ar.csv',index=False)

