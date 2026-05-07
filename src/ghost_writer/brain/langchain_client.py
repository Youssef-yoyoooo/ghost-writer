from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from .prompts import QA_ENGINEER_PROMPT

class BrainClient:
    def __init__(self, model: str = "llama3"):
        self.llm = Ollama(model=model)
        self.prompt_template = PromptTemplate.from_template(QA_ENGINEER_PROMPT)

    def analyze_code(self, code: str, file_path: str) -> str:
        """Analyze code for vulnerabilities using local LLM."""
        formatted_prompt = self.prompt_template.format(code=code, file_path=file_path)
        try:
            response = self.llm.invoke(formatted_prompt)
            return response
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"
