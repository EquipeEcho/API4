import requests
import json

class LLMClassifier:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"

    def classificar(self, nome, layer, texto, tipo_entidade):
        prompt = f"""
    Você é um classificador de elementos de projetos CAD.

    Classifique em UMA das categorias:
    - parede
    - mobiliário
    - vão
    - ambiente_nome
    - elétrica
    - hidro
    - estrutural
    - desconhecido

    Responda em JSON:
{{"tipo": "...", "confianca": 0.0}}

Elemento:
nome: {nome}
layer: {layer}
texto: {texto}
tipo: {tipo_entidade}
"""

        try:
            response = requests.post(self.url, json={
                "model": "llama3:8b",
                "prompt": prompt,
                "stream": False
            })

            resposta = response.json()["response"]
            data = json.loads(resposta)
            return data.get("tipo", "desconhecido"), data.get("confianca", 0.0)

        except:
            return "desconhecido", 0.0



def parse_resposta(resposta):
    try:
        data = json.loads(resposta)
        return data["tipo"], data["confianca"]
    except:
        return "desconhecido", 0.0
    

def heuristica(elemento):
    nome = elemento["nome"].upper()

    if "TOM" in nome:
        return "tomada", 0.95
    if "LUM" in nome:
        return "luminaria", 0.95

    return None

