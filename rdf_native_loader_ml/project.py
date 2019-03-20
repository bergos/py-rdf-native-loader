import csv
from rdf_native_loader import CodeLoader, ImplementationLoader, LoaderRegistry
from rdflib import URIRef


class Project:
    def __init__(self, model, interface, training=None):
        self.model = model
        self.interface = interface
        self.training = training

    def fit(self):
        # this should actually read the datasets from the URLs defined in training of the TTL file

        # just for the demo we read the dataset.csv file
        training_data = []
        validation_data = []

        with open('dataset.csv') as csv_file:
            dialect = csv.Sniffer().sniff(csv_file.read(1024))
            csv_file.seek(0)
            dataset_reader = csv.reader(csv_file, dialect)
            rownum = 0

            for row in dataset_reader:
                if rownum > 0 and rownum < 6:
                    training_data.append(row)
                if rownum >= 6:
                    validation_data.append(row)

                rownum += 1

            # also here the actual training function of the ML framework should be called
            for epoch in range(0, self.training.epochs):
                print('epoch: ' + str(epoch))

                for data in training_data:
                    input = self.interface.input_mapping(data)
                    target = self.interface.output_reverse_mapping(data)

                    print('  train batch...')
                    print('    input: ' + str(input))
                    print('    target: ' + str(target))

            return None

    def predict(self, input):
        input = self.interface.input_mapping(input)

        # the ML framework magic for predictions should do it's work here

        return self.interface.output_mapping(int(input[0]) + int(input[1]))


class ProjectInterface:
    def __init__(self, input_mapping, output_mapping, output_reverse_mapping):
        self.input_mapping = input_mapping
        self.output_mapping = output_mapping
        self.output_reverse_mapping = output_reverse_mapping


class ProjectLoader:
    def loader(term, graph, context, variables, basePath, loader_registry):
        model = None
        input_mapping = None
        output_mapping = None
        output_reverse_mapping = None
        training = None

        for _, _, model_term in graph.triples((term, URIRef('https://ns.bergnet.org/machine-learning/model'), None)):
            model = ImplementationLoader.loader(model_term, graph, context, variables, basePath, loader_registry)

        for _, _, interface_term in graph.triples((term, URIRef('https://ns.bergnet.org/machine-learning/interface'), None)):
            for _, _, input_mapper_term in graph.triples((interface_term, URIRef('https://ns.bergnet.org/machine-learning/inputMapper'), None)):
                input_mapping = ImplementationLoader.loader(input_mapper_term, graph, context, variables, basePath, loader_registry)
            for _, _, output_mapper_term in graph.triples((interface_term, URIRef('https://ns.bergnet.org/machine-learning/outputMapper'), None)):
                output_mapping = ImplementationLoader.loader(output_mapper_term, graph, context, variables, basePath, loader_registry)
            for _, _, output_reverse_mapper_term in graph.triples((interface_term, URIRef('https://ns.bergnet.org/machine-learning/outputReverseMapper'), None)):
                output_reverse_mapping = ImplementationLoader.loader(output_reverse_mapper_term, graph, context, variables, basePath, loader_registry)

        for _, _, training_term in graph.triples((term, URIRef('https://ns.bergnet.org/machine-learning/training'), None)):
            training = loader_registry.load(training_term, graph, context, variables, basePath)

        interface = ProjectInterface(
            input_mapping=input_mapping,
            output_mapping=output_mapping,
            output_reverse_mapping=output_reverse_mapping)

        return Project(
            model=model,
            interface=interface,
            training=training)

    def register(loader_registry):
        CodeLoader.register(loader_registry)
        loader_registry.register_node_loader('https://ns.bergnet.org/machine-learning/Project', ProjectLoader.loader)
