import ezdxf
import os
import logging
import math
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from IA_config import *

# ==============================
# CONFIGURAÇÃO E LOGGING
# ==============================
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Mapeamento de Layers REAIS (Baseado no teste.dxf)
MAP_LAYER = {
    "ARQ - ALVENARIA ALTA": "parede",
    "ARQUITETÔNICO - ALVENARIA ALTA": "parede",
    "ARQ - ALVENARIA MÉDIA-BAIXA": "parede",
    "ARQ - ESQUADRIAS": "vao",
    "ARQ - ALVENARIA (-)": "parede",
    "ESQUADRIAS": "vao",
    "ARQ - TEXTOS": "ambiente_nome",
    "ARQUITETÔNICO - TEXTOS": "ambiente_nome",
    "ESTRUTURAL - PILARES": "pilar",
    "ESTRUTURAL - VIGAS": "viga",
    "ESTRUTURAL - LAJES": "laje",
    "HIDROSSANITÁRIO - ÁGUA FRIA": "hidro",
    "HIDROSSANITÁRIO - ESGOTO": "hidro",
    "HIDROSSANITÁRIO - VENTILAÇÃO": "hidro",
    "ARQ - COBERTURA": "cobertura",
    "ARQ - DRY-WALL": "parede_leve",
    "BASE": "base"
}

# ==============================
# MODELOS DE DADOS (MEMORIAL)
# ==============================
@dataclass
class Dimensoes:
    comprimento: Optional[float] = None
    largura: Optional[float] = None
    altura: Optional[float] = 3.0  # Altura padrão (pé-direito)
    espessura: Optional[float] = 0.15

@dataclass
class Vao:
    tipo: Optional[str] = None
    comprimento: Optional[float] = None
    altura: Optional[float] = 2.1
    espessura: Optional[float] = 0.15

@dataclass
class AlvenariaAdicional:
    tipo: Optional[str] = None
    comprimento: Optional[float] = None
    altura: Optional[float] = None
    espessura: Optional[float] = None

@dataclass
class Ambiente:
    nome: str
    centro: tuple = (0, 0)
    dimensoes: Dimensoes = field(default_factory=Dimensoes)
    vao: Vao = field(default_factory=Vao)
    area_parede: float = 0
    area_liquida: float = 0

@dataclass
class ProjetoMemorial:
    nome_projeto: str
    ambientes: List[Ambiente]

# ==============================
# EXTRAÇÃO CAD
# ==============================
class CADExtractor:
    def __init__(self, file_path: str):
        self.classifier = LLMClassifier()
        self.file_path = file_path
        self.doc = self._load_file()

    def _get_centro_entidade(self, entity):
        tipo = entity.dxftype()

        if tipo == "LINE":
            x = (entity.dxf.start.x + entity.dxf.end.x) / 2
            y = (entity.dxf.start.y + entity.dxf.end.y) / 2
            return (x, y)

        elif tipo == "LWPOLYLINE":
            pontos = list(entity.get_points())
            xs = [p[0] for p in pontos]
            ys = [p[1] for p in pontos]
            return (sum(xs)/len(xs), sum(ys)/len(ys))

        elif tipo in ["TEXT", "MTEXT"]:
            return (entity.dxf.insert.x, entity.dxf.insert.y)

        return None

    def _distancia(self, p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
    
    def _encontrar_ambiente_mais_proximo(self, ponto, ambientes):
        menor_dist = float("inf")
        ambiente_escolhido = None

        for amb in ambientes:
            dist = self._distancia(ponto, amb.centro)
            if dist < menor_dist:
                menor_dist = dist
                ambiente_escolhido = amb

        return ambiente_escolhido

    def _load_file(self):
        try:
            logging.info(f"Carregando arquivo: {self.file_path}")
            return ezdxf.readfile(self.file_path)
        except Exception as e:
            logging.error(f"Erro ao abrir arquivo CAD: {e}")
            return None

    def _calcular_comprimento(self, entity):
        tipo = entity.dxftype()
        try:
            if tipo == 'LINE':
                return (entity.dxf.start - entity.dxf.end).magnitude
            elif tipo == 'LWPOLYLINE':
                pontos = list(entity.get_points())
                if len(pontos) < 2: return 0
                comprimento = 0
                for i in range(len(pontos) - 1):
                    x1, y1 = pontos[i][0], pontos[i][1]
                    x2, y2 = pontos[i + 1][0], pontos[i + 1][1]
                    comprimento += math.hypot(x2 - x1, y2 - y1)
                return comprimento
            elif tipo == 'ARC':
                raio = entity.dxf.radius
                ang = math.radians(entity.dxf.end_angle - entity.dxf.start_angle)
                if ang < 0: ang += 2 * math.pi
                return raio * ang
            elif tipo == 'CIRCLE':
                return 2 * math.pi * entity.dxf.radius
            return 0
        except Exception as e:
            return 0
        

        
    """def deve_ignorar_layer(layer):
        layer = layer.upper()

        #Alguns desses elementos nós vamos ingnorar por enquanto, pois não são relevantes para o memorial de cálculo estrutural atual.

        if "SIMBOLO" in layer:
            return True
        if "QUADRO" in layer:
            return True
        if "DETALHE" in layer:
            return True
        if "MOBILIÁRIO" in layer:
            return True
        if "DESNÍVEL" in layer:
            return True
        if "COTAS" in layer:
            return True
        if "COTA" in layer:
            return True
        if "CERCAMENTOS" in layer:
            return True
        if "CALÇADAS" in layer:
            return True
        if "CONTRA INCÊNDIO" in layer:
            return True
        if "TELEFONIA" in layer:
            return True
        if "DRENAGEM" in layer:             
            return True
        if "BAR" in layer:
            return True
        if "ESTRUTURAL - FUNDAÇÕES" in layer:
            return True 

        return False"""
    
    def _normalizar_unidade(self, valor):
        if not valor:
            return 0

        # heurística simples (ajustável depois)
        if valor > 1000:
            return valor / 1000  # mm → m
        elif valor > 100:
            return valor / 100   # cm → m
        return valor
    
    def tipo_layer_identificado(layer):
        layer = layer.upper()

        if "HIDROSSANITÁRIO" in layer:
            return "hidro"
        if "COBERTURA" in layer:
            return "cobertura"
        if "ELÉTRICA" in layer:
            return "eletrica"
        if "SÍMBOLOS" in layer or "SÍMBOLO" in layer:
            return "simbolo"
        if "DRY-WALL" in layer:
            return "parede_leve"
        if "ALVENARIA" in layer:
            return "parede"
        if "COTAS" in layer or "COTA" in layer:
            return "cota"
        if "ESQUADRIAS" in layer:
            return "vao"
        if "DESNÍVEL" in layer:
            return "desnivel"
        if "PROJEÇÔES" in layer:
            return "projecao"
        if "CIRCUITO" in layer:
            return "eletrica"
        
        return "desconhecido"
        
        
    
    def classificar_elemento(self, entity):
        layer = entity.dxf.layer.upper()

        LAYERS_IGNORADOS = {"DEFPOINTS", "0", "035"}

        if layer in LAYERS_IGNORADOS:
            return "ignorar"
        
        if CADExtractor.tipo_layer_identificado(layer) != "desconhecido":
            return CADExtractor.tipo_layer_identificado(layer)
        
       # if CADExtractor.deve_ignorar_layer(layer):
        #    return "ignorar"
        
        if layer not in MAP_LAYER:
            return "ignorar"
        
        # Heurística 
        tipo = MAP_LAYER.get(layer)
        if tipo:
            return tipo

        # IA (fallback)
        nome = getattr(entity.dxf, "name", "")
        texto = ""

        if entity.dxftype() in ["TEXT", "MTEXT"]:
            texto = entity.dxf.text if entity.dxftype() == "TEXT" else entity.text

        tipo_llm, conf = self.classifier.classificar(
            nome=nome,
            layer=layer,
            texto=texto,
            tipo_entidade=entity.dxftype()
        )

        
        logging.info(f"Classificação IA: {tipo_llm} (confiança: {conf:.2f})")

        return tipo_llm


    def extrair_dados_reais(self) -> List[Ambiente]:
        if not self.doc: return []
        msp = self.doc.modelspace()
        self.classifier = LLMClassifier()
        
        # 1. Identificar nomes de ambientes (TEXT/MTEXT nas layers mapeadas)
        ambientes_dict: Dict[str, Ambiente] = {}
        for entity in msp.query('TEXT MTEXT'):
            layer = entity.dxf.layer.upper()
            if MAP_LAYER.get(layer) == "ambiente_nome":
                nome = (entity.dxf.text if entity.dxftype() == 'TEXT' else entity.text).strip()
                if nome and len(nome) > 2 and nome not in ambientes_dict:
                    # Limpar formatação MTEXT se houver
                    if '\\P' in nome: nome = nome.split('\\P')[0]
                    ambientes_dict[nome] = Ambiente(nome=nome)

        if not ambientes_dict:
            ambientes_dict["Ambiente 1"] = Ambiente(nome="Ambiente 1")

        # 2. Agrupar medidas por tipo de layer (Lógica simplificada para MVP)
        primeiro_ambiente = list(ambientes_dict.values())[0]
        ambientes_lista = list(ambientes_dict.values())

        pos = entity.dxf.insert
        ambientes_dict[nome] = Ambiente(
            nome=nome,
            centro=(pos.x, pos.y)
        )

        for entity in msp:
            
            
            layer = entity.dxf.layer.upper()
            tipo_mapeado = self.classificar_elemento(entity)
            centro = self._get_centro_entidade(entity)
            logging.info(f"[CLASS] {layer} -> {tipo_mapeado} | {entity.dxftype()}")

            if not centro:
                continue

            ambiente = self._encontrar_ambiente_mais_proximo(centro, ambientes_lista)

            if not ambiente:
                continue
            
            if tipo_mapeado == "desconhecido":
                continue
            
            if tipo_mapeado == "ignorar":
                continue

            if tipo_mapeado == "parede":
                comp = self._calcular_comprimento(entity)
                if not ambiente.dimensoes.comprimento:
                    ambiente.dimensoes.comprimento = 0
                ambiente.dimensoes.comprimento += comp
                
                
            elif tipo_mapeado == "vao":
                comp = self._calcular_comprimento(entity)
                if not ambiente.vao.comprimento:
                    ambiente.vao.comprimento = 0
                ambiente.vao.comprimento += comp
                ambiente.vao.tipo = "Esquadrias"

        ambiente = primeiro_ambiente

        # Normalizar valores
        comprimento = self._normalizar_unidade(ambiente.dimensoes.comprimento or 0)
        vao_comp = self._normalizar_unidade(ambiente.vao.comprimento or 0)

        altura = ambiente.dimensoes.altura or 3.0
        altura_vao = ambiente.vao.altura or 2.1

        # Cálculo de áreas
        area_parede = comprimento * altura
        area_vao = vao_comp * altura_vao

        ambiente.area_parede = round(area_parede, 2)
        ambiente.area_liquida = round(max(area_parede - area_vao, 0), 2)

        # Atualizar valores normalizados
        ambiente.dimensoes.comprimento = round(comprimento, 2)
        ambiente.vao.comprimento = round(vao_comp, 2)
            

        # Limitar para os primeiros 20 ambientes para caber no template
        
        return list(ambientes_dict.values())[:20]

    

# ==============================
# GERAÇÃO EXCEL
# ==============================
class LevantamentoCampoMapper:
    START_ROW = 8
    END_ROW = 27

    def __init__(self, worksheet: Worksheet):
        self.ws = worksheet

    def preencher_titulo_projeto(self, nome_projeto: str) -> None:
        self.ws["B1"] = nome_projeto

    def preencher_ambientes(self, ambientes: List[Ambiente]) -> None:
        for index, ambiente in enumerate(ambientes):
            row = self.START_ROW + index

            self.ws[f"B{row}"] = ambiente.nome
            self.ws[f"E{row}"] = ambiente.dimensoes.comprimento or 0
            self.ws[f"G{row}"] = ambiente.dimensoes.altura
            self.ws[f"H{row}"] = ambiente.dimensoes.espessura

            self.ws[f"J{row}"] = ambiente.vao.tipo
            self.ws[f"K{row}"] = ambiente.vao.comprimento or 0

            self.ws[f"L{row}"] = ambiente.area_parede
            self.ws[f"M{row}"] = ambiente.area_liquida

class MemorialGenerator:
    SHEET_NAME = "Levantamento Campo"

    def __init__(self, template_path: str):
        self.template_path = Path(template_path)

    def generate(self, projeto: ProjetoMemorial, output_path: str) -> Path:
        wb = load_workbook(self.template_path)
        ws = wb[self.SHEET_NAME]
        mapper = LevantamentoCampoMapper(ws)
        mapper.preencher_titulo_projeto(projeto.nome_projeto)
        mapper.preencher_ambientes(projeto.ambientes)
        
        out_p = Path(output_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        wb.save(out_p)
        return out_p

# ==============================
# EXECUÇÃO
# ==============================
def run_integration(dxf_file: str, template_file: str, output_file: str):
    print(f"Processando {os.path.basename(dxf_file)}...")
    
    extractor = CADExtractor(dxf_file)
    ambientes = extractor.extrair_dados_reais()
    
    nome_projeto = os.path.basename(dxf_file).replace(".dxf", "").title()
    projeto = ProjetoMemorial(nome_projeto=nome_projeto, ambientes=ambientes)
    
    generator = MemorialGenerator(template_file)
    arquivo_final = generator.generate(projeto, output_file)
    
    print(f"Sucesso! Memorial gerado em: {arquivo_final}")

if __name__ == "__main__":
    basepath = Path(__file__).parent
    DXF_INPUT = str(Path.joinpath(basepath, "test.dxf"))
    TEMPLATE = str(Path.joinpath(basepath,  "model_memorial.xlsx"))
    OUTPUT = str(Path.joinpath(basepath, 'memorial_prenchido.xlsx'))
    
    run_integration(DXF_INPUT, TEMPLATE, OUTPUT)
