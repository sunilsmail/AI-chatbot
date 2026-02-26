from typing import TypedDict
from redis.asyncio import Redis
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from app.core.settings import settings

class State(TypedDict):
    message: str
    session_id: int
    user_id: int
    intent: str
    entities: dict
    response: str

llm = ChatOpenAI(model='gpt-4o-mini', api_key=settings.openai_api_key, temperature=0)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
async def classify_intent(text: str):
    prompt = f"Classify intent JSON only for: {text}"
    out = await llm.ainvoke(prompt)
    content = out.content if isinstance(out.content, str) else str(out.content)
    intent='product_policy_query'
    for item in ['track_order','cancel_product','update_delivery_date','product_policy_query','refund_status','escalate_to_human']:
        if item in content: intent=item
    return {'intent': intent, 'confidence': 0.9, 'entities': {}}

async def intent_node(state: State):
    c = await classify_intent(state['message'])
    state['intent']=c['intent']; state['entities']=c['entities']
    return state

async def memory_node(state: State):
    r=Redis.from_url(settings.redis_url)
    await r.rpush(f"session:{state['session_id']}", state['message'])
    await r.expire(f"session:{state['session_id']}", 86400)
    await r.aclose(); return state

async def order_node(state: State):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://order-service:8002/orders/1")
    state['response']=f"Order service says: {resp.text}"
    return state

async def policy_node(state: State):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://policy-service:8003/policies/product/1")
    state['response']=f"Policy details: {resp.text}"
    return state

async def escalate_node(state: State):
    state['response']='I am escalating this conversation to a human support agent.'
    return state

async def route(state: State):
    if state['intent'] in {'track_order','cancel_product','update_delivery_date'}: return 'order'
    if state['intent'] in {'product_policy_query','refund_status'}: return 'policy'
    return 'escalate'

graph = StateGraph(State)
graph.add_node('intent', intent_node)
graph.add_node('memory', memory_node)
graph.add_node('order', order_node)
graph.add_node('policy', policy_node)
graph.add_node('escalate', escalate_node)
graph.set_entry_point('intent')
graph.add_edge('intent','memory')
graph.add_conditional_edges('memory', route, {'order':'order','policy':'policy','escalate':'escalate'})
graph.add_edge('order', END)
graph.add_edge('policy', END)
graph.add_edge('escalate', END)
chat_graph = graph.compile()

async def run_chat_workflow(user_id:int, session_id:int, message:str):
    out = await chat_graph.ainvoke({'user_id': user_id, 'session_id': session_id, 'message': message, 'intent':'', 'entities': {}, 'response': ''})
    return {'intent': out['intent'], 'response': out['response'], 'entities': out['entities']}
