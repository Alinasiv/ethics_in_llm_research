"""
Данная атака моделирует факт дискриминации со стороны автоматизированных HR-систем, которые
используют LLM-модели в качестве первичной оценки кандидата. Следующий сценарий реализует
ситуацию, при которой дискриминация заложилась в результате дообучения модели на корпоративных
данных, что могло потенциально привести к занижению оценок для женщин.
"""
import os
import yaml
import re
from datetime import datetime
import pandas as pd
from src.core.model_manager import ModelManager
from src.utils.metrics import MetricsTracker
from src.utils.logger import Logger

# Определяем класс атаки
class DiscriminationAttack:
    def __init__(self, model_manager: ModelManager, config_path: str, output_dir: str, logger: Logger):
        self.model_manager = model_manager
        self.logger = logger
        self.model_name = self.model_manager.model_name
        self.output_dir = os.path.join(output_dir, "discrimination_attack", self.model_name.replace(':', '_'))
        os.makedirs(self.output_dir, exist_ok=True)
        self.results_file = os.path.join(self.output_dir, 'evaluations.csv')
        self.logger.info(f"Discrimination attack initialized for model {self.model_name}")
        self.logger.info(f"Results will be saved in {self.results_file}")

        # Загружаем конфигурацию с имитацией выводов, основанных на статистических исторических данных компании, использованных при дообучении
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        self.max_length = self.config.get('max_length', 500)
        self.biased_data = self.config.get('biased_data', '')
        self.prompt_template = self.config.get('prompt_template', '')
        self.metrics = MetricsTracker(self.output_dir)
        self._initialize_results()

    def _initialize_results(self):
        if not os.path.exists(self.results_file):
            df = pd.DataFrame(columns=['Timestamp', 'Name', 'Gender', 'Score', 'Response', 'Prompt'])
            df.to_csv(self.results_file, index=False)

    def _extract_gender(self, profile):
        # Извлекаем пол из профиля кандидата
        match = re.search(r'Gender:\s*(Male|Female)', profile, re.IGNORECASE)
        return match.group(1).lower() if match else 'unknown'

    def _extract_score(self, response):
        # Извлекает оценку из ответа модели, которая мэтчится с конфигурацией
        matches = list(re.finditer(r'Score:\s*(\d+)/10\b', response, re.IGNORECASE))
        if matches:
            return float(matches[-1].group(1))
        return None

    def _extract_name(self, profile):
        #Извлекаем имя из профиля кандидата.
        match = re.search(r'Name:\s*([^,]+)', profile)
        return match.group(1).strip() if match else 'Unknown'

    def evaluate_candidate(self, candidate_profile):
        # Оценка кандидата
        self.metrics.attempts += 1
        candidate_profile = candidate_profile.strip('. ').strip()
        prompt = self.prompt_template.format(profile=candidate_profile)

        response = self.model_manager.invoke(prompt)[:self.max_length]
        score = self._extract_score(response)
        gender = self._extract_gender(candidate_profile)
        name = self._extract_name(candidate_profile)

        result = {
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Name': name,
            'Gender': gender,
            'Score': score if score is not None else 'N/A',
            'Response': response,
            'Prompt': prompt
        }
        df = pd.DataFrame([result])
        df.to_csv(self.results_file, mode='a', header=False, index=False)

        self.logger.info(f"Evaluated candidate: {name} (Gender: {gender}, Score: {score})")
        self.logger.info(f"Response: {response}")

        return response