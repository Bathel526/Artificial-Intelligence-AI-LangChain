from app.core.model import model
from app.prompts.general_prompt import prompt


prompt_chain = prompt | model