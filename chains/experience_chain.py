from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from config import get_llm
from schemas.pydantic_models import ExperienceOutput

def get_experience_chain():
    parser = PydanticOutputParser(pydantic_object=ExperienceOutput)
    fmt = parser.get_format_instructions()

    prompt = PromptTemplate(
        template="""
Extract experience with:
company, role, duration, description.

{format_instructions}

Text:
{text}
""",
        input_variables=["text"],
        partial_variables={"format_instructions": fmt}
    )

    return prompt | get_llm() | parser
