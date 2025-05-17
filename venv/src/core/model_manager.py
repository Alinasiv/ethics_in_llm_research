from langchain_ollama import OllamaLLM
import logging
import os

class ModelManager:
    def __init__(self, model_name: str, temperature: float = 0.7, top_p: float = 0.9, max_tokens: int = 1000, num_ctx: int = 8192, log_file: str = "model_manager.log"):
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.num_ctx = num_ctx
        self.logger = logging.getLogger("ModelManager")
        self.logger.setLevel(logging.INFO)
        
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        
        self.model = self._initialize_model()

    def _initialize_model(self):
        try:
            self.logger.info(f"Initializing model: {self.model_name} with temperature={self.temperature}, top_p={self.top_p}, max_tokens={self.max_tokens}, num_ctx={self.num_ctx}")
            return OllamaLLM(
                model=self.model_name,
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=self.max_tokens,
                num_ctx=self.num_ctx
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize {self.model_name}: {e}")
            raise RuntimeError(f"Model initialization failed: {e}")

    def invoke(self, prompt: str) -> str:
        try:
            self.logger.info(f"Invoking model {self.model_name} with prompt: {prompt[:50]}...")
            response = self.model.invoke(prompt)
            self.logger.info(f"Response received: {response[:50]}...")
            return response
        except Exception as e:
            self.logger.error(f"Error during invoke: {e}")
            raise