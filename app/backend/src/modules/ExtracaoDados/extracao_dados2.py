import ezdxf
from ezdxf.addons import odafc
import pandas as pd
import logging
import math

# ==============================
# CONFIGURAÇÃO
# ==============================

logging.basicConfig(level=logging.INFO)

ODA_PATH = r"C:\Program Files\ODA\ODAFileConverter 27.1.0\ODAFileConverter.exe"
ezdxf.options.set("odafc-addon", "win_exec_path", ODA_PATH)

MAP_LAYER = {
    "EL_TOMADAS": "tomada",
    "EL_ILUMINACAO": "luminaria",
}

# ==============================
# CONVERSÃO DWG → DXF
# ==============================

def carregar_arquivo(caminho):
    try:
        logging.info(f"Carregando arquivo: {caminho}")
        return odafc.readfile(caminho)
    except Exception as e:
        logging.error(f"Erro ao abrir arquivo: {e}")
        return None

# ==============================
# CLASSIFICAÇÃO SEMÂNTICA
# ==============================

def classificar_entidade(entity):
    layer = entity.dxf.layer.upper()
    tipo_base = MAP_LAYER.get(layer, "desconhecido")

    return tipo_base

# ==============================
# EXTRAÇÃO GEOMÉTRICA
# ==============================

def calcular_comprimento(entity):
    tipo = entity.dxftype()
    
    try:
        if tipo == 'LINE':
            return (entity.dxf.start - entity.dxf.end).magnitude

        elif tipo == 'LWPOLYLINE':
            pontos = list(entity.get_points())
            if len(pontos) < 2:
                return None

            comprimento = 0
            for i in range(len(pontos) - 1):
                x1, y1 = pontos[i][0], pontos[i][1]
                x2, y2 = pontos[i + 1][0], pontos[i + 1][1]
                comprimento += math.hypot(x2 - x1, y2 - y1)

            return comprimento

        elif tipo == 'POLYLINE':
            pontos = [v.dxf.location for v in entity.vertices]
            if len(pontos) < 2:
                return None

            return sum(
                (pontos[i] - pontos[i + 1]).magnitude
                for i in range(len(pontos) - 1)
            )

        elif tipo == 'ARC':
            raio = entity.dxf.radius
            ang = math.radians(entity.dxf.end_angle - entity.dxf.start_angle)
            if ang < 0:
                ang += 2 * math.pi
            return raio * ang

        # 🔴 NOVO: tratar círculo
        elif tipo == 'CIRCLE':
            return 2 * math.pi * entity.dxf.radius

        # 🔴 NOVO: tratar spline (aproximação)
        elif tipo == 'SPLINE':
            pontos = list(entity.approximate(10))
            comprimento = 0
            for i in range(len(pontos) - 1):
                comprimento += (pontos[i] - pontos[i + 1]).magnitude
            return comprimento

        else:
            logging.warning(f"Tipo não suportado: {tipo}")
            return None

    except Exception as e:
        logging.warning(f"Erro ao calcular comprimento ({tipo}): {e}")
        return None

# ==============================
# PARSER PRINCIPAL
# ==============================

def extrair_entidades(doc):
    msp = doc.modelspace()
    resultados = []

    for entity in msp:
        try:
            tipo = entity.dxftype()

            dados = {
                "Layer": entity.dxf.layer,
                "Tipo_Entidade": tipo,
                "Handle": entity.dxf.handle,
                "Categoria": classificar_entidade(entity),
                "Quantidade": 1,
                "Unidade": "un",
                "Descricao": None
            }

            # ======================
            # BLOCOS
            # ======================
            if tipo == "INSERT":
                dados["Descricao"] = entity.dxf.name

                if entity.attribs:
                    atributos = ", ".join(
                        f"{a.dxf.tag}:{a.dxf.text}" for a in entity.attribs
                    )
                    dados["Descricao"] += f" ({atributos})"

            # ======================
            # ELEMENTOS LINEARES
            # ======================
            elif tipo in ['LINE', 'LWPOLYLINE', 'POLYLINE', 'ARC']:
                comprimento = calcular_comprimento(entity)

                if comprimento:
                    dados["Quantidade"] = round(comprimento, 2)
                    dados["Unidade"] = "m"
                    dados["Descricao"] = f"{tipo}_linear"
                else:
                    logging.warning(f"Falha comprimento entidade {entity.dxf.handle}")
                    continue

            # ======================
            # HATCH (ÁREA)
            # ======================
            elif tipo == "HATCH":
                dados["Descricao"] = "area_hatch"
                dados["Unidade"] = "m²"

                try:
                    if hasattr(entity, "area"):
                        dados["Quantidade"] = round(entity.area, 2)
                except:
                    logging.warning("Hatch sem área válida")

            else:
                continue

            resultados.append(dados)

        except Exception as e:
            logging.error(f"Erro ao processar entidade: {e}")

    return resultados

# ==============================
# PIPELINE COMPLETO
# ==============================

def processar_arquivo(caminho):
    doc = carregar_arquivo(caminho)

    if not doc:
        return None

    entidades = extrair_entidades(doc)

    if not entidades:
        logging.warning("Nenhuma entidade encontrada.")
        return None

    df = pd.DataFrame(entidades)

    resumo = (
        df.groupby(["Categoria", "Descricao", "Unidade"])
        .agg({"Quantidade": "sum"})
        .reset_index()
    )

    return resumo

# ==============================
# EXECUÇÃO
# ==============================

if __name__ == "__main__":
    caminho = "C:/Users/faelb/OneDrive/Desktop/EchoCAD/EchoCAD/app/backend/tests/ExtracaoDados/teste.dwg"

    resultado = processar_arquivo(caminho)

    if resultado is not None:
        print("\n--- RESUMO ---")
        print(resultado)

        resultado.to_html("saida.html", index=False)
        print("Arquivo HTML gerado com sucesso.")