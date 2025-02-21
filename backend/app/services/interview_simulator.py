from openai import OpenAI
import os
from utils.config_manager import ConfigManager
from services.llm_manager import AIAdapter
from loguru import logger

class InterviewManager:
    def __init__(self, enhanced_resume, model_type):
        logger.info("inside InterviewManager..................")
        self.resume = enhanced_resume
        self.model_type = model_type
        self.context = []

    def _call_llm(self, prompt):
        """
        Helper method to call the LLM with a given prompt.
        """
        logger.debug("inside the call llm in InterviewManager")

        config = ConfigManager.update_config()
        logger.debug(f"config : {config}")
        adapter = AIAdapter(config, self.model_type)
        logger.debug(f"adapter : {adapter}")
        response = adapter.invoke(prompt)
        return response

    def generate_question(self, prev_question, prev_questions):
        prompt = f"""
        As professional interviewer, generate a technical question based on:
        {self.resume}
        The question asked was: {prev_question}
        If no question found, generate a new one.
        Based on the question, generate the next question.
        if not possible, then generate a new one.
        Avoid asking the following questions again: {", ".join(prev_questions)}
        Consider:
        - Most technical job role in any of the experiences mentioned
        - generate questions on Technical skills mentioned
        - Industry trends
        - generate open ended questions like "did you do any kind of design, architecture in your previous roles?"
        - Potential skill based questions
        - ask only one question, without any extra addons
        """
        return self._call_llm(prompt)
    
    def generate_answer(self, question):
        prompt = f"""
        As candidate with this resume: {self.resume}
        Answer: {question}
        consider yourself to be an Software Application Architect, answer the question based on this role.
        Guidelines for generating answer:
        1. Maintain truthful core
        2. Allow 20% exaggeration in scope/depth
        3. Infer related technologies if plausible and explain in brief about its usage
        4. Use STAR method for behavioral questions
        5. Explain technical concepts clearly and be a little verbose
        6. do not output any thinking, output only the best possible answer and nothing else.
        """
        return self._call_llm(prompt)