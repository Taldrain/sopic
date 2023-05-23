from collections import deque
import graphviz


def list_childs(childs):
    if type(childs) is list:
        return childs
    return list(childs.values())

def list_childs_items(childs):
    if type(childs) is list:
        return ((i, i) for i in childs)
    return list(childs.items())


def list_steps(graph):
    steps = set()
    for key, value in graph.items():
        steps.add(key)
        steps.update(list_childs(value[1]))
    return steps


def find_indegree(graph):
    steps = list_steps(graph)
    indegree = {step: 0 for step in steps}

    for neighbors in [list_childs(i[1]) for i in graph.values()]:
        for neighbor in neighbors:
            indegree[neighbor] += 1

    return indegree


def is_valid_dag(graph):
    res = []
    q = deque()
    indegree = find_indegree(graph)
    for node in indegree:
        if indegree[node] == 0:
            q.append(node)
    while len(q) > 0:
        node = q.popleft()
        res.append(node)

        if node in graph:
            for neighbor in list_childs(graph[node][1]):
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    q.append(neighbor)

    return len(indegree) == len(res)


def graph_to_dot(graph, start_step, station_name):
    dot = graphviz.Digraph(format='png')

    steps = list_steps(graph)
    for step in steps:
        if step in graph:
            for label, neighbor in list_childs_items(graph[step][1]):
                dot.edge(step, neighbor, label=label)
            if graph[step][0].MAX_RETRIES > 0:
                dot.edge(
                    step,
                    step,
                    label=str(graph[step][0].MAX_RETRIES),
                    style="dashed",
                )
    dot.node(start_step, style="filled", fillcolor="green")

    dot.render(f"dag-{station_name}", cleanup=True)
