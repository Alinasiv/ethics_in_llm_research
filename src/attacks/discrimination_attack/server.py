import argparse
import os
import sys
import pandas as pd
import yaml
from flask import Flask, request, jsonify, send_from_directory

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.attacks.discrimination_attack.attack import DiscriminationAttack
from src.core.model_manager import ModelManager
from src.utils.logger import Logger

app = Flask(__name__)
app.static_folder = os.path.join(os.path.dirname(__file__), 'static')

parser = argparse.ArgumentParser(description="Run Discrimination Attack server.")
parser.add_argument('--model', type=str, required=True, help="Model config name (e.g., llama, qwen, mistral)")
parser.add_argument('--port', type=int, default=5001, help="Port to run the server on")
args = parser.parse_args()

# Load model config to get the actual model name
model_config_path = os.path.join(BASE_DIR, 'configs', 'models', f"{args.model}.yaml")
if not os.path.exists(model_config_path):
    print(f"Error: Model config file not found at {model_config_path}")
    sys.exit(1)

with open(model_config_path, 'r', encoding='utf-8') as f:
    model_config = yaml.safe_load(f)

model_name = model_config.get('model_name')
if not model_name:
    print(f"Error: 'model_name' not found in {model_config_path}")
    sys.exit(1)

# Use the actual model name for directory and logging
safe_model_name = model_name.replace(':', '_')
logger = Logger(os.path.join(BASE_DIR, 'src', 'results', 'discrimination_attack', safe_model_name, 'attack.log'))
model_manager = ModelManager(model_name=model_name)
attack = DiscriminationAttack(
    model_manager,
    os.path.join(BASE_DIR, 'configs', 'attacks', 'discrimination_attack', 'config.yaml'),
    os.path.join(BASE_DIR, 'src', 'results'), logger
)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/evaluate', methods=['POST'])
def evaluate_candidate():
    profile = request.json.get('profile')
    if not profile:
        return jsonify({'error': 'No profile provided'}), 400
    evaluation = attack.evaluate_candidate(profile)
    return jsonify({'evaluation': evaluation})

@app.route('/api/results', methods=['GET'])
def get_results():
    results_file = os.path.join(attack.output_dir, 'evaluations.csv')
    if not os.path.exists(results_file):
        return jsonify({'results': []})
    df = pd.read_csv(results_file)
    return jsonify({'results': df.to_dict(orient='records')})

if __name__ == '__main__':
    print(f"Starting server for model: {model_name} (config: {args.model})")
    app.run(debug=True, host='0.0.0.0', port=args.port)