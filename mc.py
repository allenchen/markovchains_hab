from mcutil import *

# N value for n-gram
# 1 for monogram
# 2 for bigram
# etc.
N = 7

def train(data, model, run_filter):
    ' '.join(data.split())
    if run_filter:
        data = filter(lambda x: x.isalpha() or x == ' ' or x == '.', data.lower())

    buffer = data[:N]
    for letter in data[N:]:
        model.observe(buffer[-1], letter, buffer[:-1])
        buffer = buffer[1:] + letter

def sample(model, length):
    node, state = model.begin_sampling()
    result = ""
    for i in xrange(length):
        sample = model.sample(node, state)
        state += node
        state = state[1:]
        node = sample
        result += sample
        #print "Node: " + node + " State: " + state
    return result

#model = MarkovChain()
       
#train(sample_corpus, model)

#print sample(model, 10000)
