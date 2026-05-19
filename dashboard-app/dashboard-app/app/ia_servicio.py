import requests
import os

API_KEY =  os.getenv("API_KEY")
def analizar_ventas(data):
    prompt =f"""
        Analiza las ventas y enviame recomendaciones: {data}
    """
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
        },
        timeout= 10
    )
    result = response.json();
    # print(result)
    return result["choices"][0]["message"]["content"]
