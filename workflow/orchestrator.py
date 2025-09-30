from langgraph.graph import StateGraph, END

def build_workflow(option_finder, pros_cons, decision):
    wf = StateGraph(dict)
    wf.add_node("find_options", option_finder)
    wf.add_node("pros_cons", pros_cons)
    wf.add_node("decision", decision)
    
    wf.add_edge("find_options", "pros_cons")
    wf.add_edge("pros_cons", "decision")
    wf.add_edge("decision", END)
    
    wf.set_entry_point("find_options")
    return wf.compile()
