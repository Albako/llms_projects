import requests
import re

def fetch_deepseek_response(question):
    deepseek_api_url = "http://127.0.0.1:1234/v1/chat/completions"
    payload = {
        "model": "deepseek-r1-distill-qwen-14b@q3_k_s", # tu trzeba wkleić dokładną nazwę używanego modelu
        "messages": [ 
        { "role": "system", "content": "Be logical and act as an expert." }, # jak ma coś robić
        { "role": "user", "content": question } # co ma robić
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
        


csv_file_path = "Health_Data.csv"
try:
    with open(csv_file_path, "r") as file:
        csv_content = file.read()
except FileNotFoundError:
    print("Error: Missing File")
    
question = f"Analyze the below health data: {csv_content}. Please give me a health report and suggest an action"
answer = fetch_deepseek_response(question)
print(answer)
