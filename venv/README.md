LLM Vulnerability Research
This repository supports multi-model LLM vulnerability research, focusing on data leakage and prompt injection attacks in enterprise strategy analysis. Designed for academic research on ethical LLM usage in business.
Setup in Visual Studio Code

Install Ollama: Download from https://ollama.com/download.
Pull Models:ollama pull llama3.2:1b

(For phi3 and qwen, configure via HuggingFace in configs/models/.)
Clone Repository:git clone <your-repo-url>
cd llm_vulnerability_research


Install Dependencies:
Open Visual Studio Code: code .
Open terminal (Ctrl+` or Terminal > New Terminal).
Install:pip install -r requirements.txt




Configure:
Edit configs/global_config.yaml for output paths and models.
Update configs/models/llama3_2_1b.yaml for llama3.2:1b settings.
Set output_dir to /Users/alinasivova/llama32/ in global_config.yaml.



Running Attacks

Single Model Attack:
In Visual Studio Code terminal:python src/scripts/run_attack_for_model.py --model llama3.2:1b --attack data_leakage




All Attacks (TBD):python src/scripts/run_all_attacks.py


Compare Models (TBD):python src/scripts/compare_models.py



Output

Results in src/results/{model_name}/:
attack_metrics.csv: Leakage metrics.
visualizations/: Graphs (success rate, keyword leakage, etc.).


Logs in src/results/{model_name}/attack.log.

Structure

configs/: Global and model-specific YAML configs.
src/: Core logic, attacks, utilities, results.
tests/: Unit tests for multi-model functionality.

Notes

For academic use only in a controlled environment.
Ensure /Users/alinasivova/llama32/ is writable.
Original code for plagiarism checks.
Run ollama serve before executing scripts.

