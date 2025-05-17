import os
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

class InjectionSpreadVisualization:
    def __init__(self, output_dir):
        self.output_dir = os.path.join(output_dir, 'visualizations')
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_visualizations(self, injection_paths, leak_counts, depth_leaks, node_response_times, contacts_network, sensitive_data, leaked_keywords):
        self._plot_network(injection_paths, leak_counts, contacts_network)
        self._plot_depth_leaks(depth_leaks)

    def _plot_network(self, injection_paths, leak_counts, contacts_network):
        G = nx.DiGraph()

        for sender, contact in injection_paths:
            G.add_edge(sender, contact, weight=leak_counts.get(contact, 0))
        
        node_colors = ['#99FF99' if leak_counts.get(node, 0) > 0 else '#FF9999' for node in G.nodes()]
        
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True)
        nx.draw_networkx_labels(G, pos)
        
        edge_labels = {(sender, contact): leak_counts.get(contact, 0) for sender, contact in injection_paths}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        
        plt.title('Injection Spread Network (Green = Leak, Red = No Leak)')
        plt.axis('off')
        plt.savefig(os.path.join(self.output_dir, 'injection_network.png'))
        plt.close()

    def _plot_depth_leaks(self, depth_leaks):
        df = pd.DataFrame({'Depth': list(depth_leaks.keys()), 'Leaks': list(depth_leaks.values())})
        plt.figure(figsize=(10, 6))
        plt.bar(df['Depth'], df['Leaks'], color='#99FF99') 
        plt.title('Data Leaks by Depth')
        plt.xlabel('Depth')
        plt.ylabel('Number of Leaks')
        plt.savefig(os.path.join(self.output_dir, 'depth_leaks.png'))
        plt.close()