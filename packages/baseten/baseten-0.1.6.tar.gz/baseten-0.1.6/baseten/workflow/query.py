class Query:
    def __init__(self, name: str, query_str: str, external_connection: str = None):
        self._name = name
        self._query_str = query_str
        self._external_connection = external_connection

    def to_json(self):
        return {
            'name': self._name,
            'query_str': self._query_str,
            'external_connection': self._external_connection,
        }
