import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud

class HallucinationAttackVisualization:
    def __init__(self, output_dir: str):
        self.output_dir = os.path.join(output_dir, "visualizations")
        os.makedirs(self.output_dir, exist_ok=True)
        plt.style.use('ggplot')

    def generate_visualizations(self, responses, response_timestamps, attempt_count):
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.labelsize'] = 10
        plt.rcParams['axes.titlesize'] = 12
        plt.rcParams['legend.fontsize'] = 8

        # 1. Гистограмма объёма ответов с выделением галлюцинаций
        plt.figure(figsize=(10, 6), dpi=100)
        attempt_nums = list(range(1, attempt_count + 1))
        response_lengths = [len(r[1].split()) for r in responses]
        is_hallucination = [1 if r[2] else 0 for r in responses]

        bar_width = 0.35
        plt.bar([x - bar_width/2 for x in attempt_nums], response_lengths, bar_width, label='Response Length (words)', color='#1f77b4', alpha=0.7)
        plt.bar([x + bar_width/2 for x in attempt_nums], [l * h for l, h in zip(response_lengths, is_hallucination)], bar_width, label='Hallucination Volume', color='#ff7f0e', alpha=0.7)

        for i, (length, halluc) in enumerate(zip(response_lengths, is_hallucination)):
            plt.text(i + 1, length + 1, f"{length}w", ha='center', va='bottom', fontsize=8)
            if halluc:
                plt.text(i + 1, length * halluc + 1, "H", ha='center', va='bottom', fontsize=8, color='red')

        plt.xlabel("Attempt Number")
        plt.ylabel("Word Count")
        plt.title("Response Length vs Hallucination Volume")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'hallucination_volume_histogram.png'))
        plt.close()

        # 2. Облако слов (разделяем слова для галлюцинаций и валидных ответов)
        halluc_words = " ".join([r[1].lower() for r in responses if r[2]])
        valid_words = " ".join([r[1].lower() for r in responses if not r[2]])

        # Облако слов для галлюцинаций
        if halluc_words:
            wordcloud_halluc = WordCloud(width=800, height=400, background_color='white', colormap='Oranges', min_font_size=10).generate(halluc_words)
            plt.figure(figsize=(10, 5), dpi=100)
            plt.imshow(wordcloud_halluc, interpolation='bilinear')
            plt.axis('off')
            plt.title("Word Cloud of Hallucinated Responses")
            plt.savefig(os.path.join(self.output_dir, 'hallucination_wordcloud.png'))
            plt.close()

        # Облако слов для валидных ответов
        if valid_words:
            wordcloud_valid = WordCloud(width=800, height=400, background_color='white', colormap='Greens', min_font_size=10).generate(valid_words)
            plt.figure(figsize=(10, 5), dpi=100)
            plt.imshow(wordcloud_valid, interpolation='bilinear')
            plt.axis('off')
            plt.title("Word Cloud of Valid Responses")
            plt.savefig(os.path.join(self.output_dir, 'valid_wordcloud.png'))
            plt.close()