"""LangChain prompt for structuring raw job-description text."""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from config import get_llm
from schemas.pydantic_models import JDOutput

def get_jd_chain():
    """Build the chain that extracts structured job description fields."""
    parser = PydanticOutputParser(pydantic_object=JDOutput)
    jd_format = parser.get_format_instructions()

    prompt = PromptTemplate(
    template="""
Extract structured job description.

{format_instructions}

Job Description:
{text}
""",
    input_variables=["text"],
    partial_variables={"format_instructions": jd_format}
)

    return prompt | get_llm() | parser
