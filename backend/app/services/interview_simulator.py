from openai import OpenAI
import os


class InterviewManager:
    def __init__(self, enhanced_resume):
        self.resume = enhanced_resume
        self.context = []

    def _call_llm(self, prompt):
        """
        Helper method to call the LLM with a given prompt.
        """
        print("inside the call llm in InterviewManager")
        client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY_1"], base_url="https://openrouter.ai/api/v1")
        try:
            # Call the OpenAI API
            response = client.chat.completions.create(
                model="deepseek/deepseek-r1-distill-llama-8b",
                # model="gpt-4o-mini",  # Use GPT-4
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,  # Controls creativity (0 = deterministic, 1 = creative)
                max_tokens=5000,   # Limit the length of the response
            )
            # Extract and return the generated text
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Handle errors gracefully
            print(f"Error calling LLM: {e}")
            return "Sorry, I couldn't generate a response. Please try again."

    def generate_question(self):
        prompt = f"""
        As professional interviewer, generate a technical question based on:
        {self.resume}
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
        Guidelines:
        1. Maintain truthful core
        2. Allow 20% exaggeration in scope/depth
        3. Infer related technologies if plausible
        4. Use STAR method for behavioral questions
        5. Explain technical concepts clearly and be a little verbose
        6. No thinking out loud, only the best possible answer should be given and nothing else.
        """
        return self._call_llm(prompt)