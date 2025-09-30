class OptionFinderAgent:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def __call__(self, state):
        query = state['query']
        results = self.vector_store.similarity_search(query, k=5)
        state['candidates'] = results
        return state
