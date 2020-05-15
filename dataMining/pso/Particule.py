import numpy as np
from random import randint
# seed random number generator

np.random.seed(42)
class Particule:
    def __init__(self,n,v_max):
        self.size=n
        self.position = np.random.choice(2,n,p=[0.98, 0.02])
        self.pBest = self.position
        self.Vid = randint(0,v_max)

    def fitness(self,df,postion=True):
        if(self.validParticule()):
            supportRegle = np.array([False for _ in range(df.shape[0])])
            supportPremis = np.array([False for _ in range(df.shape[0])])
            enter = False
            if(postion):
                particule=self.position
            else:
                particule=self.pBest
            for i in range(0, self.size, 2):
                index = round(i / 2)
                if (particule[i] == 1):
                    if (particule[i + 1] == 0):
                        # enter the if (particule[i]==1) for the first time
                        if (not enter):
                            # for calculation sup(X)  in X=>Y
                            supportPremis = np.array(df.iloc[:, index] == 1)
                        else:
                            # for calculation sup(X)  in X=>Y
                            supportPremis = supportPremis & np.array(df.iloc[:, index] == 1)

                    # enter the if (particule[i]==1) for the first time
                    if (not enter):
                        # for calculation sup(X=>Y)  in X=>Y
                        supportRegle = np.array(df.iloc[:, index] == 1)
                        enter = True
                    else:
                        # for calculation sup(X=>Y)  in X=>Y
                        supportRegle = supportRegle & np.array(df.iloc[:, index] == 1)
            supportRegle=(supportRegle==True).sum()
            supportPremis=(supportPremis==True).sum()
            if(supportPremis!=0 and supportRegle!=0):
                return (supportRegle/supportPremis)#*supportRegle
            else:
                return 0
        else:
            return 0



    def updatePosition(self): pass

    def updateVelocity(self): pass

    def getRule(self,columns):
        premis = []
        conclusion = []
        for i in range(0, self.size, 2):
            if (self.pBest[i] == 1):
                # if particule has the conclusion part
                if (self.pBest[i + 1] == 1):
                    conclusion.append(columns[i / 2])
                # if particule has the premis part
                else:
                    premis.append(columns[i / 2])
        print('(', end='')
        for pre in premis:
            print(pre, end=',')
        print(')=>', end=' ')
        for con in conclusion:
            print(con, end=',')

    def validParticule(self):
        validConclusion = False
        validPremis = False
        for i in range(0, self.size, 2):
            if (self.position[i] == 1):
                # if particule has the conclusion part
                if (self.position[i + 1] == 1):
                    validConclusion = True
                # if particule has the premis part
                else:
                    validPremis = True
        if (validPremis and validConclusion):
            return True
        else:
            return False



