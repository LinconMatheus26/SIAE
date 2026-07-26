import pdfplumber

def ler_pdf(caminho):

    paginas_texto = []

    with pdfplumber.open(caminho) as pdf:
        for page in pdf.pages:
            texto = page.extract_text()
            paginas_texto.append(texto if texto else "")

    return paginas_texto, None