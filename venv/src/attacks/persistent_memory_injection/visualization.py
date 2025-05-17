import os
import matplotlib.pyplot as plt

class PersistentMemoryInjectionVisualization:
    def __init__(self, output_dir: str):
        self.output_dir = os.path.join(output_dir, "visualizations")
        os.makedirs(self.output_dir, exist_ok=True)
        plt.style.use('ggplot')

    def generate_visualizations(self, successful_exfils, jargon_usage, exfil_timestamps, session_count):
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.labelsize'] = 10
        plt.rcParams['axes.titlesize'] = 12
        plt.rcParams['legend.fontsize'] = 8

        # Exfiltration timeline
        plt.figure(figsize=(10, 5), dpi=100)
        sessions = list(range(1, session_count + 1))
        successes = successful_exfils[:session_count]
        if len(successes) < session_count:
            successes.extend([0] * (session_count - len(successes)))
        total_successes = sum(successes)

        plt.plot(sessions, successes, marker='o', color='blue', linestyle='-', linewidth=2, label='Success (1=Yes, 0=No)')
        if total_successes == 0:
            plt.text(0.5, 0.5, "No successful exfiltrations", ha='center', va='center', transform=plt.gca().transAxes, fontsize=10)

        plt.xlabel("Session Number")
        plt.ylabel("Success (1=Yes, 0=No)")
        plt.title(f"Exfiltration Timeline Across Sessions (Successes: {total_successes})")
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend(loc='best')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'exfiltration_timeline.png'))
        plt.close()

        # Jargon usage histogram
        plt.figure(figsize=(8, 5), dpi=100)
        jargon = list(jargon_usage.keys())
        counts = list(jargon_usage.values())
        total_usage = sum(counts)
        
        bars = plt.bar(jargon, counts, color='orange', edgecolor='black', alpha=0.7)
        if total_usage > 0:
            for bar in bars:
                yval = bar.get_height()
                percentage = (yval / total_usage) * 100
                plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f"{int(yval)} ({percentage:.1f}%)", ha='center', fontsize=8)
        else:
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f"{int(yval)}", ha='center', fontsize=8)

        plt.xlabel("Corporate Jargon")
        plt.ylabel("Usage Count")
        plt.title(f"Corporate Jargon Usage (Total: {total_usage})")
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'jargon_usage.png'))
        plt.close()

        # Success rate pie chart
        success_count = sum(successes)
        failure_count = session_count - success_count
        labels = ['Successful', 'Failed']
        sizes = [success_count, failure_count]
        colors = ['green', 'red']
        plt.figure(figsize=(6, 6), dpi=100)
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        plt.title("Exfiltration Success Rate")
        plt.savefig(os.path.join(self.output_dir, 'exfil_success_rate.png'))
        plt.close()