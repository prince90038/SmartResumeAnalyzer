"""Generate resume improvement suggestions from gaps and job requirements."""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from config import get_llm
from schemas.pydantic_models import SuggestionOutput


def get_suggestion_chain():
    """Build the chain that turns analysis gaps into actionable suggestions."""
    parser = PydanticOutputParser(pydantic_object=SuggestionOutput)

    prompt = PromptTemplate(
        template="""
You are a hiring expert.

Generate actionable suggestions based on gaps.

STRICT RULES:
- No generic advice
- Suggestions must be specific
- Focus on improving resume for this JD

{format_instructions}

Job Description:
{jd}

Missing Skills:
{missing}

Partial Skills:
{partial}

Resume Skills:
{skills}
""",
        input_variables=["jd", "missing", "partial", "skills"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    return prompt | get_llm() | parser


def generate_suggestions(jd_json, resume_json, gap_data):
    """Invoke the suggestion chain with job, resume, and gap context."""
    chain = get_suggestion_chain()

    return chain.invoke({
        "jd": "\n".join(jd_json.get("responsibilities", [])),
        "missing": ", ".join(gap_data["critical_gaps"]),
        "partial": ", ".join(gap_data["secondary_gaps"]),
        "skills": ", ".join(resume_json.get("skills", []))
    })
