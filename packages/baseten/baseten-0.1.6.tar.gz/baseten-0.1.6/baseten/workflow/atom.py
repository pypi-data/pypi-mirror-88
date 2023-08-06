from typing import Dict


class Atom:
    """Atom is a reusable action.

    This class is a marker node and also performs basic dsl functions.
    """

    def then(self, other):
        from baseten.workflow.worklet import wrap
        return wrap(self).then(other)

    def __rshift__(self, other):
        return self.then(other)

    @property
    def node_name(self):
        raise NotImplementedError('Derived classes should override.')


class RegisteredAtom(Atom):
    """RegisteredAtom is a registered reusable action."""

    def __init__(self, name: str, node_name: str = '', conf=None):
        self._conf = conf or {}
        self._name = name
        self._node_name = node_name

    @property
    def conf(self) -> Dict:
        return self._conf

    @property
    def name(self) -> str:
        return self._name

    @property
    def node_name(self):
        return self._node_name
