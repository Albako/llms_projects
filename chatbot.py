import re
import requests

def deepseek_chatbot():
    messages = [ 
            { "role": "system", "content": "Be logical and act as an expert." },
            ]
    while True:
        
        deepseek_api_url = "http://127.0.0.1:1234/v1/chat/completions"
        question = input("You: ").strip()
        if question.lower() in ["exit","quit"]:
            print("Goodbye! Till the next time and may the force be with you!")
            break
        messages.append({"role":"user","content":question})
        payload = {
            "model": "deepseek-r1-distill-qwen-14b@q3_k_s", # tu trzeba wkleić dokładną nazwę używanego modelu
            "messages": messages, 
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
            #return filtered_answer
            print(f"DeepSeek: {filtered_answer}")
            
deepseek_chatbot()