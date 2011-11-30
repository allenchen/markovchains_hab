import collections
import random

class TMap():
    def __init__(self):
        self.stateCountMap = collections.defaultdict(int)
        self.stateMap = {}

    def observe(self, transition, state):
        if state not in self.stateMap:
            self.stateMap[state] = collections.defaultdict(int)
        self.stateMap[state][transition] += 1
        self.stateCountMap[state] += 1

    def sample(self, state):
        #print self.stateMap
        total = self.stateCountMap[state]
        if total == 0:
            # Downgrade the state and continue to retry
            for i in xrange(len(state)):
                state = state[1:]
                if (self.stateCountMap[state] > 0):
                    return self.sample(state)

            # Fall through - bad training data probably.
            # Just pick a completely random example. (similar to smoothing)
            return random.choice(self.stateMap[random.choice(self.stateMap.keys())].keys())

        r = random.randrange(1, total + 1)

        count = 0
        for k,v in self.stateMap[state].iteritems():
            if (r > count and r <= count + v):
                return k
            count += v
        
        assert False, "Sampling error."
        return None
        
class MarkovChain():
    def __init__(self):
        self.nodes = {}

    def observe(self, node, transition, state):
        if node not in self.nodes:
            self.nodes[node] = TMap()
        self.nodes[node].observe(transition, state)
    
    def sample(self, node, state):
        if node not in self.nodes:

            # No transition at all found, probably due to bad training data.
            return None
                    
                
        return self.nodes[node].sample(state)

    def begin_sampling(self):
        node = random.choice(self.nodes.keys())
        #print "Random choice of node: " + node
        state = random.choice(self.nodes[node].stateMap.keys())
        #print "Random choice of state: " + state
        return node,state
