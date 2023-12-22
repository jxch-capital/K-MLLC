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
    def __init__(self, features, info=None, prediction=None):
        self.info = info
        self.features = features
        if prediction is not None:
            self.prediction = prediction
            self.diction = Diction.press_of_prediction(self.prediction)

        self.neighbor_nodes = []

    def score(self, neighbor_nodes):
        self.neighbor_nodes = neighbor_nodes
        self.prediction = sum([neighbor.node.prediction for neighbor in neighbor_nodes])
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
        distance = lorentzian_distance(x.features, y.features, size)
        if len(min_dist_k_nodes) < k:
            min_dist_k_nodes.append(NearestNeighbor(y, distance))
            min_dist_k_nodes.sort(key=lambda x: x.distance)
        elif distance < min_dist_k_nodes[-1].distance:
            min_dist_k_nodes.append(NearestNeighbor(y, distance))
            min_dist_k_nodes.sort(key=lambda x: x.distance)
            min_dist_k_nodes.pop()

    return min_dist_k_nodes


def train_data_by_df(df, features_definition, source='Close', future_count=4):
    train_data = []
    position = 0
    for index, row in df.iterrows():
        next_position = position + future_count
        position = position + 1
        if next_position < len(df):
            features = [row[name] for name in features_definition.features_names()]
            target_row = df.iloc[next_position]
            k_node = KNode(features, prediction=Diction.press_of_prediction(target_row[source] - row[source]).value)
            train_data.append(k_node)
    return train_data


def test_data_by_df(df, features_definition, source='Close', future_count=4):
    test_data = []
    position = 0
    for index, row in df.iterrows():
        next_position = position + future_count
        position = position + 1
        if next_position < len(df):
            features = [row[name] for name in features_definition.features_names()]
            target_row = df.iloc[next_position]

            the_d = Diction.NEUTRAL
            if target_row[source] > row[source] and target_row['Low'] > row['Low']:
                the_d = Diction.LONG
            elif target_row[source] < row[source] and target_row['High'] < row['High']:
                the_d = Diction.SHORT
            k_node = KNode(features, prediction=Diction.press_of_prediction(target_row[source] - row[source]).value,
                           info=row)
            test_data.append(k_node)
    return test_data


def prediction2node(row, train_data, features_definition, k=8):
    features = [row[name] for name in features_definition.features_names()]
    current_node = KNode(features)
    neighbor_node = lorentzian_k_nearest_neighbor(current_node, train_data, features_definition.features_num(), k)
    current_node.score(neighbor_node)
    return current_node
