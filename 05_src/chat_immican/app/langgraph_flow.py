# app/langgraph_flow.py
# PSEUDO: show how to register a simple LangGraph flow that does:
# semantic retrieval -> rewrite (LLM) -> optional function call
from langgraph import Graph, Task  # adjust import per your LangGraph SDK

def build_simple_flow(semantic_service, llm_client=None):
    graph = Graph(name="qa_rewrite_flow")
    # Node: semantic retrieval
    def retrieve(inputs):
        q = inputs["question"]
        hits = semantic_service.query(q, k=3)
        return {"hits": hits}
    graph.add_task(Task(func=retrieve, name="retrieve"))

    # Node: rewrite using LLM or deterministic function
    def rewrite(inputs):
        hits = inputs["retrieve"]["hits"]
        text = hits[0]["metadata"]["content"]
        # If llm_client provided, call it to rewrite (omitted here)
        # fallback deterministic rephrase:
        return {"answer": text.split(".")[0] + "."}
    graph.add_task(Task(func=rewrite, name="rewrite", upstream=["retrieve"]))
    return graph
