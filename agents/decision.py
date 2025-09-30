class DecisionAgent:
    def __init__(self, llm):
        self.llm = llm

    def __call__(self, state):
        # Format the analyses for better readability
        analyses_text = ""
        for i, analysis in enumerate(state['analyses']):
            analyses_text += f"\nOption {i+1}: {analysis['option']}\n"
            analyses_text += f"Analysis: {analysis['analysis']}\n"
            analyses_text += "-" * 50 + "\n"
        
        prompt = (
            f"Based on the following analyses, recommend the best option and explain why:\n"
            f"{analyses_text}\n"
            f"Please provide a clear recommendation with reasoning."
        )
        
        try:
            recommendation = self.llm.generate(prompt)
            state['recommendation'] = recommendation
        except Exception as e:
            state['recommendation'] = f"Error generating recommendation: {str(e)}"
        
        return state
