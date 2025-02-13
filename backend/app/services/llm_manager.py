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
        # logger.debug(f"response : {response}")
        return response


class DeepSeekModel(AIModel):
    def __init__(self, api_key: str,  llm_model: str):       
        self.api_key = api_key
        self.llm_model = llm_model
        logger.debug(f"self.api_key : {self.api_key}")
        logger.debug(f"self.llm_model : {self.llm_model}")  


    def invoke(self, prompt: str) -> BaseMessage:
        logger.debug("Invoking DeepSeek API")
        try:
            # Call the Deepseek API
            client = OpenAI(api_key=self.api_key, base_url="https://openrouter.ai/api/v1") 
            # logger.debug(f"prompt : {prompt}")
            # print("Sending payload:", {
            #     "model": self.llm_model,
            #     "messages": [{"role": "user", "content": prompt}],
            #     "temperature": 0.4,
            #     # "max_tokens": 5000,
            # })
            
            response = client.chat.completions.create(
                model=self.llm_model, 
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,  # Controls creativity (0 = deterministic, 1 = creative)
                # max_tokens=500,   # Limit the length of the response
            )
            print("response-------------------------------- : ", response)
            # Extract and return the generated text
            return response.choices[0].message.content.strip()

        except Exception as e:
            # Handle errors gracefully
            print(f"Error calling LLM: {e}")
            return "Sorry, I couldn't generate a response. Please try again."
    
    
class AIAdapter:
    def __init__(self, configs: dict, model_type: str):
        logger.debug(f"model type in AIAdapter : {model_type}")
        self.model = self._create_model(configs, model_type)

    def _create_model(self, configs: dict, model_type : str) -> AIModel:
        logger.debug(f"model type in create model of AIAdapter : {model_type}")
        logger.debug(f"configs in create model of AIAdapter : {configs}")
        for config in configs:
            logger.debug(f"config in create model of AIAdapter : {config}")
            if model_type in config.get("name"):
                logger.debug(f"config in create model of AIAdapter : {config}")
                llm_model = config['model_name'][0]
                logger.debug(f"llm_model : {llm_model}")
                llm_api_key = config['api_key']
                logger.debug(f"Using {model_type} with {llm_model}")
                break
            
        if model_type == "openai":
            return OpenAIModel(api_key=llm_api_key, llm_model=llm_model)
        elif model_type == "deepseek":
            return DeepSeekModel(api_key=llm_api_key, llm_model=llm_model)
        else:    
            raise ValueError(f"Unsupported model type: {model_type}")
        
        
    def invoke(self, prompt: str) -> str:
        return self.model.invoke(prompt)

