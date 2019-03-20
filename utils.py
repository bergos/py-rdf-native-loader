from rdflib import Graph


def graph_from_file (filename):
    graph = Graph()

    graph.parse(filename, format='text/turtle')

    return graph
