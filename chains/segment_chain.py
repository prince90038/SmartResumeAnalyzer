from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from config import get_llm
from schemas.pydantic_models import ResumeSections

def get_segment_chain():
    parser = PydanticOutputParser(pydantic_object=ResumeSections)
    format_instructions = parser.get_format_instructions()

    prompt = PromptTemplate(
        template="""
Split resume into sections.

{format_instructions}

Resume:
{text}
""",
        input_variables=["text"],
        partial_variables={"format_instructions": format_instructions}
    )

    return prompt | get_llm() | parser
