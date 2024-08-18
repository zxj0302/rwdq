**Description**:

This tool is used to extract specific graphs in a database(must have the same columns and attributes with ours).

**Motivation**:

In GNN dataset like OGB and TUDataset, we can directly use the dataset e.g. MUTAG, Cora, etc. However, in some cases, we need to extract specific graphs from a database to support specific tasks or experiments or do some stress tests. Take the GNN based subgraph counting for example, there is a method that cannot support very dense graphs or graphs has some dense and star-shaped part, so we need to filter the graphs to get proper ones. This tool is designed for this purpose.

**Usage**:

* python main.py --config my_config.json --database my_database.db
* data_objects = run_query('config.json', 'rwd.db')

The configuration file should be a JSON file specifying the query parameters.

**License**:

This project is licensed under the MIT License - see the LICENSE file for details.
