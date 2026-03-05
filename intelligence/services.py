import openai
import os
from django.conf import settings
from pypdf import PdfReader
from docx import Document

# 1. Text Extraction Utilities
def extract_text_from_file(material):
    """
    Reads the file from Cloudinary (or local) and extracts text.
    """
    file_path = material.file.path
    text = ""
    
    try:
        if file_path.endswith('.pdf'):
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
    except Exception as e:
        print(f"Error extracting text: {e}")
        return "Error reading file."
        
    return text

# 2. The AI Generator
class LessonPlanGenerator:
    def __init__(self, substrand_id, material_id=None):
        from curriculum.models import SubStrand
        from resources.models import Material
        
        self.substrand = SubStrand.objects.get(id=substrand_id)
        self.material = Material.objects.get(id=material_id) if material_id else None
        
        # Load API Key from environment variables
        openai.api_key = os.environ.get('OPENAI_API_KEY')

    def generate(self):
        # A. Prepare Context
        outcomes_list = [o.description for o in self.substrand.outcomes.all()]
        context = f"""
        Strand: {self.substrand.strand.name}
        Sub-Strand: {self.substrand.name}
        Specific Learning Outcomes: {', '.join(outcomes_list)}
        """

        reference_content = ""
        if self.material:
            print("Extracting text from material...")
            reference_content = extract_text_from_file(self.material)
            context += f"\nReference Material Content:\n{reference_content[:3000]}" # Limit to 3000 chars to save tokens

        # B. Construct the Prompt
        system_prompt = "You are an expert teacher specializing in the Competency-Based Curriculum (CBC). Create a structured lesson plan in JSON format."
        
        user_prompt = f"""
        Based on the following curriculum details:
        {context}
        
        Generate a lesson plan. Return ONLY valid JSON with this structure:
        {{
            "title": "Creative Lesson Title",
            "objectives": ["Objective 1", "Objective 2"],
            "core_competencies": ["Communication", "Critical Thinking"],
            "learning_activities": [
                {{"step": 1, "activity": "Introduction...", "duration": "10 mins"}},
                {{"step": 2, "activity": "Main activity...", "duration": "30 mins"}}
            ],
            "assessment": "Description of how to assess learning",
            "resources": ["Chalkboard", "Charts"]
        }}
        """

        # C. Call OpenAI
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", # Or gpt-4 if you have access
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            
            # D. Parse Response
            content = response.choices[0].message['content']
            # Note: In production, you should use json.loads() here to validate it's valid JSON
            # But for now, we return it raw or parsed.
            
            return {
                "success": True,
                "data": content,
                "title": f"Lesson Plan: {self.substrand.name}"
            }

        except Exception as e:
            print(f"OpenAI Error: {e}")
            return {
                "success": False,
                "error": str(e)
            }