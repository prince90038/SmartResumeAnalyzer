"""LangChain prompt for extracting technical skills from a resume section."""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from config import get_llm
from schemas.pydantic_models import SkillsOutput

def get_skills_chain():
    """Build the chain that extracts only technical skills."""
    parser = PydanticOutputParser(pydantic_object=SkillsOutput)
    fmt = parser.get_format_instructions()

    prompt = PromptTemplate(
        template="""
Extract ONLY technical skills.

{format_instructions}

Text:
{text}
""",
        input_variables=["text"],
        partial_variables={"format_instructions": fmt}
    )

    return prompt | get_llm() | parser
