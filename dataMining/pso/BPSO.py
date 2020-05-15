
from Particule import Particule
import pandas as pd
import numpy as np
np.random.seed(42)
class BPSO:
    def __init__(self,df, particule_count=5000,v_max=20, C1=2,C2=2,w_coef=0.4,max_iter=500,n=200):
        self.population = [Particule(n=n,v_max=v_max) for _ in range(particule_count)]
        self.gBest = 0
        self.gBestfitness = 0
        self.max_iter = max_iter
        self.C1 = C1
        self.C2 = C2
        self.w_coef=w_coef
        self.particule_count=particule_count
        for i  in range(0,particule_count):
            p = self.population[i]
            pbestFitness=p.fitness(df=df,postion=False)
            if(pbestFitness > self.gBestfitness):
                self.gBest=i
                self.gBestfitness=pbestFitness
                #print(pbestFitness)
                #print(self.gBestfitness)
                #print(p.validParticule())
                #print(p.getRule(df.columns))
                self.population[self.gBest].getRule(columns=df.columns)
                print(self.gBestfitness)

    def getGbest(self):
        return self.population[self.gBest]
    def run(self):
        for _ in range(self.max_iter):
            for i in range(self.particule_count):
                p = self.population[i]
                p.updateVelocity()
                p.updatePosition()


if __name__ == '__main__':

    df= pd.read_csv('../../dataSource/market/market.csv')
    instance = BPSO(df=df,n=2*len(df.columns))
    #gbest = instance.getGbest()
    #print(gbest.getRule(columns=df.columns))
    #print(gbest.fitness(df=df))