from common.individual import Individual
from math import cos
import random

class ChaosMaps:
    salt = random.random() * (10 ** -10)
    current_value = None
    def __init__(self,variables_range,num_of_variables):
        self.floor = min(variables_range)
        self.ceiling = max(variables_range)
        self.num_of_variables = num_of_variables
        self.n_first = 20

    def _convert_01_to_range(self,floor:int, ceiling:int, random_number:int):
        if random_number < 0:
            random_number *= -1
        return round(((self.ceiling - self.floor) * random_number) + self.floor)
    
    def generic_logistic_map(self,features):
        features = [0.254561 if ChaosMaps.current_value == None else ChaosMaps.current_value]
        r = 3.999999301 + ChaosMaps.salt
        for n in range(self.num_of_variables + self.n_first):
            features.append( r*features[n]*(1-features[n]) )
        del features[:self.n_first+1]

        ChaosMaps.current_value = features[-1]
        features = [self._convert_01_to_range(self.floor,self.ceiling,i) for i in features]
        return features
   
    def cosin_map_generation(self,features):
        features = [0.1 if ChaosMaps.current_value == None else ChaosMaps.current_value]
        r = 6 + ChaosMaps.salt
        for n in range(self.num_of_variables+self.n_first):
            features.append( cos(r*features[n]) )
        del features[:self.n_first+1]
        
        ChaosMaps.current_value = features[-1]
        
        if self.floor == 0 and self.ceiling == 1:
            features = [0 if i <= 0 else 1 for i in features]
        else:
            features = [self._convert_01_to_range(self.floor,self.ceiling,i) for i in features]
        
        return features