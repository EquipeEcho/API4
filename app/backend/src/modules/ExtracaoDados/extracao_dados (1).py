import ezdxf
from ezdxf.addons import odafc
import pandas as pd

# Configuração do ODA (Caminho do exe do ODA)
CAMINHO_ODA = r"C:\Program Files\ODA\ODAFileConverter 27.1.0\ODAFileConverter.exe"
ezdxf.options.set("odafc-addon", "win_exec_path", CAMINHO_ODA)


#dwg_path é o caminho do arquivo dwg que sera precessado
def extrair_dados_orcamento(dwg_path):
    try:
        doc = odafc.readfile(dwg_path)
    except Exception as e:
        print(f"Erro: {e}")
        return None

    msp = doc.modelspace()
    lista_materiais = []

    for entity in msp:
        # Dicionário base com dados de identificação
        dados = {
            'Layer': entity.dxf.layer,
            'Tipo_Entidade': entity.dxftype(),
            'Handle': entity.dxf.handle,
            'Quantidade': 1,  # Padrão para itens unitários
            'Unidade': 'un',
            'Descricao': ''
        }

        # 1. TRATAMENTO PARA BLOCOS (Insert) - Itens Unitários
        if entity.dxftype() == 'INSERT':
            dados['Descricao'] = entity.dxf.name
            # Se houver atributos no bloco (ex: marca, modelo), podemos pegar aqui
            if entity.has_attrib:
                attr_str = ", ".join([f"{a.dxf.tag}: {a.dxf.text}" for a in entity.attribs])
                dados['Descricao'] += f" ({attr_str})"

        # 2. TRATAMENTO PARA LINHAS / ARCOS - Materiais Lineares
        elif entity.dxftype() in ['LINE', 'ARC', 'POLYLINE', 'LWPOLYLINE']:
            try:
                # O ezdxf tem métodos prontos para calcular comprimento
                if entity.dxftype() == 'LINE':
                    comprimento = (entity.dxf.start - entity.dxf.end).magnitude
                else:
                    # Para polilinhas e arcos complexos
                    comprimento = entity.length() 
                
                dados['Quantidade'] = round(comprimento, 2)
                dados['Unidade'] = 'm'
                dados['Descricao'] = f"Segmento de {entity.dxftype()}"
            except:
                continue

        # 3. TRATAMENTO PARA ÁREAS (Hatch)
        elif entity.dxftype() == 'HATCH':
            # Nota: extrair área de hachura pode ser pesado dependendo do arquivo
            dados['Unidade'] = 'm²'
            dados['Descricao'] = "Área de revestimento/preenchimento"
            # Quantidade aqui exigiria entity.area (disponível se a hachura for associativa)

        # Filtrar atributos Nulos antes de adicionar
        dados_limpos = {k: v for k, v in dados.items() if v is not None}
        lista_materiais.append(dados_limpos)

    return pd.DataFrame(lista_materiais)

# --- EXECUÇÃO E AGRUPAMENTO ---
df_orcamento = extrair_dados_orcamento(r"C:\Users\faelb\OneDrive\Desktop\EchoCAD\EchoCAD\app\backend\tests\ExtracaoDados\teste.dwg")

if df_orcamento is not None:
    # Agrupar itens iguais para facilitar o orçamento
    # Isso soma os metros de tubos e conta as unidades de tomadas automaticamente
    resumo = df_orcamento.groupby(['Layer', 'Descricao', 'Unidade']).agg({
        'Quantidade': 'sum'
    }).reset_index()

    print("--- RESUMO PARA ORÇAMENTO ---")
    print(resumo)
    # Gerando o HTML com uma classe de estilo (opcional)
    html_string = resumo.to_html(classes='table table-striped', index=False)
    
    # Salvando no arquivo
    with open("visualizacao.html", "w", encoding="utf-8") as f:
        f.write(f'''
        <html>
            <head>
                <title>Resumo de Orçamento DWG</title>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
            </head>
            <body class="container mt-5">
                <h2>Relatório de Quantitativos - Projeto CAD</h2>
                {html_string}
            </body>
        </html>
        ''')
    
    print("Visualização gerada! Abra o arquivo 'visualizacao.html' no seu navegador.")
    # Depois é só abrir o arquivo visualizacao.html no Chrome/Edge
# Visualizar como JSON formatado se preferir
    print(resumo.to_json(orient='records', indent=4))