import os
import matplotlib.pyplot as plt

class RemoteFinancialControlVisualization:
    def __init__(self, output_dir: str):
        self.output_dir = os.path.join(output_dir, "visualizations")
        os.makedirs(self.output_dir, exist_ok=True)
        plt.style.use('ggplot')

    def generate_visualizations(self, successful_exfils, jargon_usage, exfil_timestamps, request_count, exfiltrated_data=None):
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.labelsize'] = 10
        plt.rcParams['axes.titlesize'] = 12
        plt.rcParams['legend.fontsize'] = 8

        # 1. Гистограмма использования жаргона
        plt.figure(figsize=(8, 5), dpi=100)
        jargon_terms = list(jargon_usage.keys())
        usage_counts = list(jargon_usage.values())
        total_usage = sum(usage_counts)
        
        bars = plt.bar(jargon_terms, usage_counts, color='#1f77b4', edgecolor='black', alpha=0.7)
        
        if total_usage > 0:
            for bar in bars:
                yval = bar.get_height()
                percentage = (yval / total_usage) * 100
                plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f"{int(yval)} ({percentage:.1f}%)", ha='center', fontsize=8)
        else:
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f"{int(yval)}", ha='center', fontsize=8)

        plt.xlabel("Market Jargon Terms")
        plt.ylabel("Usage Count")
        plt.title(f"Market Jargon Usage (Total: {total_usage})")
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'jargon_usage_histogram.png'))
        plt.close()

        # 2. Линейный график успешности эксфильтрации по времени
        plt.figure(figsize=(10, 5), dpi=100)
        requests = list(range(1, request_count + 1))
        successes = successful_exfils
        total_successes = sum(successful_exfils)

        if exfil_timestamps and len(exfil_timestamps) >= request_count:
            relative_times = [(t - exfil_timestamps[0]) for t in exfil_timestamps[:request_count]]
            plt.plot(relative_times, successes, marker='o', color='#2ca02c', linestyle='-', linewidth=2, label='Success (1=Yes, 0=No)')

            if exfiltrated_data and len(exfiltrated_data) > 0:
                data_types = [data[0].split(':')[0] for data in exfiltrated_data]
                for i, (time_val, success, data_type) in enumerate(zip(relative_times, successes, data_types[:len(successes)])):
                    if success == 1:
                        plt.annotate(data_type, (time_val, success), textcoords="offset points", xytext=(0, 15), ha='center', fontsize=8)
            else:
                plt.text(0.5, 0.5, "No successful exfiltrations", ha='center', va='center', transform=plt.gca().transAxes, fontsize=10)

            plt.xlabel("Time (seconds since first request)")
            plt.ylabel("Success (1=Yes, 0=No)")
            plt.title(f"Exfiltration Success Over Time (Successes: {total_successes})")
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.legend(loc='best')
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'exfiltration_success_over_time.png'))
            plt.close()
        else:
            with open(os.path.join(self.output_dir, 'exfiltration_success_over_time.txt'), 'w') as f:
                f.write(f"Insufficient timestamps ({len(exfil_timestamps)}) for {request_count} requests.")