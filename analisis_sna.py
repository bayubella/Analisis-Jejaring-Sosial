import urllib.request
import gzip
import networkx as nx
import community as community_louvain
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from pyvis.network import Network
import json
import os

def download_dataset():
    url = "https://snap.stanford.edu/data/facebook_combined.txt.gz"
    local_filename = "facebook_combined.txt.gz"
    if not os.path.exists(local_filename):
        print("Downloading Facebook combined dataset from SNAP...")
        urllib.request.urlretrieve(url, local_filename)
        print("Download completed!")
    else:
        print("Dataset already downloaded.")
    return local_filename

def load_graph(filename):
    print("Loading graph...")
    with gzip.open(filename, "rt") as f:
        G = nx.read_edgelist(f, nodetype=int)
    print(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G

def calculate_centralities(G):
    print("Calculating centrality metrics...")
    
    # 1. Degree Centrality
    deg_cent = nx.degree_centrality(G)
    
    # 2. Betweenness Centrality
    print("  Calculating Betweenness Centrality (this may take ~30-50s)...")
    betweenness_cent = nx.betweenness_centrality(G)
    
    # 3. Closeness Centrality
    print("  Calculating Closeness Centrality (this may take ~10-20s)...")
    closeness_cent = nx.closeness_centrality(G)
    
    # 4. Eigenvector Centrality
    print("  Calculating Eigenvector Centrality...")
    eigenvector_cent = nx.eigenvector_centrality(G, max_iter=1000)
    
    # Compile into a DataFrame
    df_cent = pd.DataFrame(index=G.nodes())
    df_cent["degree"] = [deg_cent[n] for n in df_cent.index]
    df_cent["betweenness"] = [betweenness_cent[n] for n in df_cent.index]
    df_cent["closeness"] = [closeness_cent[n] for n in df_cent.index]
    df_cent["eigenvector"] = [eigenvector_cent[n] for n in df_cent.index]
    
    df_cent.index.name = "node_id"
    df_cent.to_csv("centrality_results.csv")
    print("Centrality scores saved to centrality_results.csv")
    
    return df_cent

def run_si_simulation(G, seed_node, transmission_prob=0.03, num_steps=20, num_trials=50):
    """
    Simulates Susceptible-Infected (SI) model of information propagation.
    Returns average number of infected nodes at each step.
    """
    num_nodes = G.number_of_nodes()
    history = np.zeros((num_trials, num_steps + 1))
    
    for trial in range(num_trials):
        states = {node: 0 for node in G.nodes()} # 0: Susceptible, 1: Infected
        states[seed_node] = 1
        infected = {seed_node}
        history[trial, 0] = 1
        
        for step in range(1, num_steps + 1):
            new_infected = set()
            for u in list(infected):
                for v in G.neighbors(u):
                    if states[v] == 0:
                        if random.random() < transmission_prob:
                            new_infected.add(v)
            for v in new_infected:
                states[v] = 1
                infected.add(v)
            history[trial, step] = len(infected)
            
    return np.mean(history, axis=0)

def simulate_propagation(G, df_cent):
    print("Running SI propagation simulations...")
    
    # Choose seeds
    degree_seed = df_cent["degree"].idxmax()
    betweenness_seed = df_cent["betweenness"].idxmax()
    closeness_seed = df_cent["closeness"].idxmax()
    eigenvector_seed = df_cent["eigenvector"].idxmax()
    
    # Pick a random node with low centrality as baseline
    low_cent_nodes = df_cent[df_cent["degree"] < 0.01].index.tolist()
    random.seed(42)
    random_seed = random.choice(low_cent_nodes)
    
    seeds = {
        "Degree Hub (Node 107)": degree_seed,
        "Betweenness Broker (Node 107)": betweenness_seed,
        "Closeness Hub (Node 107)": closeness_seed,
        "Eigenvector Hub (Node 1912)": eigenvector_seed,
        "Random Node (Node {})".format(random_seed): random_seed
    }
    
    num_steps = 20
    num_trials = 50
    prob = 0.08
    
    results = {}
    for name, seed in seeds.items():
        print(f"  Simulating spread from {name} (ID {seed})...")
        avg_history = run_si_simulation(G, seed, transmission_prob=prob, num_steps=num_steps, num_trials=num_trials)
        results[name] = avg_history
        
    # Plot results
    plt.figure(figsize=(10, 6))
    colors = {
        "Degree Hub (Node 107)": "#1f77b4",
        "Betweenness Broker (Node 107)": "#ff7f0e",
        "Closeness Hub (Node 107)": "#2ca02c",
        "Eigenvector Hub (Node 1912)": "#9467bd",
        "Random Node (Node {})".format(random_seed): "#d62728"
    }
    
    for name, history in results.items():
        pct = (history / G.number_of_nodes()) * 100
        plt.plot(pct, label=name, color=colors.get(name, "gray"), linewidth=2.5)
        
    plt.title("Simulasi Penyebaran Informasi (Model SI) pada Jejaring Facebook SNAP", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Langkah Waktu (Siklus)", fontsize=12)
    plt.ylabel("Persentase Node Terinfeksi (%)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=11, loc='lower right')
    plt.xlim(0, num_steps)
    plt.ylim(0, 105)
    
    plt.axhline(y=50, color='gray', linestyle=':', alpha=0.7)
    plt.text(0.5, 51, "50% Terinfeksi", color='gray', fontsize=9)
    plt.axhline(y=90, color='gray', linestyle=':', alpha=0.7)
    plt.text(0.5, 91, "90% Terinfeksi", color='gray', fontsize=9)
    
    plt.tight_layout()
    plt.savefig("simulation_plot.png", dpi=300)
    plt.close()
    print("Simulation plot saved as simulation_plot.png")
    
    # Save simulation history to CSV
    df_sim = pd.DataFrame(results)
    df_sim.index.name = "Step"
    df_sim.to_csv("simulation_results.csv")
    
    # Print speed milestones
    total_nodes = G.number_of_nodes()
    for name, history in results.items():
        step_50 = np.where(history >= total_nodes * 0.50)[0]
        step_90 = np.where(history >= total_nodes * 0.90)[0]
        t_50 = step_50[0] if len(step_50) > 0 else "N/A"
        t_90 = step_90[0] if len(step_90) > 0 else "N/A"
        print(f"  - {name:32}: 50% = {t_50} langkah, 90% = {t_90} langkah")

def visualize_network(G, partition, df_cent):
    print("Generating visualizations...")
    
    # 1. Static Plot (Matplotlib)
    print("  Drawing static visualization (network_static.png)...")
    plt.figure(figsize=(12, 12))
    
    # Calculate positions using spring layout
    print("    Calculating layout positions (Fruchterman-Reingold)...")
    pos = nx.spring_layout(G, k=0.08, iterations=15, seed=42)
    
    # Colors based on communities (top communities get colors, rest are gray)
    unique_comm = sorted(list(set(partition.values())))
    num_comm = len(unique_comm)
    
    color_palette = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", 
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
        "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5"
    ]
    while len(color_palette) < num_comm:
        color_palette += color_palette
        
    node_colors = [color_palette[partition[node]] for node in G.nodes()]
    
    # Node size scaled by degree centrality
    node_sizes = [2 + (df_cent.loc[node, "degree"] * 250) for node in G.nodes()]
    
    # Draw edges with high transparency (very thin to avoid hairball)
    nx.draw_networkx_edges(G, pos, alpha=0.01, width=0.1, edge_color="gray")
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.7)
    
    # Label top 3 centrality nodes (107, 1684, 1912)
    labels = {107: "Node 107 (Degree Hub)", 1684: "Node 1684 (Betweenness Hub)", 1912: "Node 1912 (Eigenvector Hub)"}
    nx.draw_networkx_labels(
        G, pos, labels=labels, font_size=9, font_weight='bold', font_color='black',
        bbox=dict(facecolor='white', edgecolor='red', alpha=0.8, boxstyle='round,pad=0.2')
    )
    
    plt.title("Visualisasi Jejaring Sosial Facebook SNAP\n(Warna menunjukkan Komunitas Louvain, Ukuran menunjukkan Degree Centrality)", fontsize=14, fontweight='bold', pad=15)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("network_static.png", dpi=300)
    plt.close()
    print("  Static visualization saved to network_static.png")
    
    # 2. Interactive Plot (PyVis HTML)
    print("  Generating interactive visualization (network_interactive.html)...")
    # To prevent browser rendering lag with 88,000 edges, we will export a representative 
    # subgraph containing the ego networks of the top 3 nodes (IDs 107, 1684, 1912)
    # This keeps the HTML light, responsive, and extremely informative!
    top_nodes = [107, 1684, 1912]
    subgraph_nodes = set(top_nodes)
    for node in top_nodes:
        subgraph_nodes.update(G.neighbors(node))
        
    G_sub = G.subgraph(subgraph_nodes)
    print(f"    Subsampling graph for interactive visualization: {G_sub.number_of_nodes()} nodes, {G_sub.number_of_edges()} edges")
    
    net = Network(height="800px", width="100%", bgcolor="#0f172a", font_color="white", directed=False)
    net.barnes_hut(gravity=-6000, central_gravity=0.3, spring_length=60, spring_strength=0.05, damping=0.09)
    
    # Draw nodes
    for node in G_sub.nodes():
        community = int(partition[node])
        deg = df_cent.loc[node, "degree"]
        bet = df_cent.loc[node, "betweenness"]
        clo = df_cent.loc[node, "closeness"]
        eig = df_cent.loc[node, "eigenvector"]
        
        tooltip = f"""
        <div style="font-family: sans-serif; padding: 10px; color: #1e293b; background: white; border-radius: 8px; border: 1px solid #cbd5e1;">
            <b style="font-size: 14px; color: #0f172a;">Node ID: {node}</b><br/>
            <hr style="margin: 5px 0; border: 0; border-top: 1px solid #e2e8f0;"/>
            <b>Komunitas (Louvain):</b> {community}<br/>
            <hr style="margin: 5px 0; border: 0; border-top: 1px solid #e2e8f0;"/>
            <b>SNA Centrality Scores:</b><br/>
            - Degree: {deg:.5f}<br/>
            - Betweenness: {bet:.5f}<br/>
            - Closeness: {clo:.5f}<br/>
            - Eigenvector: {eig:.5f}
        </div>
        """
        
        color = color_palette[community]
        size = 5 + (deg * 150)
        if node in top_nodes:
            size += 15
            
        net.add_node(
            int(node),
            label=f"Hub {node}" if node in top_nodes else "",
            title=tooltip,
            color=color,
            size=size,
            shape="dot"
        )
        
    for u, v in G_sub.edges():
        net.add_edge(
            int(u), int(v),
            color={"color": "#475569", "highlight": "#f43f5e", "hover": "#f43f5e", "opacity": 0.2},
            width=0.5
        )
        
    options = {
        "interaction": {
            "hover": True,
            "tooltipDelay": 200,
            "hideEdgesOnDrag": True
        },
        "physics": {
            "barnesHut": {
                "gravitationalConstant": -8000,
                "centralGravity": 0.3,
                "springLength": 60,
                "springStrength": 0.05,
                "damping": 0.09,
                "avoidOverlap": 0.2
            },
            "stabilization": {
                "enabled": True,
                "iterations": 100,
                "updateInterval": 25,
                "onlyDynamicEdges": False,
                "fit": True
            }
        }
    }
    
    net.set_options(json.dumps(options))
    net.save_graph("network_interactive.html")
    print("  Interactive visualization saved as network_interactive.html")

def main():
    filename = download_dataset()
    G = load_graph(filename)
    
    # Adjacency Matrix sample
    sample_nodes = [0, 1, 2, 3, 4]
    adj_matrix = nx.adjacency_matrix(G, nodelist=sample_nodes).todense()
    adj_matrix = np.array(adj_matrix).tolist()
    
    # Global metrics
    density = nx.density(G)
    avg_clustering = nx.average_clustering(G)
    
    largest_cc = max(nx.connected_components(G), key=len)
    G_lcc = G.subgraph(largest_cc)
    diameter = nx.diameter(G_lcc)
    avg_path_length = nx.average_shortest_path_length(G_lcc)
    
    # Louvain Communities
    partition = community_louvain.best_partition(G)
    modularity = community_louvain.modularity(partition, G)
    
    # Save community list
    df_nodes = pd.DataFrame(index=G.nodes())
    df_nodes["community"] = [partition[n] for n in df_nodes.index]
    df_nodes.index.name = "node_id"
    df_nodes.to_csv("nodes_with_community.csv")
    
    # Run/Load centralities
    df_cent = calculate_centralities(G)
    
    # Run simulations
    simulate_propagation(G, df_cent)
    
    # Visualizations
    visualize_network(G, partition, df_cent)
    
    # Export summary JSON
    summary = {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "density": density,
        "diameter": diameter,
        "avg_path_length": avg_path_length,
        "avg_clustering": avg_clustering,
        "modularity": modularity,
        "num_communities": len(set(partition.values())),
        "adj_matrix_sample": adj_matrix
    }
    
    with open("network_summary.json", "w") as f:
        json.dump(summary, f, indent=4)
        
    print("\nAll analysis steps executed successfully!")

if __name__ == "__main__":
    main()
