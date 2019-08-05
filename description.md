### Amazing Co Solution Description

The requirement presents a tree-like data model where each office of Amazing Co is a node that has one or more descendant nodes. This is a hierarchical model with each node having only a single parent with only a single root node at the top of the hierarchy.

Typically object graphs such as this tree are not efficient to store in a relational database because each relation requires an expensive JOIN on tables (or JOIN against the same table) and retrieving a complete list of descendants would require repeated querying (or joining) the tables for children at lower and lower depths.

The tree could be stored however in a queue-like storage that could be persisted in a table providing that the nodes are always stored using a predetermined sequence in the table (depth first order).

In order to make the persistence efficient, I annotated each office node with two additional integers:
* node_pos - the position of the node in the "queue". Having this field indexed allows fast access to the nodes based on their position in the "queue".
* desc_count - the total count of all descendants under this node. This field is kept up to date as the tree undergoes changes and would always indicate the count of entries in the queue for descendants after the current element.
Setting up an index that covers node_pos and desc_count together allows for rapid updates of the queue-structure when changes are being made in the hierarchy.

Using the above two fields all required API calls can be implemented with queries against the backend that do not need to perform depth-based scan of the tree data and run as a few single statements (SELECT/UPDATE) using indexed fields.

The "models.py" defines this model that gets persisted by the framework in the backend used (SQLite in this current implementation). It also includes the necessary logic that allows the building and changing of the tree while maintaining the above indexed fields.

A REST API is built around this model using Django REST Framework. Serializers are defined in api_serializers.py and the access points are created in api_views.py. The API's URLs are wired into the app's urls through the urls.py file.

Django REST Framework automatically generates an HTML browsable version of the API for discovery purposes. This can be accessed at "/branches/v1/".

### User Interface

A basic front-end UI is created using components from Kendo UI framework that only consume the defined API viewpoints and display the results in a tree list and a list view.

The tree list provides a hierarchical view of all the nodes. Buttons are provided for adding nodes and deleting nodes. The "name" field ca be edited within the cell. Drag and drop option is available on the first column cell of each node, which in turn will trigger the change of parent in the backend.

Any changes made need to be saved using the Save Changes button, they aren't immediately committed.

The front end UI can be accessed through "/branches".

The project can be pulled as a docker image from here:

**docker pull pgalfi/assignments:AmazingCo**

Please run it with -p 80:80 to expose the http port that the app will listen to.