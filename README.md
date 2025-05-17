LLM Vulnerability Research
This repository supports multi-model LLM vulnerability research, focusing on data leakage and prompt injection attacks in enterprise strategy analysis. Designed for academic research on ethical LLM usage in business.
Setup in Visual Studio Code

Install Ollama: Download from https://ollama.com/download.
Pull Models:
ollama pull llama3.2:1b
ollama pull openhermes
ollama pull mistral
ollama pull zephyr
ollama pull qwen2:7b


Clone Repository:git clone <your-repo-url>
cd ethics_in_llm_research


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
In Visual Studio Code terminal:python src/scripts/run_attack_for_model.py --model llama3.2:3b --attack data_leakage


All Attacks:python src/scripts/run_all_attacks.py


Output

Results in src/results/{attack_name}/{model_name}:
visualizations/: Graphs (success rate, keyword leakage, etc.).


Logs in src/results/{attack_name}/{model_name}/attack.log.

Structure

configs/: Global and model-specific YAML configs.
src/: Core logic, attacks, utilities, results.

Notes

For academic use only in a controlled environment.
Run ollama serve before executing scripts.

