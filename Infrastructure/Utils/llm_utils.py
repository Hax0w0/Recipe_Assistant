import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from Domain.recipe import Recipe

class LLM_Utils:

    def connect_to_llm(self) -> ChatOpenAI:

        # Load environment variables from .env file
        load_dotenv()

        # Retrieve values from environment variables
        key = os.getenv("KEY")
        endpoint = os.getenv("ENDPOINT")
        deployment_name = os.getenv("DEPLOYMENT_NAME")

        # Connect to the model
        llm = ChatOpenAI(model=deployment_name,
                        base_url=endpoint,
                        api_key=key)
        
        return llm
    
    def summarize_recipe(self, recipe: Recipe) -> str:

        # Connect to the model
        llm = self.connect_to_llm()

        # Create the prompt and generate summary
        prompt = recipe.get_summary_prompt()
        summary = llm.invoke(prompt).content

        return summary
    
    def rate_recipe(self, recipe: Recipe) -> str:

        # Connect to the model
        llm = self.connect_to_llm()

        # Create the prompt and generate rating
        prompt = recipe.get_rating_prompt()
        rating = llm.invoke(prompt).content

        return rating
    