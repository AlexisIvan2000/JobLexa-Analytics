from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from services.data_provider import DataProvider
from services.uploader import Uploader
from services.analyzer import AnalyzerService
import os

router = APIRouter(
        prefix="/jobmatch", 
        tags=["JobMatch"])

data_provider = DataProvider()
uploader = Uploader()
analyzer = AnalyzerService()

@router.post("/skills")
async def get_job_skills(
    job_title: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
):
    try:
        language = "fr" if state.lower() in ("qc", "quebec", "québec") else "en"

        if not all([job_title, city, state]):
            raise HTTPException(
                status_code=400,
                detail="Veuillez remplir tous les champs : titre, ville et province.",
            )

        skills = data_provider.job_details(
            job_title=job_title, city=city, language=language, num_results=35
        )

        if not skills:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Aucune compétence trouvée."},
            )

        return {"success": True, "job_title": job_title, "skills": skills}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/analyze")
async def analyze_cv(
    file: UploadFile = File(...),
):
    try:
      
        if not data_provider.last_skills:
            raise HTTPException(
                status_code=400,
                detail="Aucune compétence n’a encore été extraite. Veuillez d’abord appeler /jobmatch/skills."
            )

       
        file_path, message = await uploader.upload_file(file)
        if not file_path:
            raise HTTPException(status_code=400, detail=message)

        
        file_type = file.filename.split(".")[-1].lower()
        resume_text = await analyzer.extract_text(file_path, file_type)

        
        result = await analyzer.get_match_score(resume_text, data_provider.last_skills, "Poste actuel")

     
        if os.path.exists(file_path):
            os.remove(file_path)

        return {
            "success": True,
            "message": "Analyse de CV effectuée avec succès.",
            "match_score": result.get("match_percentage", 0),
            "missing_skills": result.get("missing_skills", []),
            "suggestion": result.get("suggestion", "Aucune suggestion."),
            "skills_used": data_provider.last_skills
        }

    except Exception as e:
        if "file_path" in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))
