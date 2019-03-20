import json
import re

file_url_parser = re.compile('file:([^#]*)')


def mapping_from_json_file(mapping_file):
    parsed = file_url_parser.match(str(mapping_file))

    if parsed is None:
        raise Exception('URL not supported: ' + str(mapping_file))

    filename = parsed.group(1)

    return json.load(open(filename))

#
# from graph to numpy for training and predictions
#
# e.g. for a classification project this could resolve & load images from URLs in the dataset and map them into a numpy array
#
def input_mapper(mapping_file):
    mapping = mapping_from_json_file(mapping_file)

    def f(row):
        data = []

        for column in mapping['input']:
            data.append(int(row[column], 16))

        return data

    return f


#
# from numpy to graph for predictions
#
# e.g. for a classification project this could map the indexes and values to triples with rdf:Class IRIs and nice scoring result structure
#
def output_mapper(mapping_file):
    mapping = mapping_from_json_file(mapping_file)

    def f(row):
        return str(row)

    return f


#
# from graph to numpy for training
#
# e.g. for a classification project this could map the rdf:Class IRI to a numpy array
#
def output_reverse_mapper(mapping_file):
    mapping = mapping_from_json_file(mapping_file)

    def f(row):
        data = []

        for column in mapping['output']:
            data.append(int(row[column], 16))

        return data

    return f
