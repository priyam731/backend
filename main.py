from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from collections import defaultdict, deque

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://flowcraft-zeta.vercel.app/"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PipelineRequest(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]


class PipelineResponse(BaseModel):
    num_nodes: int
    num_edges: int
    is_dag: bool


def is_dag(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> bool:
    """
    Check if the graph represented by nodes and edges is a Directed Acyclic Graph (DAG).
    Uses Kahn's algorithm (topological sort with in-degree tracking).
    """
    if not nodes:
        return True  # Empty graph is a DAG
    

    node_ids = {node['id'] for node in nodes}
    adj_list = defaultdict(list)
    in_degree = defaultdict(int)
    
    # Initialize in-degree for all nodes
    for node_id in node_ids:
        in_degree[node_id] = 0
    
    # Process edges
    for edge in edges:
        source = edge.get('source')
        target = edge.get('target')
        
        # Only process edges that connect existing nodes
        if source in node_ids and target in node_ids:
            adj_list[source].append(target)
            in_degree[target] += 1
    

    queue = deque([node_id for node_id in node_ids if in_degree[node_id] == 0])
    visited_count = 0
    
    while queue:
        current = queue.popleft()
        visited_count += 1
        
        for neighbor in adj_list[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    

    return visited_count == len(node_ids)


@app.get('/')
def read_root():
    return {'Ping': 'Pong'}


@app.post('/pipelines/parse')
def parse_pipeline(pipeline: PipelineRequest) -> PipelineResponse:
    """
    Parse the pipeline and return statistics about it.
    
    Returns:
        - num_nodes: Number of nodes in the pipeline
        - num_edges: Number of edges in the pipeline
        - is_dag: Whether the pipeline forms a valid DAG
    """
    nodes = pipeline.nodes
    edges = pipeline.edges
    
    num_nodes = len(nodes)
    num_edges = len(edges)
    is_dag_result = is_dag(nodes, edges)
    
    return PipelineResponse(
        num_nodes=num_nodes,
        num_edges=num_edges,
        is_dag=is_dag_result
    )
