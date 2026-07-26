# Separador de PDF

Sistema desenvolvido para automatizar a separação e organização de arquivos utilizados no projeto da PRF.

---

# Como o sistema funciona

O programa realiza:

* Leitura dos arquivos de entrada
* Processamento e separação automática dos dados
* Organização dos arquivos em pastas específicas
* Geração dos arquivos finais tratados

Fluxo básico:

1. O usuário inserem os arquivos necessários em arquivo pdf
2. O sistema lê os arquivos automaticamente
3. Os dados são processados
4. Os resultados são gerados nas pastas de saída escolhida pelo usuário

---

# Estrutura do projeto

```bash
projeto/
│
├── config/
│   ├── agua.xlsx
│   └── energia.xlsx
│
├── output/
├── src/
├── main.py
└── README.md
```

---

# Instalação

## 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

## 2. Entrar na pasta do projeto

```bash
cd SIAE
```

## 3. Criar ambiente virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

# Instalar dependências

```bash
pip install -r requirements.txt
```

---

# Como executar

```bash
python main.py
```

## 4. Caso preferir pode instalar como programa nativo windows, seguindo o passo a passo: 

Dentro da pasta instalador há um arquivo chamado SIAE_Setup_v1.5.exe.

Execute esse arquivo e siga o processo de instalação para instalar o programa nativamente no Windows.

Etapas:

Click na pasta instalador
Execute o arquivo SIAE_Setup_v1.5.exe
Avançar pelas etapas do instalador
Finalizar instalação
Abrir o sistema pelo atalho criado automaticamente na área de trabalho

# Tecnologias utilizadas

* Python
* Pandas
* OpenPyXL
* Git
* VS Code
* inno setup
