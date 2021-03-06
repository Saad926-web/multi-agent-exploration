import math
import copy
import numpy as np
from config.Config import Config
from utils.util_functions import stateNameToCoords, l2_distance

class Node:
    def __init__(self, id):
        self.id = id
        # dictionary of parent node ID's
        # key = id of parent
        # value = (edge cost,)
        self.parents = {}
        # dictionary of children node ID's
        # key = id of child
        # value = (edge cost,)
        self.children = {}
        # g approximation
        self.g = float('inf')
        # rhs value
        self.rhs = float('inf')

    def __str__(self):
        return 'Node: ' + self.id + ' g: ' + str(self.g) + ' rhs: ' + str(self.rhs)

    def __repr__(self):
        return self.__str__()

    def update_parents(self, parents):
        self.parents = parents


class Graph:
    def __init__(self):
        self.graph = {}

    def __str__(self):
        msg = 'Graph:'
        for i in self.graph:
            msg += '\n  node: ' + i + ' g: ' + \
                str(self.graph[i].g) + ' rhs: ' + str(self.graph[i].rhs)
        return msg

    def __repr__(self):
        return self.__str__()

    def setStart(self, id):
        if(self.graph[id]):
            self.start = id
        else:
            raise ValueError('start id not in graph')

    def setGoal(self, id):
        if(self.graph[id]):
            self.goal = id
        else:
            raise ValueError('goal id not in graph')


def addNodeToGraph(graph, id, neighbors, edge=1):
    node = Node(id)
    for i in neighbors:
        # print(i)
        node.parents[i] = edge
        node.children[i] = edge
    graph[id] = node
    return graph


# def makeGraph():
#     graph = {}

#     # 8-connected graph (w diagonals)
#     # Impossible to find path - 2 obstacles in middle
#     # graph = addNodeToGraph(graph, 'x1y1', ['x1y2', 'x2y1', 'x2y2'])
#     # graph = addNodeToGraph(
#     #     graph, 'x2y1', ['x1y1', 'x1y2', 'x3y1', 'x2y2', 'x3y2'], float('inf'))
#     # graph = addNodeToGraph(graph, 'x1y2', ['x1y1', 'x2y1', 'x2y2'])
#     # graph = addNodeToGraph(
#     #     graph, 'x2y2', ['x1y1', 'x1y2', 'x3y1', 'x2y1', 'x3y2'], float('inf'))
#     # graph = addNodeToGraph(graph, 'x3y1', ['x3y2', 'x2y1', 'x2y2'])
#     # graph = addNodeToGraph(graph, 'x3y2', ['x3y1', 'x2y1', 'x2y2'])

#     # 8-connected graph (w diagonals)
#     # Impossible to find path - 2 obstacles in middle
#     # graph = addNodeToGraph(graph, 'x1y1', ['x1y2', 'x2y1', 'x2y2'])
#     # graph = addNodeToGraph(
#     #     graph, 'x2y1', ['x1y1', 'x1y2', 'x3y1', 'x2y2', 'x3y2'], float('inf'))
#     # graph = addNodeToGraph(graph, 'x1y2', ['x1y1', 'x2y1', 'x2y2'])
#     # graph = addNodeToGraph(
#     #     graph, 'x2y2', ['x1y1', 'x1y2', 'x3y1', 'x2y1', 'x3y2'])
#     # graph = addNodeToGraph(graph, 'x3y1', ['x3y2', 'x2y1', 'x2y2'])
#     # graph = addNodeToGraph(graph, 'x3y2', ['x3y1', 'x2y1', 'x2y2'])

#     # 4-connected graph (w/out diagonals)
#     graph = addNodeToGraph(graph, 'x1y1', ['x1y2', 'x2y1'])
#     graph = addNodeToGraph(graph, 'x2y1', ['x1y1', 'x3y1', 'x2y2'])
#     graph = addNodeToGraph(graph, 'x1y2', ['x1y1', 'x2y2'])
#     graph = addNodeToGraph(graph, 'x2y2', ['x1y2', 'x2y1', 'x3y2'])
#     graph = addNodeToGraph(graph, 'x3y1', ['x3y2', 'x2y1'])
#     graph = addNodeToGraph(graph, 'x3y2', ['x3y1', 'x2y2'])

#     g = GridWorld(X_DIM, Y_DIM)
#     # g.graph = graph
#     # print(g)
#     return g


def get_closest_vertex_coords_on_graph_from_pos(graph, pos_x, pos_y, edge_cost):

    temp_x = pos_x
    temp_y = pos_y
    temp_dist = math.inf

    for el in graph:
        temp_coords = stateNameToCoords(el, edge_cost)
        new_temp_dist = l2_distance(temp_x, temp_y, temp_coords[1], temp_coords[0])
        if new_temp_dist < temp_dist:
            # print("Found a better coord", temp_coords)
            x = temp_coords[1]
            y = temp_coords[0]
            temp_dist = new_temp_dist
        
    return x, y


def check_if_no_obs_bw_nodes(node_1, node_2, grid):
        
    # print(node_1, node_2)
    temp_coord_1 = stateNameToCoords(node_1, Config.EDGE_COST)
    temp_coord_2 = stateNameToCoords(node_2, Config.EDGE_COST)

    if temp_coord_1[1] == temp_coord_2[1]:
        width_min = temp_coord_1[1] - 5
        width_max = temp_coord_2[1] + 5
    else:
        width_min = min(temp_coord_1[1], temp_coord_2[1])
        width_max = max(temp_coord_1[1], temp_coord_2[1])

    if temp_coord_1[0] == temp_coord_2[0]:
        len_min = temp_coord_1[0] - 5
        len_max = temp_coord_2[0] + 5
    else:
        len_min = min(temp_coord_1[0], temp_coord_2[0])
        len_max = max(temp_coord_1[0], temp_coord_2[0])

    temp_grid = copy.copy(grid)

    roi = copy.copy(temp_grid[len_min:len_max, width_min:width_max])
    temp_points = np.where(np.all(roi == [0, 0, 0], axis=-1))

    if len(temp_points[0])>0 or len(temp_points[1])>0:
            # print("Obstacle")
        return False
    else:
            # print("Path Clear")
        return True