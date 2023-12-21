import math
from operator import attrgetter
from enum import Enum


class Diction(Enum):
    LONG = 1
    SHORT = -1
    NEUTRAL = 0

    @staticmethod
    def press_of_prediction(score):
        if score < 0:
            return Diction.SHORT
        if score == 0:
            return Diction.NEUTRAL
        if score > 0:
            return Diction.LONG


class KNode:
    def __init__(self, info, features, prediction=None):
        self.info = info
        self.features = features
        if prediction is not None:
            self.prediction = prediction
            self.diction = Diction.press_of_prediction(self.prediction)

    def score(self, predictions):
        self.prediction = sum(predictions)
        self.diction = Diction.press_of_prediction(self.prediction)


class NearestNeighbor:
    def __init__(self, node, distance):
        self.node = node
        self.distance = distance


def lorentzian_distance(x, y, size):
    if len(x) != len(y):
        raise ValueError('x and y must have the same length')
    return sum(math.log(1 + abs(x[i] - y[i])) for i in range(size))


def lorentzian_k_nearest_neighbor(x, y_arr, size, k=8):
    min_dist_k_nodes = []
    for y in y_arr:
        distance = lorentzian_distance(x.feature, y.feature, size)
        if len(min_dist_k_nodes) < k:
            min_dist_k_nodes.append(NearestNeighbor(y, distance))
            sorted(min_dist_k_nodes, key=attrgetter('distance'))
        elif distance < min_dist_k_nodes[-1].distance:
            min_dist_k_nodes.append(NearestNeighbor(y, distance))
            sorted(min_dist_k_nodes, key=attrgetter('distance'))
            min_dist_k_nodes.pop()

    return min_dist_k_nodes
