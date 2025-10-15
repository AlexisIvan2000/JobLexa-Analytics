from io import StringIO
from openai import AsyncOpenAI
from settings import settings
import json
from pdfminer.high_level import extract_text_to_fp
from docx import Document
from typing import List, Dict, Any


class AnalyzerService:
    def __init__(self):
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OpenAI API key is not configured.")
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"

    async def extract_text_from_pdf(self, file_path: str) -> str:
        output_string = StringIO()
        with open(file_path, "rb") as file:
            extract_text_to_fp(file, output_string)
        return output_string.getvalue()

    async def extract_text_from_docx(self, file_path: str) -> str:
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    async def extract_text(self, file_path: str, file_type: str) -> str:
        extractors = {
            "pdf": self.extract_text_from_pdf,
            "docx": self.extract_text_from_docx,
        }
        if file_type not in extractors:
            raise ValueError(f"Unsupported file type. Use pdf or docx.")
        return await extractors[file_type](file_path)

    async def get_match_score(self, resume_text: str, required_skills: List[str], job_title: str) -> Dict[str, Any]:
        """Analyzes how well a resume matches a job description."""
        skills_formatted = "\n- " + "\n- ".join(required_skills)
        prompt = f"""
        You are a recruiter specialized in {job_title}.
        Evaluate this resume against the job's skill requirements.

        **Required skills:**
        {skills_formatted}

        **Resume:**
        {resume_text}

        Return a JSON object with:
        - match_percentage (int)
        - missing_skills (list)
        - suggestion (string)
        """

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an HR expert that returns valid JSON only."},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
            )

            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f" AI error: {e}")
            return {
                "match_percentage": 0,
                "missing_skills": ["AI parsing error"],
                "suggestion": "Could not process resume properly.",
            }                  