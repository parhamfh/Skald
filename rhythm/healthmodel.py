import viterbi, numpy

class HealthState:
    def __init__(self,n,condition):
        self.i = n
        self.condition = condition

    def __str__(self):
        return self.condition

    def __repr__(self):
        return self.condition

class HealthObservation:
    def __init__(self,observed_state):
        self.observed_state = observed_state

    @property 
    def feeling(self):
        return self.observed_state

H = [HealthState(0,'Healthy'), HealthState(1,'Fever')]
 
observed = [HealthObservation('normal'), 
            HealthObservation('cold'),
            HealthObservation('dizzy')]
 
start_p = [0.6, 0.4]  # index 0 'Healthy'
                      # index 1 'Fever'

'''transition_probability = {
   'Healthy' : {'Healthy': 0.7, 'Fever': 0.3},
   'Fever' : {'Healthy': 0.4, 'Fever': 0.6},
   }'''
'''emission_probability = {
   'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
   'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6},
}'''

T = numpy.matrix(
    [[0.7, 0.3],
   [0.4, 0.6]])

def health_p(state, emission):
    e_p = [{'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
           {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}]
    return e_p[state.i][emission.feeling]

xpath = viterbi.viterbi(observed,H,T,start_p,health_p)
for x in xpath:
    print x