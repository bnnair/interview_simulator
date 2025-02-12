import openai


def enhance_resume(resume_text: str) -> str:
    prompt = f"""
    Transform this resume into a professional format with the following improvements:
    1. Optimize action verbs and industry-specific keywords
    2. Improve readability with clear sections (Experience, Education, Skills)
    3. Add missing professional summary if needed
    4. Maintain factual accuracy while enhancing language
    5. Make sure that the enhanced resume adheres to the following format:
        a. name: str
        b. contact_info: str
        c. summary: str
        d. experiences: List[Experience]
        e. education: List[Education]
        f. skills: List[Skill]
        g. certifications: Optional[List[Certification]] = None
    
    Resume: {resume_text[:3000]}
    """
    return openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content