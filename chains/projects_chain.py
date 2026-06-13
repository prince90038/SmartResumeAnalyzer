from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from config import get_llm
from schemas.pydantic_models import ProjectsOutput

def get_projects_chain():
    parser = PydanticOutputParser(pydantic_object=ProjectsOutput)
    proj_format = parser.get_format_instructions()

    prompt = PromptTemplate(
    template="""
Extract projects with name, description, technologies.

{format_instructions}

Text:
{text}
""",
    input_variables=["text"],
    partial_variables={"format_instructions": proj_format}
)

    return prompt | get_llm() | parser
