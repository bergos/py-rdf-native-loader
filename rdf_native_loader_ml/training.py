from rdflib import URIRef


class Training:
    def __init__(self, training_dataset, validation_dataset, batch_size, epochs):
        self.training_dataset = training_dataset
        self.validation_dataset = validation_dataset
        self.batch_size = batch_size
        self.epochs = epochs


class TrainingLoader:
    def loader(term, graph, context, variables, basePath, loader_registry):
        training_dataset = None
        validation_dataset = None
        batch_size = None
        epochs = None

        for _, _, training_dataset_term in graph.triples((term, URIRef('https://ns.bergnet.org/machine-learning/trainingDataset'), None)):
            training_dataset = training_dataset_term
        for _, _, validation_dataset_term in graph.triples((term, URIRef('https://ns.bergnet.org/machine-learning/validationDataset'), None)):
            validation_dataset = validation_dataset_term
        for _, _, batch_size_term in graph.triples((term, URIRef('https://ns.bergnet.org/machine-learning/batchSize'), None)):
            batch_size = int(batch_size_term)
        for _, _, epochs_term in graph.triples((term, URIRef('https://ns.bergnet.org/machine-learning/epochs'), None)):
            epochs = int(epochs_term)

        return Training(
            training_dataset=training_dataset,
            validation_dataset=validation_dataset,
            batch_size=batch_size,
            epochs=epochs)

    def register(loader_registry):
        loader_registry.register_node_loader('https://ns.bergnet.org/machine-learning/Training', TrainingLoader.loader)
