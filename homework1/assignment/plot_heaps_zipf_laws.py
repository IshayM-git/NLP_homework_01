import json
import pickle
import os.path
from collections import defaultdict
from matplotlib import pyplot as plt
from math import log
import seaborn as sn
sn.set()


def read_data(filename):
    word2freq = defaultdict(int)

    i = 0

    N = 0   # Total words counter
    step = 10000
    x = []  # Collecting data for heaps law plotting
    y = []  # Collecting data for heaps law plotting

    with open(filename, 'r', encoding='utf-8') as fin:
        print('reading the text file...')
        for i, line in enumerate(fin):
            for word in line.split():
                word2freq[word] += 1

                # Collecting data for heaps law plotting
                N += 1
                if N % step == 0:
                    x.append(N)
                    y.append(len(word2freq))

            if i % 100000 == 0:
                print(i)

        # Save the final point
        if N > 0 and N % step != 0:
            x.append(N)
            y.append(len(word2freq))

    total_words = sum(word2freq.values())
    word2nfreq = {w: word2freq[w]/total_words for w in word2freq}

    return (word2nfreq, x, y)


def plot_zipf_law(word2nfreq):
    y = sorted(word2nfreq.values(), reverse=True)
    x = list(range(1, len(y)+1))

    product = [a * b for a, b in zip(x, y)]
    print(product[:1000])  # todo: print and note the roughly constant value

    y = [log(e, 2) for e in y]
    x = [log(e, 2) for e in x]

    plt.plot(x, y)
    plt.xlabel('log(rank)')
    plt.ylabel('log(frequency)')
    plt.title("Zipf's law")
    plt.show()

def plot_heaps_law(x, y):
    plt.plot(x, y)
    plt.xlabel('Number of tokens (N)')
    plt.ylabel('Vocabulary size (V)')
    plt.title("Heaps' law")
    plt.show()

if __name__ == '__main__':
    with open('config.json', 'r', encoding='utf-8') as json_file:
        config = json.load(json_file)

    if not os.path.isfile('word2nfreq.pkl') or not os.path.isfile('x.pkl') or not os.path.isfile('y.pkl'):
        data = read_data(config['corpus'])
        pickle.dump(data[0], open('word2nfreq.pkl', 'wb'))
        pickle.dump(data[1], open('x.pkl', 'wb'))
        pickle.dump(data[2], open('y.pkl', 'wb'))

    plot_zipf_law(pickle.load(open('word2nfreq.pkl', 'rb')))
    plot_heaps_law(
        pickle.load(open('x.pkl', 'rb')),  # x
        pickle.load(open('y.pkl', 'rb'))   # y
    )
