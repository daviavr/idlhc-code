import math


class Knapsack:
    minimum_size = 100
    min_item_value = 1
    max_item_value = int(math.ceil(1.6 * minimum_size))
    min_weight_value = 1
    max_weight_value = int(math.ceil(1.6 * minimum_size))

    def __init__(self, instance_data):
        self.values = self._get_values(instance_data)
        self.weights = self._get_weights(instance_data)
        self.capacity = self._get_capacity()

    def _get_values(self, instance_data):
        return instance_data["values"]
    
    def _get_weights(self, instance_data):
        return instance_data["weights"]
    
    def _get_capacity(self):
        return math.ceil(0.5 * (sum(self.weights)))

    def get_sorted_ratio_indexes(self):
        ratios = [self.values[i] / self.weights[i] for i in range(len(self.values))]
        sorted_ratio_indexes = sorted(range(len(self.values)), key=lambda i: ratios[i])
        return sorted_ratio_indexes

    def bench(self, individual):
        if len(individual.features) != len(self.values) or len(individual.features) != len(self.weights):
            return False

        total_value = 0
        individual.total_weight = 0

        for count,value in enumerate(individual.features):
            if value != 0 and value != 1:
                return False
            elif value == 1:
                individual.total_weight += self.weights[count]
                total_value += self.values[count]

        return total_value

    def repair(self, individual):
        if individual.total_weight <= self.capacity:
            return individual
        for count,value in enumerate(self.values):
            if individual.total_weight > self.capacity:
                sorted_ratio_indexes = self.get_sorted_ratio_indexes()
                index = sorted_ratio_indexes[count]
                if individual.features[index] == 1:
                    individual.features[index] = 0
                    individual.total_weight -= self.weights[index]
                    individual.objective -= self.values[index]
            else:
                break
        return individual

class UnconstrainedKnapsack:
    minimum_size = 100
    min_item_value = int( -1 * math.ceil(1.6 * minimum_size))
    max_item_value = int(math.ceil(1.6 * minimum_size))
    #min_weight_value = 1
    #max_weight_value = int(math.ceil(1.6 * minimum_size))

    def __init__(self, instance_data):
        self.values = self._get_values(instance_data)
        self.capacity = self._get_capacity()

    def _get_values(self, instance_data):
        return instance_data["values"]
    
    def _get_capacity(self):
        return math.ceil(0.5 * (sum(self.weights)))

    def get_sorted_ratio_indexes(self):
        #ratios = [self.values[i] / self.weights[i] for i in range(len(self.values))]
        sorted_ratio_indexes = sorted(range(len(self.values)), key=lambda i: self.values[i])
        return sorted_ratio_indexes

    def bench(self, individual):
        if len(individual.features) != len(self.values) or len(individual.features) != len(self.weights):
            return False

        total_value = 0
        individual.total_weight = 0

        for count,value in enumerate(individual.features):
            if value != 0 and value != 1:
                return False
            elif value == 1:
                individual.total_weight += self.weights[count]
                total_value += self.values[count]

        return total_value

    #def repair(self, individual):
        #if individual.total_weight <= self.capacity:
            #return individual
        #for count,value in enumerate(self.values):
            #if individual.total_weight > self.capacity:
                #sorted_ratio_indexes = self.get_sorted_ratio_indexes()
                #index = sorted_ratio_indexes[count]
                #if individual.features[index] == 1:
                    #individual.features[index] = 0
                    #individual.total_weight -= self.weights[index]
                    #if self.values[index] > 0:
                        #individual.objective -= self.values[index]
                    #else:
                        #individual.objective += self.values[index] 
            #else:
                #break
        #return individual

class MinMax:
    def __init__():
        pass