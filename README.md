# PDFAI - Leitor Inteligente de PDFs

PDFAI é uma aplicação web desenvolvida com Streamlit que permite carregar, analisar e extrair informações de arquivos PDF de forma fácil e intuitiva.

![PDFAI Logo](https://via.placeholder.com/800x400?text=PDFAI+-+Leitor+Inteligente+de+PDFs)

## Funcionalidades

- ✅ **Extração de texto**: Converte documentos PDF em texto editável
- 🔍 **Análise de conteúdo**: Identifica palavras-chave e estatísticas do documento
- 📊 **Estatísticas detalhadas**: Contagem de caracteres, palavras e linhas
- 📝 **Resumo automático**: Gera resumos simples do conteúdo
- 🔎 **Busca avançada**: Procura termos específicos no documento
- 💾 **Download de dados**: Permite baixar o texto extraído

## Instalação

### Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

### Passos para Instalação

1. **Clone o repositório ou baixe os arquivos**:

   ```bash
   git clone https://github.com/seu-usuario/pdfai.git
   cd pdfai
   ```

2. **Crie um ambiente virtual (recomendado)**:

   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual**:

   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

   Se o arquivo requirements.txt não estiver disponível, instale as dependências manualmente:

   ```bash
   pip install streamlit pdfplumber pillow
   ```

## Uso

1. **Inicie a aplicação**:

   ```bash
   python -m streamlit run gui.py
   ```

2. **Acesse a interface web**:

   - A aplicação será aberta automaticamente em seu navegador padrão
   - Se não abrir, acesse: http://localhost:8501

3. **Upload de arquivos**:

   - Use a área de upload para selecionar e enviar um arquivo PDF
   - O sistema processará o arquivo automaticamente

4. **Explore as funcionalidades**:
   - Use as diferentes abas para acessar as análises e visualizações
   - Experimente a busca por termos específicos
   - Baixe o texto extraído para uso posterior

## Estrutura do Projeto

```
PDFAI/
├── gui.py             # Arquivo principal da aplicação
├── requirements.txt   # Dependências do projeto
└── utils/             # Módulos utilitários
    ├── __init__.py    # Torna o diretório um pacote Python
    └── extractor.py   # Funções para extração de texto
```

## Solução de Problemas

### Erro de importação do módulo extractor

Se você encontrar um erro como `ImportError: cannot import name 'extract_text_from_pdf'`, verifique:

1. Se o arquivo `extractor.py` existe no diretório `utils`
2. Se a função está definida corretamente no arquivo
3. Se todas as dependências estão instaladas: `pip install pdfplumber`

### O Streamlit não é reconhecido

Se o comando `streamlit` não for reconhecido, tente:

1. Usar `python -m streamlit run gui.py`
2. Verificar se o Streamlit está instalado: `pip show streamlit`
3. Reinstalar o Streamlit: `pip install streamlit`

## Limitações Atuais

- O resumo automático é uma implementação básica (usa apenas as primeiras frases);
- A extração de palavras-chave é baseada em frequência, não em relevância semântica;
- A detecção de seções do documento é experimental.

## Desenvolvimentos Futuros

- [ ] Integração com modelos de IA para resumos mais inteligentes
- [ ] Suporte para análise de documentos em vários idiomas
- [ ] Extração e análise de tabelas e imagens
- [ ] Comparação entre múltiplos documentos
