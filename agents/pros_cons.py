class ProsConsAgent:
    def __init__(self, llm):
        self.llm = llm

    def __call__(self, state):
        analyses = []
        for i, option in enumerate(state['candidates']):
            prompt = (
                f"Analyze the following option and provide pros and cons:\n"
                f"Option {i+1}: {option.page_content}\n"
                f"Please provide a structured analysis with clear pros and cons."
            )
            try:
                result = self.llm.generate(prompt)
                analyses.append({
                    'option': option.page_content,
                    'analysis': result
                })
            except Exception as e:
                analyses.append({
                    'option': option.page_content,
                    'analysis': f"Error analyzing option: {str(e)}"
                })
        state['analyses'] = analyses
        return state
