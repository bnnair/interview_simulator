from abc import ABC, abstractmethod
from langchain_core.messages import BaseMessage
from loguru import logger
from openai import OpenAI
import os
from langchain_openai import ChatOpenAI


class AIModel(ABC):
    @abstractmethod
    def invoke(self, prompt: str) -> str:
        pass


class OpenAIModel(AIModel):
    def __init__(self, api_key: str, llm_model: str):
        self.model = ChatOpenAI(model_name=llm_model, openai_api_key=api_key,
                                temperature=0.4)

    def invoke(self, prompt: str) -> BaseMessage:
        logger.debug("Invoking OpenAI API")
        response = self.model.invoke(prompt)
        return response


class DeepSeekModel(AIModel):
    def __init__(self, api_key: str,  llm_model: str):       
        self.api_key = api_key
        self.llm_model = llm_model

class AIAdapter:
    def __init__(self, config: dict, api_key: str):
        self.model = self._create_model(config, api_key)

    def _create_model(self, config: dict, api_key: str) -> AIModel:
        llm_model_type = config['llm_model_type']
        llm_model = config['llm_model'][0]

        logger.debug(f"Using {llm_model_type} with {llm_model}")

        if llm_model_type == "openai":
            return OpenAIModel(api_key, llm_model)
        else:
            raise ValueError(f"Unsupported model type: {llm_model_type}")

    def invoke(self, prompt: str) -> str:
        return self.model.invoke(prompt)

