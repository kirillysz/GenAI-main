from typing import AsyncGenerator, List, Dict
from ollama import AsyncClient

import asyncio

class UnsupportedModelError(Exception):
    pass

class Model:
    def __init__(self, model_name: str = 'llama3.2'):
        self.model_name = model_name
        self.client = AsyncClient()
        self._validate_model()

    def _validate_model(self):
        supported_models = ['llama3.2', 'llama3.1:8b', "deepseek-r1:14b"]
        if self.model_name not in supported_models:
            raise UnsupportedModelError(f"Model {self.model_name} not supported")

    async def generate_answer(
        self, 
        messages: List[Dict[str, str]]
    ):
        try:
            response = await self.client.chat(
                model=self.model_name,
                messages=messages,
                stream=False
            )

            return response.message.content
                
        except Exception as e:
            raise Exception(e)
