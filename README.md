# rdf-native-loader

The RDF Native Loader provides a registry and loaders to convert RDF data to native Python objects/code.
It also include a loader for the [Code Ontology](https://code.described.at/) to load Python code from file URLs or lambda functions from literals. 

The `example.py` code shows how code is loaded from factory methods from a file URL and a literal.

# rdf-native-loader-ml

The RDF Native Loader for Machine Learning is a small demo, which is not yet connected to a ML framework.
The `example-ml.py` file shows how a ML project is loaded from an RDF description in `ml.ttl`.
As this is just a demo, there are comments in the code, which describe the logic the final code would implement.

## Model

A code loader is used to load the factory method which generates the model object.
In the demo, the model is just a dummy.
In the final version, the model would be an instance of the ML framework model (e.g. Keras Model).
`code:Python` can be used to create the model via Python code.
An alternative could be `code:Onnx` to load the model from a standard Onnx file.

## Interface

The interface provides mappings to convert input RDF data to NumPy arrays for the model and also from NumPy arrays from the model to the output RDF data.
There is also a reverse output mapping, which maps the RDF output data from the training data, to the target NumPy arrays.
Besides directly mapping the values, the mapping could be also used to load images from URLs or translate classification results into more readable structures with scoring and IRIs to the classes.

## Training

The properties `ml:trainingDataset` and `ml:validationDataset` point to containers, with link to all input and output data.
Each link should contain one entry of input and output data.
The input mapping and output reverse mapping code takes care of mapping the data entry into input and output NumPy objects.
The demo only contains mock code and reads the data not from a RDF source, but from a static CSV file.
But the basic structure, calling the mapping functions, is already there.   