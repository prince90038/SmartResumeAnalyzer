# SmartResumeAnalyzer

SmartResumeAnalyzer is a Streamlit app that uses Hugging Face models to extract resume content, analyze a job description, match skills and experience, and present an overall fit score with gaps and suggestions.

## Features

- Resume parsing from PDF
- Job description analysis and normalization
- Skill and experience matching
- Fit scoring with an overall decision label
- Gap analysis and improvement suggestions
- Streamlit dashboard for reviewing results

## Screenshots

### Upload Resume

![Upload Resume](images/upload_pdf.png)

### Overall Score

![Overall Score](images/overall_score.png)

### Experience Match

![Experience Match](images/experience_match.png)

### Gap Analysis

![Gap Analysis](images/gap_analysis.png)

### Skill Recommendations

![Skill Recommendations](images/skill_recommendations.png)

### Project Suggestions

![Project Suggestions](images/project_suggestions.png)

## Project Structure

- `main.py` - orchestration entry point
- `pipeline/` - resume and JD processing flows
- `matching/` - skill and experience matching helpers
- `scoring/` - score calculation logic
- `analysis/` - gap analysis and suggestion generation
- `ui/` - Streamlit application and components
- `utils/` - PDF loading, text cleanup, and validation helpers

## Prerequisites

- Python 3.11-3.13 recommended (Python 3.14 currently emits a LangChain compatibility warning)
- A virtual environment is recommended
- A Hugging Face access token for hosted inference, or enough local resources to run a Transformers model

## Setup

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:PYTHONPATH="."
Copy-Item .env.example .env
```

For hosted inference, set `HF_TOKEN` in `.env`. The default model is
`Qwen/Qwen2.5-7B-Instruct`, accessed through Hugging Face's conversational
chat API.

To run without an inference API, set `HF_BACKEND=local`. Local mode downloads
`Qwen/Qwen2.5-1.5B-Instruct` on first use and runs on CPU by default. Set
`HF_LOCAL_DEVICE=0` to use the first compatible GPU.

## Run the App

```powershell
streamlit run ui/app.py
```

The same pipeline can be run from the command line:

```powershell
python main.py data/input/resume.pdf data/input/jd.txt --output data/output/match.json
```

## Tests

```powershell
python -m unittest discover -s tests -v
```

## Usage

1. Upload a resume PDF.
2. Paste the job description.
3. Click Analyze.
4. Review the score, skill match, experience match, gaps, and suggestions.

## Notes

- Generated output files in `data/output/` are ignored from GitHub pushes.
- Uploaded resumes are written to unique temporary files and removed after analysis.
- Model selection and generation limits can be changed through the variables documented in `.env.example`.
