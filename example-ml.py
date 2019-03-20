from rdflib import URIRef
from rdf_native_loader import LoaderRegistry
from rdf_native_loader_ml import ProjectLoader, TrainingLoader
from utils import graph_from_file


registry = LoaderRegistry()
ProjectLoader.register(registry)

# just skip the next line for already trained models
TrainingLoader.register(registry)

graph = graph_from_file('ml.ttl')
project = registry.load(URIRef('http://example.org/project'), graph)

project.fit()

print('let\'s do a prediction: ' + str(project.predict(['5', '5'])))
