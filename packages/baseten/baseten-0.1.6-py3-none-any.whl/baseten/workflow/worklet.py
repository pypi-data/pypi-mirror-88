import itertools
from typing import List

from baseten.workflow.atom import Atom, RegisteredAtom


def _tree_copy(tree_root, needle):
    """Perform deep copy, return new root and node corresponding to 'needle' if found."""
    new_tree_root = _Node(tree_root.atom)
    needle_counterpart = None

    if tree_root == needle:
        needle_counterpart = new_tree_root

    for c in tree_root.children:
        child_copy, child_needle_counterpart = _tree_copy(c, needle)
        new_tree_root.add_child(child_copy)
        needle_counterpart = needle_counterpart or child_needle_counterpart
    return new_tree_root, needle_counterpart


class _Node:
    """_Node is unit of graph that tracks atom flow.

    Used by Worklet internally, shouldn't be used outside.
    """

    counter = itertools.count()

    def __init__(self, atom: Atom):
        """Constructor for _Node"""
        self._children = []
        self._atom = atom
        # TODO(pankaj): This is temporary, node doen't need unique id,
        # created here for ease during publication. Should be generated
        # during publish.
        self._id = next(_Node.counter)

    @property
    def id(self):
        return self._id

    @property
    def children(self):
        return self._children

    @property
    def atom(self):
        return self._atom

    def shallow_copy(self):
        """Children are not copied deep, just references. Id is not copied and is freshly created."""
        new_node = _Node(self.atom)
        new_node._children = self._children.copy()
        return new_node

    def add_child(self, node):
        """Mutation, expected to be called only from inside Worklet."""
        self._children.append(node)
        return self


def wrap(atom):
    """Wrap an atom into a worklet. This is the primary way of creating worklets."""
    return Worklet(_Node(atom))


def wrap_with_name(atom, name):
    """Wrap an atom into a worklet, also specifying name."""
    return Worklet(_Node(atom), name)


class Worklet:
    """
    Worklet is a named rooted graph of work nodes

    Two nodes in the graph are special for Worklet, root and last.
    Worklet has only one entry point, the root node but it can have
    many leaf nodes each of which creates a separate output. Of these
    the last node is considered special, it is where any additional
    nodes get added, using e.g. the then method. Output of last node
    is considered the output of worklet.
    """

    def __init__(self, root: _Node, name: str = None, last: _Node = None):
        """
        Worklet is expected to be created mostly via wrapping atom so
        reference to _Node is ok here.
        """
        self._name = name
        self._root = root
        self._last = last
        if not last:
            self._last = root

    @property
    def root(self):
        return self._root

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def last(self):
        return self._last

    def deep_copy(self):
        new_root, new_worklet_last = _tree_copy(self._root, self._last)
        return Worklet(root=new_root, name=self._name, last=new_worklet_last)

    def then(self, worklet):
        new_worklet = self.deep_copy()
        if isinstance(worklet, list):
            for item in worklet:
                if isinstance(item, Atom):
                    new_worklet._last.add_child(_Node(item))
                elif isinstance(item, Worklet):
                    new_worklet._last.add_child(item.root)
                else:
                    raise ValueError(f'Unexpected type for list element in then: {type(item)}')
            new_worklet._last = new_worklet._last.children[0]

        elif isinstance(worklet, Atom):
            node = _Node(worklet)
            new_worklet._last.add_child(node)
            new_worklet._last = node

        elif isinstance(worklet, Worklet):
            new_worklet._last.add_child(worklet.root)
            new_worklet._last = worklet.last
        else:
            raise ValueError(f'Unexpected type for then: {type(worklet)}')

        return new_worklet

    def __rshift__(self, other):
        return self.then(other)

    def to_json(self):
        if not self._name:
            raise ValueError('A worklet should have a name')
        if not self._root:
            raise ValueError('A worklet should have work to do')

        # TODO(pankaj) node ids should be generated via topological sorting
        # this will be better because it will generate more stable ids, which
        # may be good for debugging/logging purposes.
        nodes = [_node_payload(node) for node in _all_nodes(self._root)]

        return {
            'name': self._name,
            'entry_point': self._root.id,
            'nodes': nodes,
            'exit_point': self._last.id,
        }


def _all_nodes(root: _Node) -> List[_Node]:
    nodes = []

    def accumulate_nodes(node):
        nodes.append(node)
    _walk_graph(root, accumulate_nodes, set())
    return nodes


def _walk_graph(node: _Node, func, seen):
    """Execute func on each node of graph, breaks cycles."""
    if not node:
        return

    if node in seen:
        return
    seen.add(node)

    func(node)

    for child in node.children:
        _walk_graph(child, func, seen)


def _node_payload(node: _Node):
    atom = node.atom
    if isinstance(atom, RegisteredAtom):
        return {
            'id': node.id,
            'children': [n.id for n in node.children],
            'node_name': atom.node_name,
            'atom': {
                'name': atom.name,
                'conf': atom.conf,
            },
        }

    raise ValueError('Unsupported Atom type.')
