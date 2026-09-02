import networkx as nx

# Create graph
G = nx.DiGraph()

# Sample transaction relationships
G.add_edge("ACC001", "ACC002")
G.add_edge("ACC002", "ACC003")
G.add_edge("ACC003", "ACC001")
G.add_edge("ACC001", "ACC004")
G.add_edge("ACC004", "ACC005")

# -------------------------
# PageRank
# -------------------------

pagerank = nx.pagerank(G)

print("=== PageRank ===")

for account, score in sorted(
    pagerank.items(),
    key=lambda x: x[1],
    reverse=True
):
    print(account, ":", round(score, 4))


# -------------------------
# Community Detection
# -------------------------

print("\n=== Community Detection ===")

undirected_graph = G.to_undirected()

communities = nx.community.louvain_communities(
    undirected_graph,
    seed=42
)

for community_id, community in enumerate(communities):