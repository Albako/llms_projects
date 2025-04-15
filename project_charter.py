import re
import requests
from Markdown2docx import Markdown2docx

def fetch_deepseek_response(app_idea):
    deepseek_api_url = "http://127.0.0.1:1234/v1/chat/completions"
    payload = {
        "model": "deepseek-r1-distill-qwen-14b@q3_k_s", # tu trzeba wkleić dokładną nazwę używanego modelu
        "messages": [ 
        { "role": "system", "content": "Act as a project architekt." }, # jak ma coś robić
        { "role": "user", "content": f"""
         Generate a project charter for the following app idea: {app_idea}. 
         Please include the following sections:
         1. Project Title
         2. Project Purpose or Justification – a clear explanation of why the project is being undertaken and the problem/opportunity it addresses.
         3. Objectives and Success Criteria – define SMART objectives and specify how success will be measured.
         4. Scope Description – detail what is in scope and what is explicitly out of scope.
         5. High-Level Requirements – outline the major deliverables or functionalities needed.
         6. Milestones – list key project phases or delivery points with estimated dates.
         7. Budget Summary – a high-level estimate of project costs and funding source.
         8. Risks and Assumptions – identify initial risks, constraints, and key assumptions.
         9. Key Stakeholders – list individuals or groups with interest in the project, and their roles.
         10. Project Manager and Authority Level – name the PM and describe their decision-making power.
         11. Approval and Sign-off Section – a space for executive sponsors or key stakeholders to formally approve the charter.
         """} # co ma robić
        ], 
        "temperature": 0.1, # od 0 do 2 - od 0 do 0.3 bardzo dokładnie
        "max_tokens": -1, # -1 usuwa limit maksymalnych "tokenów"
        "stream": False
    
    }

    response = requests.post(deepseek_api_url, json=payload)

    if response.status_code == 200:
        generated_response = response.json()
        answer = generated_response.get("choices")[0].get("message").get("content")
        # .get() or response["choices"]
        filtered_answer = re.sub(r"<think>.*</think>","",answer,flags=re.DOTALL).strip()
        # usuwa proces myślowy (thinking process of a LLM)
        return filtered_answer
    else:
        return None

def generate(app_idea):
    
    project_charter_text = fetch_deepseek_response(app_idea)
    if project_charter_text:
        with open("project_charter.md", "w", encoding="utf-8") as file:
            file.write(project_charter_text)
    # converting the markdown file into a word document
        word_file = Markdown2docx('project_charter')
        word_file.eat_soup()
        word_file.save()
        print("Project charter has been saved succesfully!")
        return project_charter_text
    else:
        print("An error occured during project charter generation.")
        return None