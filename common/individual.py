class Individual(object):

    def __init__(self, direction):
        self.id = 0 # id do indivíduo
        self.objective = None # valor da função objetivo
        self.direction = direction # direção (se MAX ou MIN)
        self.total_weight = 0        
        self.features = [] #vetor de decisão

    #     if self.direction == "MAX":
    #         if self.objective > other_individual.objective:
    #             condition = True
    #         else:
    #             condition = False
    #     return condition

