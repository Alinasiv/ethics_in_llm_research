import os
import matplotlib.pyplot as plt
import pandas as pd

class JailbreakAttackVisualization:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(os.path.join(self.output_dir, "visualizations"), exist_ok=True)

    def generate_visualizations(self, responses, response_timestamps, attempt_count, jailbreak_details):
        # Подготовка данных для графика
        attempts = list(range(1, attempt_count + 1))
        jailbreak_successes = [1 if r[2] else 0 for r in responses]

        # График успеха джейлбрейка
        plt.figure(figsize=(8, 5))
        plt.plot(attempts, jailbreak_successes, 'go-', label='Jailbreak Success', markersize=8)
        plt.title('Jailbreak Success Across Attempts', fontsize=12)
        plt.xlabel('Attempt Number', fontsize=10)
        plt.ylabel('Success (1 = Yes, 0 = No)', fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=10)
        plt.xticks(attempts)
        plt.savefig(os.path.join(self.output_dir, 'visualizations', 'jailbreak_success.png'))
        plt.close()

