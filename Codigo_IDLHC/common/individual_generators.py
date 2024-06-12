from scipy.stats import qmc
import random
import numpy as np

def quantization(floor:int, ceiling:int, random_number:int):
    discretizations = (ceiling - floor) + 1 
    for discrete_number in range(floor, discretizations):
        numerator = discrete_number + 1 if floor == 0 else discrete_number  
        if random_number <= numerator/discretizations:
            break
    return discrete_number

class ChaosMaps:
    salt = random.random()
    current_value = None
    def __init__(self,variables_range,num_of_variables):
        self.floor = min(variables_range)
        self.ceiling = max(variables_range)
        self.num_of_variables = num_of_variables

    
    def generic_logistic_map(self):
        r = 3.999999301
        
        features = [ChaosMaps.salt if ChaosMaps.current_value == None else ChaosMaps.current_value] 
        
        for n in range(self.num_of_variables-1):
            features.append( r*features[n]*(1-features[n]) )

        ChaosMaps.current_value = features[-1]
        features = [quantization(self.floor,self.ceiling,i) for i in features]
        return features
   
    def cosin_map_generation(self):
        r = 6
        
        features = [ChaosMaps.salt if ChaosMaps.current_value == None else ChaosMaps.current_value] 

        for n in range(self.num_of_variables-1):
            features.append( np.cos(r*features[n]) )
        
        ChaosMaps.current_value = features[-1]
        
        features = [quantization(self.floor,self.ceiling,abs(i)) for i in features]
        return features

class BetaFunctionVariations:
    def __init__(self,variables_range,num_of_variables):
        self.floor = min(variables_range)
        self.ceiling = max(variables_range)
        self.num_of_variables = num_of_variables

    def latin_hypercube(self):
        features = qmc.LatinHypercube(d=1).random(n=self.num_of_variables).flatten()
        features_discretized = [quantization(self.floor,self.ceiling,num) for num in features]
        return features_discretized
