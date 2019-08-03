### Amazing Company Requirements

We in Amazing Co need to model how our company is structured so we can do
awesome stuff.

We have a root node (only one) and several children nodes, each one with its
own children as well. It’s a tree-based structure.

Something like:

```
    root
   /    \
  a      b
```
We need two HTTP APIs that will serve the two basic operations:

1) Get all children nodes (all descendants) of a given node (the given node can be anyone in the tree structure).

2) Change the parent node of a given node (the given node can be anyone in
the tree structure).

They need to answer quickly, even with tons of nodes. Also,we can’t afford
to lose this information, so some sort of persistence is required.

Each node should have the following info:

1) node identification

2) who is the parent node

3) who is the root node

4) the height of the node. In the above example, height(root) == 0 and
height(a) == 1.

If it is possible for you to make a simple UI for this challenge, that
would be great. If you feel adventurous you can use our UI components (http://ui.tradeshift.com )
