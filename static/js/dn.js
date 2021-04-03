"use strict";

function DynamicNetwork(serialized) {

    var VERSION = "ver 0.0.1"

    var AUTHOR = "Yichen Wang"

    function Graph(directed) {
        this.edges = {};
        this.directed = directed;
    }
    Graph.prototype = {
        _pick_random: function (array) {
            if (array.length) {
                let e = array.pop();
                array.push(e);
                return e
            }
        },
        _addVertex: function (node) {
            this.edges[node] = this._adjacent(node)
        },
        _adjacent: function (node) {
            return this.edges[node] || []
        },
        addEdge: function (u, v) {
            u = String(u)
            v = String(v)
            this._addVertex(u);
            this._addVertex(v);
            this._adjacent(u).push(v)
            if (!this.directed) { this._adjacent(v).push(u) }
        },
        nrOfVertices: function () {
            return Object.keys(this.edges).length
        },
        nrOfEdges: function () {
            let output = 0
            Object.entries(this.edges).forEach(([k, v]) => output += v.length / (2 - this.directed));
            return output
        },
        maximalCliques: function (reporter, clique = [], candidates = Object.keys(this.edges), excluded = []) {
            if (!candidates.length && !excluded.length) {
                reporter.push(clique);
                return
            }
            let pivot = this._pick_random(candidates) || this._pick_random(excluded);
            (candidates.filter(x => !this.edges[pivot].includes(x))).forEach(v => {
                let newCandidates = candidates.filter(x => this.edges[v].includes(x));
                let newExcluded = excluded.filter(x => this.edges[v].includes(x));
                let newClique = [...clique, v];
                this.maximalCliques(reporter, newClique, newCandidates, newExcluded);
                candidates = candidates.filter(x => x !== v);
                excluded.push(v);
            });
        },
        maximumClique: function () {
            let reporter = [];
            this.maximalCliques(reporter);
            let output = 0
            reporter.forEach(a => {
                output = a.length > output ? a.length : output;
            })
            return output;
        }

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
        relationships[edge.t].addEdge(edge.i, edge.j);
    }

    let addRelationships = (edges, directed = false) => edges.forEach(e => _addRelationship(e, directed));

    let getTimeline = () => { return Object.keys(relationships); }

    let getListNrOfVertices = () => {
        let output = [];
        Object.entries(relationships).forEach(([k, v]) => output.push(v.nrOfVertices()));
        return output;
    }

    let getListNrOfEdges = () => {
        let output = [];
        Object.entries(relationships).forEach(([k, v]) => output.push(v.nrOfEdges()));
        return output;
    }

    let getListMaximumClique = () => {
        let output = [];
        Object.entries(relationships).forEach(([k, v]) => output.push(v.maximumClique()));
        return output;
    }


    return {
        version: VERSION,
        author: AUTHOR,
        nodes: nodes,
        relationships: relationships,
        addNodes: addNodes,
        addRelationships: addRelationships,
        getTimeline: getTimeline,
        getListNrOfVertices: getListNrOfVertices,
        getListNrOfEdges: getListNrOfEdges,
        getListMaximumClique: getListMaximumClique
    };
}


