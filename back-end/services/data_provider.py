from serpapi.google_search import GoogleSearch
import spacy
import json
from settings import settings
from collections import Counter

with open("skills.json", "r", encoding="utf-8") as f:
    SKILLS_CATEGORIES = json.load(f)
    SKILLS_DB = {
        skill.lower(): cat
        for cat, skills in SKILLS_CATEGORIES.items()
        for skill in skills
    }

nlp = {
    "en": spacy.load("en_core_web_sm"),
    "fr": spacy.load("fr_core_news_sm"),
}


class DataProvider:
    def __init__(self):
        self.api_key = settings.SERPAPI_API_KEY
        self.last_skills = None 
        if not self.api_key:
            raise ValueError("SerpAPI API key is not configurée.")
        print(f"[DEBUG] Clé API SerpAPI chargée: {self.api_key[:6]}******")

 
    def job_details(self, job_title, city, language="en", num_results=35):
        location = city.strip() if city else "Canada"
        print(f"\n[DIAGNOSTIC] Recherche SerpApi : '{job_title}' à '{location}' (langue={language})...")

        params = {
            "api_key": self.api_key,
            "engine": "google_jobs",
            "q": job_title,
            "location": location,
            "gl": "ca",
            "hl": language,
            "num": 20,
        }

        all_descriptions = self._fetch_all_results(params, num_results)

       
        if not all_descriptions.strip() and language == "fr":
            print("[DIAGNOSTIC] Aucun résultat en français, tentative en anglais...")
            params["hl"] = "en"
            all_descriptions = self._fetch_all_results(params, num_results)
        if not all_descriptions.strip():
            print("[DIAGNOSTIC] Aucun texte collecté depuis SerpApi.")
            return {}      
        skills = self._analyze_top_skills(all_descriptions, language, top_n=35)       
        self.last_skills = skills
        print("[INFO] Compétences sauvegardées pour réutilisation dans l’analyse.")
        return skills

    def _fetch_all_results(self, params, max_count):
        all_descriptions = []
        page = 1
        print("[DIAGNOSTIC] Lancement de la collecte d'annonces...")

        while len(all_descriptions) < max_count:
            print(f"[DIAGNOSTIC] Requête SerpApi - page {page}")
            search = GoogleSearch(params)
            results = search.get_dict()

            if "error" in results:
                print(f"[ERREUR SERPAPI] {results['error']}")
                break

            jobs = results.get("jobs_results", [])
            if not jobs:
                print("[DIAGNOSTIC] Aucune annonce trouvée, arrêt.")
                break

            all_descriptions.extend([job.get("description", "") for job in jobs])

            if len(all_descriptions) >= max_count:
                break

            next_page_token = results.get("serpapi_pagination", {}).get("next_page_token")
            if not next_page_token:
                break

            params["next_page_token"] = next_page_token
            page += 1

        full_text = " ".join(all_descriptions)
        print(f"[DIAGNOSTIC] Taille totale du texte collecté: {len(full_text)} caractères.")
        return full_text

  
    def _analyze_top_skills(self, all_descriptions, language, top_n=35):
        print(f"[DIAGNOSTIC] Début de l’analyse linguistique ({language})...")
        doc = nlp.get(language, nlp["en"])(all_descriptions)

        found_skills = []
        for token in doc:
            lemma = token.lemma_.lower()
            if lemma in SKILLS_DB:
                found_skills.append(lemma)

        freq = Counter(found_skills)
        most_common = [skill for skill, _ in freq.most_common(top_n * 2)]  
        print(f"[DIAGNOSTIC] {len(most_common)} compétences identifiées avant regroupement.")

        grouped_skills = self._group_skills_by_category(most_common)
        print(f"[DIAGNOSTIC] Regroupement terminé ({len(grouped_skills)} catégories trouvées).")

        
        MAX_TOTAL_SKILLS = 35
        MAX_PER_CATEGORY = 6

        cleaned_grouped = {}
        total_count = 0

        for cat, skills in grouped_skills.items():
            unique_skills = []
            for skill in skills:
                if (
                    skill not in unique_skills
                    and len(unique_skills) < MAX_PER_CATEGORY
                    and total_count < MAX_TOTAL_SKILLS
                ):
                    unique_skills.append(skill)
                    total_count += 1
            if unique_skills:
                cleaned_grouped[cat] = unique_skills

        print(f"[DIAGNOSTIC] {total_count} compétences finales après filtrage équilibré.")
        return cleaned_grouped

    def _group_skills_by_category(self, skills_list):
        grouped = {}
        for skill in skills_list:
            category = SKILLS_DB.get(skill, "other")
            grouped.setdefault(category, []).append(skill)
        return grouped
