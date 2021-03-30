"use strict";
function DynamicNetwork(serialized) {

    function Graph(directed) {
        this.edges = {};
        this.directed = directed;
    }
    Graph.prototype = {
        _addVertex: function (node) {
            this.edges[node] = this._adjacent(node)
        },
        _adjacent: function (node) {
            return this.edges[node] || []
        },
        _addEdge: function (u, v) {
            this._addVertex(u);
            this._addVertex(v);
            this._adjacent(u).push(v)
            if (!this.directed) { this._adjacent(v).push(u) }
        },
        _nrOfVertices: function () { return Object.keys(this.edges).length }
    }



    if (serialized) {
        alert('shit');
    }

    var nodes = {}
    var relationships = {}

    let _addNode = (node) => {
        nodes[node.id] = Object.keys(node).reduce((object, key) => {
            if (key != 'id') { object[key] = node[key] }
            return object
        }, {});
    }

    let addNodes = (nodes) => nodes.forEach(e => _addNode(e));

    let _addRelationship = (edge, directed) => {
        if (!relationships[edge.t]) { relationships[edge.t] = new Graph(directed); }
        relationships[edge.t]._addEdge(edge.i, edge.j);
    }

    let addRelationships = (edges, directed = false) => edges.forEach(e => _addRelationship(e, directed));

    let getTimeline = () => { return Object.keys(relationships) }

    let getListNrOfVertices = () => {
        let output = []
        Object.entries(relationships).forEach(([k, v]) => output.push(v._nrOfVertices()));
        return output
    }


    return {
        nodes: nodes,
        relationships: relationships,
        addNodes: addNodes,
        addRelationships: addRelationships,
        getTimeline: getTimeline,
        getListNrOfVertices:getListNrOfVertices,
    };
}


