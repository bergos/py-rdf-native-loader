from rdf_native_loader import CodeLoader, ImplementationLoader, LoaderRegistry
from rdflib import URIRef
from utils import graph_from_file

registry = LoaderRegistry()
CodeLoader.register(registry)
registry.register_node_loader('http://example.org/Factory', ImplementationLoader.loader)

graph = graph_from_file('example.ttl')
func = registry.load(URIRef('http://example.org/function'), graph)
func()
funcLiteral = registry.load(URIRef('http://example.org/literalFunction'), graph)
funcLiteral()
