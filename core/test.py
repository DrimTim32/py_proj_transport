from dataStructures import *
nodes = []
for letter in "ABCDEF":
    nodes.append(Node(letter))

graph = Graph(nodes)
graph.connect_both("A", "B", 1)
graph.connect_both("A", "E", 1)
graph.connect_both("E", "F", 1)
graph.connect_both("B", "F", 5)
graph.connect_both("B", "C", 2)
graph.connect_both("D", "C", 1)
print(graph)