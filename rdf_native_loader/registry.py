from rdflib import BNode, Literal, RDF, URIRef

class LoaderRegistry:
    def __init__(self):
        self.literal_loaders = {}
        self.node_loaders = {}

    def register_literal_loader(self, type, loader):
        self.literal_loaders[str(type)] = loader

    def register_node_loader(self, type, loader):
        self.node_loaders[str(type)] = loader

    def load(self, term, graph, context=None, variables=None, basePath=None):
        loader = None

        if isinstance(term, Literal):
            type_str = str(term.datatype)

            if type_str in self.literal_loaders:
                loader = self.literal_loaders[type_str]

        if isinstance(term, URIRef) or isinstance(term, BNode):
            for _, _, type in graph.triples((term, RDF.type, None)):
                if str(type) in self.node_loaders:
                    loader = self.node_loaders[str(type)]

        if loader is not None:
            return loader(term, graph, context, variables, basePath, self)

        return None
