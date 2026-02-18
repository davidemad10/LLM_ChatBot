"""Prompt configuration management."""
import json
import os
from typing import Dict, Any
from ..utils.logging import setup_logger

logger = setup_logger("config_manager")

# Get the path relative to this file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "prompt_config.json")

DEFAULT_CONFIG = {
    "prompt_template": "Answer the question based on the following context:\n\n{context}\n\n---\n\nQuestion: {question}\n\nIf the answer is in the context, use it. If the context doesn't contain the answer, you may use your own knowledge to help answer the question.",
    "system_message": "You are a helpful assistant. Prioritize using the provided context to answer questions. If the context doesn't contain the answer, you can use your general knowledge to provide a helpful response.",
    "similarity_threshold": 0.2,
    "top_k_results": 3
}


class PromptManager:
    """Manages application prompts from JSON file."""
    
    def __init__(self, config_path: str = CONFIG_PATH):
        self.config_path = config_path
        self._ensure_config_exists()
    
    def _ensure_config_exists(self):
        """Create config file with defaults if it doesn't exist."""
        if not os.path.exists(self.config_path):
            logger.warning("Config file not found, creating with defaults")
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
    
    def get(self) -> Dict[str, Any]:
        """Get current configuration from JSON file."""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                logger.debug("Configuration loaded successfully", extra={'stage': 'CONFIG'})
                return config
        except FileNotFoundError:
            logger.warning("Config file not found, using defaults")
            return DEFAULT_CONFIG
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            return DEFAULT_CONFIG


# Create a singleton instance
prompt_manager = PromptManager()
