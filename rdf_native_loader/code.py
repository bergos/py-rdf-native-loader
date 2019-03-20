from rdflib import BNode, Literal, URIRef
from importlib.machinery import SourceFileLoader
import re

file_url_parser = re.compile('file:([^#]*)#(.*)')


class CodeLoader:
    def literal_loader(term):
        return eval(str(term))

    def node_loader(term, graph):
        for (_, _, link) in graph.triples((term, URIRef('https://code.described.at/link'), None)):
            parsed = file_url_parser.match(str(link))

            if parsed is None:
                raise Exception('URL not supported: ' + str(link))

            filename = parsed.group(1)
            property = parsed.group(2)

            return getattr(SourceFileLoader('', filename).load_module(), property)

        return None

    def loader(term, graph, context, variables, basePath, loader_registry):
        if isinstance(term, Literal):
            return CodeLoader.literal_loader(term)

        if isinstance(term, URIRef) or isinstance(term, BNode):
            return CodeLoader.node_loader(term, graph)

        return None

    def register(loader_registry):
        loader_registry.register_literal_loader('https://code.described.at/Python', CodeLoader.loader)
        loader_registry.register_node_loader('https://code.described.at/Python', CodeLoader.loader)
