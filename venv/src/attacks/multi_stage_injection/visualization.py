import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class MultiStageInjectionVisualization:
    def __init__(self, output_dir):
        self.output_dir = os.path.join(output_dir, 'visualizations')
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_visualizations(self, successful_exfils, exfiltrated_data, corporate_jargon, session_count, code_activations):
        self._plot_exfiltration_stages(successful_exfils, code_activations, session_count)
        self._plot_jargon_usage(corporate_jargon)

    def _plot_exfiltration_stages(self, successful_exfils, code_activations, session_count):
        stages = pd.DataFrame({
            'Stage': list(range(1, len(successful_exfils) + 1)),
            'Success': [True if x == 1 else False for x in successful_exfils],
            'CodeActivation': [True if x == 1 else False for x in code_activations]
        })

        # Проверяем, есть ли разнообразие в Success (успехи и провалы)
        if len(stages['Success'].unique()) > 1:  # Если есть и True, и False
            plt.figure(figsize=(10, 6))
            sns.countplot(data=stages, x='Stage', hue='Success', palette={True: '#99FF99', False: '#FF9999'})  # Зеленый для успеха, красный для провала
            plt.title('Exfiltration Success by Stage')
            plt.xlabel('Stage')
            plt.ylabel('Count')
            plt.savefig(os.path.join(self.output_dir, 'exfiltration_stages.png'))
            plt.close()
        else:
            # Если все успехи или все провалы, записываем сообщение вместо графика
            with open(os.path.join(self.output_dir, 'exfiltration_stages.txt'), 'w') as f:
                status = "Success" if stages['Success'].iloc[0] else "Failure"
                f.write(f"All stages resulted in {status}. No plot generated.\n")

        # Аналогично для CodeActivation
        if len(stages['CodeActivation'].unique()) > 1:
            plt.figure(figsize=(10, 6))
            sns.countplot(data=stages, x='Stage', hue='CodeActivation', palette={True: '#99FF99', False: '#FF9999'})
            plt.title('Code Activation by Stage')
            plt.xlabel('Stage')
            plt.ylabel('Count')
            plt.savefig(os.path.join(self.output_dir, 'code_activation_stages.png'))
            plt.close()
        else:
            with open(os.path.join(self.output_dir, 'code_activation_stages.txt'), 'w') as f:
                status = "Activated" if stages['CodeActivation'].iloc[0] else "Not Activated"
                f.write(f"Code activation status for all stages: {status}. No plot generated.\n")

    def _plot_jargon_usage(self, corporate_jargon):
        plt.figure(figsize=(8, 6))
        sns.countplot(x=corporate_jargon)
        plt.title('Corporate Jargon Usage')
        plt.xlabel('Jargon')
        plt.ylabel('Count')
        plt.savefig(os.path.join(self.output_dir, 'jargon_usage.png'))
        plt.close()