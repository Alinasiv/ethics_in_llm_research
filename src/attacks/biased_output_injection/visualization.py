# Данный класс необходим для визуализации прогресса атаки BiasedOutputInjection.
import matplotlib.pyplot as plt
import os

# Создание класса для визуализации прогресса атаки BiasedOutputInjection
class BiasedOutputInjectionVisualization:
    def __init__(self, output_dir: str, attack_type: str):
        self.output_dir = os.path.join(output_dir, "visualizations")
        os.makedirs(self.output_dir, exist_ok=True)
        self.attack_type = attack_type

    def plot_attack_progress(self, all_samples: list, best_samples: list, average_fitness_samples: list):
        """
        График прогресса атаки, включающий в себя:
        """
        plt.figure(figsize=(8, 6))
        
        if all_samples:
            all_gens, all_fits = zip(*all_samples)
            plt.scatter(all_gens, all_fits, alpha=0.2, color='gray', label="All Samples", s=30)
        
        if best_samples:
            best_gens, best_fits = zip(*best_samples)
            plt.plot(best_gens, best_fits, 'r-', linewidth=2, label="Best Fitness")
        
        if average_fitness_samples:
            avg_gens, avg_fits = zip(*average_fitness_samples)
            plt.plot(avg_gens, avg_fits, 'b--', linewidth=2, label="Average Fitness")
        
        plt.xlabel("Generation", fontsize=12)
        plt.ylabel("Fitness (Negative Score)", fontsize=12)
        plt.title(f"Attack Progress ({self.attack_type})", fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=10)
        plt.tight_layout()
        
        plot_path = os.path.join(self.output_dir, 'attack_progress.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()