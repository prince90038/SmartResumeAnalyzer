"""LangChain prompt for extracting structured education entries."""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from config import get_llm
from schemas.pydantic_models import EducationOutput

def get_education_chain():
    """Build the chain that extracts education details."""
    parser = PydanticOutputParser(pydantic_object=EducationOutput)
    edu_format = parser.get_format_instructions()

    prompt = PromptTemplate(
    template="""
Extract education details.

{format_instructions}

Text:
{text}
""",
    input_variables=["text"],
    partial_variables={"format_instructions": edu_format}
)

    return prompt | get_llm() | parser
