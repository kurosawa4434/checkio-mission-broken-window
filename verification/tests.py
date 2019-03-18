"""
TESTS is a dict with all you tests.
Keys for this will be categories' names.
Each test is dict with
    "input" -- input data for user function
    "answer" -- your right answer
    "explanation" -- not necessary key, it's using for additional info in animation.
"""
from random import randint, choice, shuffle


def make_randoms(num):
    for _ in range(num):
        width = randint(4, 20)
        height = randint(2, width-2)

        tops = []
        bottoms = []
        b = randint(0, height)
        tp = [b]
        bt = [height-b]
        prev = b
        for w in range(width):

            # vertical break
            if w < width-1:
                v = choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3])
                if v == 1 and len(tp) >= 2 and tp[-1] != 0:
                    tops.append(tuple(reversed(tp)))
                    tp = [tp[-1]]
                    continue
                elif v == 2 and len(bt) >= 2 and bt[-1] != height:
                    bottoms.append(tuple(bt))
                    bt = [bt[-1]]
                    continue
                elif v == 3 and len(bt) >= 2 and len(tp) >= 2:
                    tops.append(tuple(reversed(tp)))
                    bottoms.append(tuple(bt))
                    tp = []
                    bt = []
                    prev = -1

            while True:
                b = randint(0, height)
                if b != prev or b not in (0, height):
                    break

            tp.append(b)
            bt.append(height-b)
            if len(tp) >= 2 and (w == width-1 or b == 0):
                tops.append(tuple(reversed(tp)))
                tp = [b]
            if len(bt) >= 2 and (w == width-1 or b == height):
                bottoms.append(tuple(bt))
                bt = [height-b]
            prev = b

        ls = list(map(list, tops+bottoms))
        shuffle(ls)
        yield ls, height


basics = [
    ([[0, 1], [0, 1]], 1),
    ([[0, 3, 4, 1], [4, 0], [3, 0], [0, 1, 4, 0]], 4),
]

edges = [
    ([[1, 1], [1, 1], [1, 1], [1, 1]], 2),
]

make_tests = lambda tests: [{'input': t, 'answer': t, 'explanation': h} for t, h in tests]

TESTS = {
    "Basics": make_tests(basics),
    "Edges": make_tests(edges),
    "Randoms": make_tests(make_randoms(10)),
}

