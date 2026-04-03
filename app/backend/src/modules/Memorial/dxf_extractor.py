# modulo de extração de dados de arquivos dxf

import logging
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from ezdxf.document import Drawing
from ezdxf.filemanagement import readfile

from modules.Memorial.IA_config import classificar


logger = logging.getLogger(__name__)

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
    tipo: str = "parede"  
    dimensoes: Dimensoes = field(default_factory=Dimensoes)
    vao: Vao = field(default_factory=Vao)
    area_parede: float = 0
    area_liquida: float = 0
    custo_unitario: float = 0
    custo_total: float = 0

@dataclass
class ProjetoMemorial:
    nome_projeto: str
    ambientes: List[Ambiente]


class CADExtractor:
    def __init__(self, file_path: str):
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

        elif tipo in ["ARC", "CIRCLE"]:
            return (entity.dxf.center.x, entity.dxf.center.y)

        elif tipo == "INSERT":
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

    def _load_file(self) -> Drawing | None:
        """Lê e retorna o arquivo DXF carregado na memória."""
        try:
            logging.info(f"Carregando arquivo: {self.file_path}")
            return readfile(self.file_path)
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
                if len(pontos) < 2:
                    return 0
                comprimento = 0
                for i in range(len(pontos) - 1):
                    x1, y1 = pontos[i][0], pontos[i][1]
                    x2, y2 = pontos[i + 1][0], pontos[i + 1][1]
                    comprimento += math.hypot(x2 - x1, y2 - y1)
                return comprimento
            elif tipo == 'ARC':
                raio = entity.dxf.radius
                ang = math.radians(entity.dxf.end_angle -
                                   entity.dxf.start_angle)
                if ang < 0:
                    ang += 2 * math.pi
                return raio * ang
            elif tipo == 'CIRCLE':
                return 2 * math.pi * entity.dxf.radius
            return 0
        except Exception as e:
            return 0

    def _normalizar_unidade(self, valor):
        if not valor:
            return 0

        # heurística simples (ajustável depois)
        if valor > 1000:
            return valor / 1000  # mm → m
        elif valor > 100:
            return valor / 100   # cm → m
        return valor

    def tipo_layer_identificado(self, layer):
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

        tipo = self.tipo_layer_identificado(layer)

        if tipo != "desconhecido":
            return tipo

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

        conf = classificar(
            nome=nome,
            layer=layer,
            texto=texto,
            tipo_entidade=entity.dxftype()
        )

        logging.info(f"Classificação IA: (confiança: {conf:.2f})")

    def extrair_dados_reais(self) -> List[Ambiente]:
        if not self.doc:
            return []
        msp = self.doc.modelspace()

        # 1. Identificar nomes de ambientes (TEXT/MTEXT nas layers mapeadas)
        ambientes_dict: Dict[str, Ambiente] = {}
        for entity in msp.query('TEXT MTEXT'):
            layer = entity.dxf.layer.upper()
            if MAP_LAYER.get(layer) == "ambiente_nome":
                nome = (entity.dxf.text if entity.dxftype() ==
                        'TEXT' else getattr(entity, 'TEXT', '')).strip()
                if nome and len(nome) > 2 and nome not in ambientes_dict:
                    # Limpar formatação MTEXT se houver
                    if '\\P' in nome:
                        nome = nome.split('\\P')[0]
                    centro_texto = self._get_centro_entidade(entity) or (0, 0)
                    ambientes_dict[nome] = Ambiente(
                        nome=nome, centro=centro_texto)

        if not ambientes_dict:
            ambientes_dict["Ambiente 1"] = Ambiente(nome="Ambiente 1")

        # 2. Agrupar medidas por tipo de layer
        ambientes_lista = list(ambientes_dict.values())

        for entity in msp:

            layer = entity.dxf.layer.upper()
            tipo_mapeado = self.classificar_elemento(entity)
            # logging.info(f"[CLASS] {layer} -> {tipo_mapeado} | {entity.dxftype()}")

            if tipo_mapeado == "desconhecido":
                continue

            if tipo_mapeado == "ignorar":
                continue

            centro = self._get_centro_entidade(entity)

            if not centro:
                continue

            ambiente = self._encontrar_ambiente_mais_proximo(
                centro, ambientes_lista)

            if not ambiente:
                continue

            if tipo_mapeado in ["parede", "hidro", "vao", "cobertura", "parede_leve", "laje"]:
                ambiente.tipo = tipo_mapeado

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

        for ambiente in ambientes_lista:
            # Normalizar valores por ambiente
            comprimento = self._normalizar_unidade(
                ambiente.dimensoes.comprimento or 0)
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
