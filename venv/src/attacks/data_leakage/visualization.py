import matplotlib.pyplot as plt
import os

class DataLeakageVisualization:
    def __init__(self, output_dir: str, attack_type: str):
        self.output_dir = os.path.join(output_dir, "visualizations")
        os.makedirs(self.output_dir, exist_ok=True)
        self.attack_type = attack_type

    def plot_trigger_success(self, trigger_variants: dict):
        plt.figure(figsize=(8, 6))
        plt.bar(trigger_variants.keys(), trigger_variants.values(), color='blue')
        plt.title(f'Trigger Success Count ({self.attack_type})')
        plt.xlabel('Triggers')
        plt.ylabel('Successful Leaks')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'trigger_success.png'))
        plt.close()

    def plot_keyword_leakage(self, leaked_keywords: dict):
        plt.figure(figsize=(8, 6))
        plt.bar(leaked_keywords.keys(), leaked_keywords.values(), color='red')
        plt.title(f'Keyword Leakage Count ({self.attack_type})')
        plt.xlabel('Keywords')
        plt.ylabel('Occurrences')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'keyword_leakage.png'))
        plt.close()

    def plot_success_rate(self, successes: int, attempts: int):
        plt.figure(figsize=(6, 6))
        plt.pie([successes, attempts - successes], labels=['Successful', 'Failed'], colors=['green', 'red'], autopct='%1.1f%%')
        plt.title(f'Success Rate ({self.attack_type})')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'success_rate.png'))
        plt.close()

    def plot_response_times(self, response_times: list):
        plt.figure(figsize=(8, 6))
        plt.hist(response_times, bins=20, color='purple')
        plt.title(f'Response Time Distribution ({self.attack_type})')
        plt.xlabel('Response Time (sec)')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'response_times.png'))
        plt.close()

    def generate_visualizations(self, trigger_variants: dict, leaked_keywords: dict, successes: int, attempts: int, response_times: list):
        self.plot_trigger_success(trigger_variants)
        self.plot_keyword_leakage(leaked_keywords)
        self.plot_success_rate(successes, attempts)
        self.plot_response_times(response_times)