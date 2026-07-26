import re

def extrair_codigo(texto):

    encontrados = re.findall(r'[\d\.\-\s]{7,}', texto)

    codigos = []

    for item in encontrados:
        numero = re.sub(r'\D', '', item)

        if len(numero) >= 7:
            codigos.append(numero)

    return codigos


def extrair_mes_ano(texto):

    match = re.search(r'Vencimento.*?(\d{2})/(\d{2})/(\d{4})', texto, re.IGNORECASE)

    if not match:
        match = re.search(r'(\d{2})/(\d{2})/(\d{4})', texto)

    if match:
        mes_num = int(match.group(2))
        ano = match.group(3)

        meses = [
            "Janeiro","Fevereiro","Março","Abril","Maio","Junho",
            "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"
        ]

        return meses[mes_num - 1], ano

    return "MesDesconhecido", "AnoDesconhecido"