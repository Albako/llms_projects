import re
import requests
import markdown2

def fetch_deepseek_response(project_charter):
    deepseek_api_url = "http://127.0.0.1:1234/v1/chat/completions"
    payload = {
        "model": "deepseek-r1-distill-qwen-14b@q3_k_s", # tu trzeba wkleić dokładną nazwę używanego modelu
        "messages": [ 
        { "role": "system", "content": "Act as a IT risk analyst." }, # jak ma coś robić
        { "role": "user", "content": f"""
         Please genereta a risk management plan based opn my project charter: {project_charter}
         Please provide me with a markdown output with clearly labelled headings and sub-headings.
         Introduction – brief explanation of the purpose of the Risk Management Plan and its alignment with the project.
         Risk Management Approach – describe the methodology used (e.g., qualitative, quantitative, or both), tools, and frameworks to identify and manage risks.
         Roles and Responsibilities – define who is responsible for identifying, monitoring, responding to, and escalating risks.
         Risk Categories – use a Risk Breakdown Structure (RBS) if possible, or list categories like Technical, Schedule, Cost, External, Organizational, etc.
         Risk Identification – list key project-specific risks based on the charter, including:
         - Risk Description
         - Likelihood (Low/Medium/High)
         - Impact (Low/Medium/High)
         - Risk Owner
         Risk Analysis – provide a qualitative risk matrix (Probability × Impact), and optionally a quantitative analysis for critical risks.
         Risk Response Planning – define strategies (Avoid, Transfer, Mitigate, Accept) for each high or medium priority risk, with action steps.
         Risk Monitoring and Reporting – describe how risks will be tracked, reviewed, and updated throughout the project.
         Contingency and Fallback Plans – specify predefined plans for high-risk events if they materialize.
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

def generate(project_charter):
    
    risk_managment_text = fetch_deepseek_response(project_charter)
    if risk_managment_text:
        with open("project_charter.md", "w", encoding="utf-8") as file:
            file.write(risk_managment_text)
         # convert markdown to html    
        risk_management_html_text = markdown2.markdown(risk_managment_text, extras=["fenced-code-blocks", "tables"])
        with open("risk_management.html", "w", encoding="utf-8") as file:
            file.write(risk_management_html_text)
        print("Risk management plan html file has been saved succesfully!")
        return risk_managment_text
    else:
        print("An error occured during risk management html file generation.")
        return None