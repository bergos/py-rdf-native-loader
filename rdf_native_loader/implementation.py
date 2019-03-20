from rdflib import URIRef
from rdflib.collection import Collection


class ImplementationLoader:
    def loader(term, graph, context, variables, basePath, loader_registry):
        args = None

        for _, _, args_term in graph.triples((term, URIRef('https://code.described.at/arguments'), None)):
            args = list(Collection(graph, args_term))

        for _, _, code in graph.triples((term, URIRef('https://code.described.at/implementedBy'), None)):
            result = loader_registry.load(code, graph, context, variables, basePath)

            if result is not None:
                if args is not None:
                    return result(*args)
                else:
                    return result()

        return None

