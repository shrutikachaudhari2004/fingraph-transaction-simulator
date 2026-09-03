import networkx as nx

# Create directed graph
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

print("\n===== PageRank =====")

for account, score in sorted(
    pagerank.items(),
    key=lambda x: x[1],
    reverse=True
):
    print(account, ":", round(score, 4))


# -------------------------
# Louvain Community Detection
# -------------------------

print("\n===== Louvain Communities =====")

communities = nx.community.louvain_communities(
    G.to_undirected()
)

for community_id, community in enumerate(communities):
    print(
        "Community",
        community_id,
        ":",
        list(community)
    )