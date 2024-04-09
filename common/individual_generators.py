from common.individual import Individual
from scipy.stats import qmc,rayleigh
from math import cos
import random


def convert_01_to_range(floor:int, ceiling:int, random_number:int):
    return round(((ceiling - floor) * random_number) + floor)

class ChaosMaps:
    salt = random.random() * (10 ** -10)
    current_value = None
    def __init__(self,variables_range,num_of_variables):
        self.floor = min(variables_range)
        self.ceiling = max(variables_range)
        self.num_of_variables = num_of_variables

    
    def generic_logistic_map(self):
        r = 3.999999301 + ChaosMaps.salt
        
        if ChaosMaps.current_value == None:
            features = [0.254561]
            for n in range(8):
                features.append(r * features[n] * (1-features[n]))
            features = [features[-1]]
        else:
            features = [ChaosMaps.current_value] 
        
        for n in range(self.num_of_variables-1):
            features.append( r*features[n]*(1-features[n]) )

        ChaosMaps.current_value = features[-1]
        features = [convert_01_to_range(self.floor,self.ceiling,i) for i in features]
        return features
   
    def cosin_map_generation(self):
        r = 6 + ChaosMaps.salt
        
        if ChaosMaps.current_value == None:
            features = [0.1]
            for n in range(8):
                features.append( cos(r*features[n]) )
            features = [features[-1]]
        else:
            features = [ChaosMaps.current_value] 
        
        for n in range(self.num_of_variables-1):
            features.append( cos(r*features[n]) )
        
        ChaosMaps.current_value = features[-1]
        
        if self.floor == 0 and self.ceiling == 1:
            features = [0 if i <= 0 else 1 for i in features]
        else:
            features = [convert_01_to_range(self.floor,self.ceiling,abs(i)) for i in features]
        return features

class QuasiRandomNumberSequences():
    def __init__(self,variables_range,num_of_variables):
        self.floor = min(variables_range)
        self.ceiling = max(variables_range)
        self.num_of_variables = num_of_variables
    
    def sobol_sequence(self):
        features_01 = qmc.Sobol(d=1).random(self.num_of_variables).flatten()
        features = [convert_01_to_range(floor=self.floor,ceiling=self.ceiling,random_number=n) for n in features_01]
        print(features)
        return features


class BetaFunctionVariatios:
    def __init__(self,variables_range,num_of_variables):
        self.floor = min(variables_range)
        self.ceiling = max(variables_range)
        self.num_of_variables = num_of_variables

    def latin_hypercube(self):
        features_01 = qmc.LatinHypercube(d=1).random(self.num_of_variables).flatten()
        features = [convert_01_to_range(floor=self.floor,ceiling=self.ceiling,random_number=n) for n in features_01]
        return features

    #def multinomial(self):
        #features_01 = qmc.MultinomialQMC(pvals=[0.2, 0.4, 0.4],engine=qmc.Halton(d=1)).random(self.num_of_variables)
        #features = [convert_01_to_range(floor=self.floor,ceiling=self.ceiling,random_number=n) for n in features_01]
        #return features
    #def levy
    #def rayleigh(self):
        #features_01 = rayleigh.rvs(size=self.num_of_variables)
        #features = [convert_01_to_range(floor=self.floor,ceiling=self.ceiling,random_number=n) for n in features_01]
        #return features
