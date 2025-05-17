import argparse
import os
import sys
import yaml

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.core.model_manager import ModelManager
from src.core.knowledge_base import KnowledgeBase
from src.attacks.injection_spread.attack import InjectionSpreadAttack
from src.attacks.multi_stage_injection.attack import MultiStageInjection   
from src.attacks.hallucination_attack.attack import HallucinationAttack
from src.attacks.disinformation_attack.attack import DisinformationAttack
from src.attacks.jailbreak_attack.attack import JailbreakAttack
from src.attacks.data_leakage.attack import DataLeakageAttack
from src.attacks.remote_financial_control.attack import RemoteFinancialControl
from src.attacks.persistent_memory_injection.attack import PersistentMemoryInjection
from src.attacks.biased_output_injection.attack import BiasedOutputInjection
from src.utils.logger import Logger

def load_config(config_path):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="Run an attack on a specified model.")
    parser.add_argument('--model', type=str, required=True, help="Model name (e.g., openhermes, llama3.2:1b)")
    parser.add_argument('--attack', type=str, required=True, choices=['data_leakage', 'injection_spread', 'remote_financial_control', 'persistent_memory_injection', 'multi_stage_injection', 'hallucination_attack', 'disinformation_attack', 'jailbreak_attack', 'data_leakage', 'persistent_memory_injection', 'remote_financial_control', 'biased_output_injection'], help="Attack type")
    args = parser.parse_args()

    config_dir = os.path.join(BASE_DIR, 'configs')
    results_dir = os.path.join(BASE_DIR, 'src', 'results')

    model_config_path = os.path.join(config_dir, 'models', f"{args.model.replace(':', '_')}.yaml")
    if not os.path.exists(model_config_path):
        print(f"Error: Model config {model_config_path} not found.")
        sys.exit(1)
    model_config = load_config(model_config_path)
    model_name = model_config['model_name']

    attack_config_path = os.path.join(config_dir, 'attacks', args.attack, 'config.yaml')
    if not os.path.exists(attack_config_path):
        print(f"Error: Attack config {attack_config_path} not found.")
        sys.exit(1)

    safe_model_name = model_name.replace(':', '_')
    model_results_dir = os.path.join(results_dir, args.attack, safe_model_name)
    os.makedirs(model_results_dir, exist_ok=True)

    model_manager = ModelManager(
        model_name=model_name,
        temperature=model_config.get('temperature', 0.7),
        top_p=model_config.get('top_p', 0.9),
        max_tokens=model_config.get('max_tokens', 1000),
        num_ctx=model_config.get('num_ctx', 4096),
        log_file=os.path.join(model_results_dir, 'model_manager.log')
    )
    knowledge_base = KnowledgeBase()
    logger = Logger(os.path.join(model_results_dir, f'{args.attack}.log'))

    attack_classes = {
        'injection_spread': InjectionSpreadAttack,
        'multi_stage_injection': MultiStageInjection,
        'hallucination_attack': HallucinationAttack,
        'disinformation_attack': DisinformationAttack,
        'jailbreak_attack': JailbreakAttack,
        'data_leakage': DataLeakageAttack,
        'remote_financial_control': RemoteFinancialControl,
        'persistent_memory_injection': PersistentMemoryInjection,
        'biased_output_injection': BiasedOutputInjection
    }

    if args.attack not in attack_classes:
        print(f"Error: Attack {args.attack} not implemented.")
        sys.exit(1)

    try:
        attack = attack_classes[args.attack](
            model_manager=model_manager,
            knowledge_base=knowledge_base,
            config_path=attack_config_path,
            output_dir=results_dir,
            logger=logger
        )
    except Exception as e:
        logger.error(f"Failed to initialize {args.attack}: {e}")
        sys.exit(1)

    attack.run()

    print(f"Attack {args.attack} completed for model {model_name}. Results saved in {model_results_dir}")

if __name__ == '__main__':
    main()