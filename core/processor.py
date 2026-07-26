import os
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter

from core.pdf_reader import ler_pdf
from core.extractor import extrair_codigo, extrair_mes_ano
from core.renamer import gerar_nome
from core.detector import detectar_tipo_pdf

from utils.normalizer import normalizar_texto
from utils.validator import validar_nome_unidade


def normalizar_colunas(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


def limpar_codigo(valor):
    try:
        return str(int(float(valor)))
    except (ValueError, TypeError):
        return str(valor).strip()


# 🔥 NOVO: output_dir opcional
def processar(pdf_path, energia_path, agua_path, config, output_dir=None):

    # =========================
    # 1. DEFINIR PASTA DE SAÍDA
    # =========================
    if output_dir:
        pasta_saida = output_dir
    else:
        pasta_saida = config.get("pasta_saida", "output")

    os.makedirs(pasta_saida, exist_ok=True)

    # =========================
    # 2. LEITURA PDF
    # =========================
    paginas_texto, _ = ler_pdf(pdf_path)
    reader_pdf = PdfReader(pdf_path)

    if not paginas_texto:
        raise Exception("❌ O PDF está vazio ou não pôde ser lido.")

    # =========================
    # 3. DETECÇÃO DO TIPO
    # =========================
    tipo_pdf = detectar_tipo_pdf(paginas_texto[0])
    if tipo_pdf == "Desconhecido":
        raise Exception("❌ Tipo de PDF não identificado (Neoenergia/Compesa)")

    # =========================
    # 4. PLANILHAS
    # =========================
    mapa_energia = {}
    mapa_agua = {}

    if energia_path:
        df_energia = normalizar_colunas(pd.read_excel(energia_path))
        if "codigo_energia" in df_energia.columns:
            mapa_energia = {
                limpar_codigo(row['codigo_energia']): row['nome_unidade']
                for _, row in df_energia.iterrows()
            }

    if agua_path:
        df_agua = normalizar_colunas(pd.read_excel(agua_path))
        if "matricula_agua" in df_agua.columns:
            mapa_agua = {
                limpar_codigo(row['matricula_agua']): row['nome_unidade']
                for _, row in df_agua.iterrows()
            }

    # =========================
    # 5. PROCESSAMENTO
    # =========================
    arquivos = {}
    mes, ano = extrair_mes_ano(paginas_texto[0])

    for i, texto in enumerate(paginas_texto):
        print(f"\n--- PÁGINA {i} ---")

        codigos_encontrados = extrair_codigo(texto)
        unidade = None
        tipo = None

        for cod_pdf in codigos_encontrados:
            cod_pdf = cod_pdf.strip()

            if tipo_pdf == "Compesa":
                for mat_planilha, nome_unidade in mapa_agua.items():
                    if mat_planilha in cod_pdf:
                        unidade = nome_unidade
                        tipo = "Compesa"
                        break

            elif tipo_pdf == "Neoenergia":
                for cod_planilha, nome_unidade in mapa_energia.items():
                    if cod_planilha in cod_pdf:
                        unidade = nome_unidade
                        tipo = "Neoenergia"
                        break

            if unidade:
                break

        if unidade:
            valido, msg = validar_nome_unidade(unidade)
            if not valido:
                print(f"⚠ Aviso: {msg}")

            unidade_norm = normalizar_texto(unidade)
            nome_arquivo = gerar_nome(tipo, unidade_norm, mes, ano)

            if nome_arquivo not in arquivos:
                arquivos[nome_arquivo] = PdfWriter()

            arquivos[nome_arquivo].add_page(reader_pdf.pages[i])
            print(f"✅ Página {i} vinculada a: {unidade}")
        else:
            print(f"⚪ Página {i} ignorada")

    # =========================
    # 6. SALVAR PDFs
    # =========================
    for nome, writer in arquivos.items():
        caminho = os.path.join(pasta_saida, f"{nome}.pdf")
        with open(caminho, "wb") as f:
            writer.write(f)

    # =========================
    # 7. CONSOLIDADO
    # =========================
    writer_consolidado = PdfWriter()
    writer_consolidado.add_page(reader_pdf.pages[0])

    nome_consolidado = f"Fatura_{tipo_pdf}_CONSOLIDADA_{mes}_{ano}.pdf"
    caminho_consolidado = os.path.join(pasta_saida, nome_consolidado)

    with open(caminho_consolidado, "wb") as f:
        writer_consolidado.write(f)

    print(f"\n🚀 Concluído! {len(arquivos)} PDFs em: {pasta_saida}")

    return pasta_saida, tipo_pdf