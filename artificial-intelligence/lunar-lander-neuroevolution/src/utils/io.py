import config as cfg

def load_bests(fname):
    # Load bests from file
    bests = []
    with open(fname, 'r') as f:
        for line in f:
            fitness, shape, genotype = line.split('\t')
            bests.append(( eval(fitness),eval(shape), eval(genotype)))
    return bests

def save_bests(bests, filename):
    with open(filename, 'w') as f:
        for b in bests:
            f.write(f'{b[1]}\t{cfg.SHAPE}\t{b[0]}\n')
