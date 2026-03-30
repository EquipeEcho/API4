import requests
import json
import re
import json


class LLMClassifier:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"

    def classificar(self, nome, layer, texto, tipo_entidade):
        prompt = f"""
        Você é um classificador de elementos de projetos CAD.

        Classifique em UMA das categorias:
        - parede
        - cotas
        - cobertura
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
                "model": "qwen2.5:3b",
                "prompt": prompt,
                "stream": False
            })

            resposta = response.json()["response"]
            data = extrair_json(resposta)
            print(f"Resposta do LLM: {data}")
            return data.get("tipo", "desconhecido"), data.get("confianca", 0.0)

        except:
            return "desconhecido", 0.0


def extrair_json(resposta):
    try:
        # pega o primeiro bloco JSON da string
        match = re.search(r'\{.*\}', resposta, re.DOTALL)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)
    except:
        pass

    return None


def heuristica(elemento):
    nome = elemento["nome"].upper()

    if "TOM" in nome:
        return "tomada", 0.95
    if "LUM" in nome:
        return "luminaria", 0.95

    return None
