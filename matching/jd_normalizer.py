"""LLM chain that normalizes job-description text into atomic skills."""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from config import get_llm
from schemas.pydantic_models import NormalizedSkills

def get_jd_normalizer_chain():
    """Build the chain that expands and cleans JD skill requirements."""
    parser = PydanticOutputParser(pydantic_object=NormalizedSkills)
    jd_normalize_format = parser.get_format_instructions()

    prompt = PromptTemplate(
        template="""
Convert the following job requirements into a clean list of atomic technical skills.

RULES:
- break combined statements into individual skills
- remove experience requirements (e.g., 5 years)
- remove generic filler phrases like "knowledge of", "ability to", "understanding of", "experience in"
- expand "at least one of Django, Flask or FastAPI" into separate skills: django, flask, fastapi
- keep only concrete technologies, frameworks, libraries, or architecture concepts

{format_instructions}

Input:
{text}
""",
        input_variables=["text"],
        partial_variables={"format_instructions": jd_normalize_format}
    )

    return prompt | get_llm() | parser
