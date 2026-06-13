from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from config import get_llm
from schemas.pydantic_models import ExperienceMatch


def get_experience_match_chain():
    parser = PydanticOutputParser(pydantic_object=ExperienceMatch)
    fmt = parser.get_format_instructions()

    prompt = PromptTemplate(
        template="""
Evaluate how well the candidate's experience matches the job.

{format_instructions}

Job Responsibilities:
{jd}

Candidate Experience:
{exp}
""",
        input_variables=["jd", "exp"],
        partial_variables={"format_instructions": fmt}
    )

    return prompt | get_llm() | parser


def match_experience(jd_responsibilities, experience_list):
    exp_text = " ".join([e.get("description", "") for e in experience_list])

    chain = get_experience_match_chain()

    return chain.invoke({
        "jd": "\n".join(jd_responsibilities),
        "exp": exp_text
    })
