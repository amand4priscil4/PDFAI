import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from utils.extractor import extract_text_from_pdf
import tempfile
import base64
from PIL import Image
import io
import re

# Configuração da página
st.set_page_config(
    page_title="PDF'S - Leitor Inteligente",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para adicionar CSS personalizado
def local_css():
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1E3A8A;
            margin-bottom: 1rem;
            text-align: center;
        }
        .sub-header {
            font-size: 1.5rem;
            font-weight: 600;
            color: #2563EB;
            margin: 1rem 0;
        }
        .card {
            padding: 1.5rem;
            border-radius: 0.5rem;
            background-color: #F3F4F6;
            margin-bottom: 1rem;
            border-left: 4px solid #3B82F6;
            color: #1F2937;
        }
        .info-text {
            color: #4B5563;
            font-size: 0.9rem;
        }
        /* Estilo específico para o sidebar */
        .sidebar .card {
            color: #1F2937;
        }
        .sidebar ul li, .sidebar ol li {
            color: #1F2937;
        }
        .highlight {
            background-color: #DBEAFE;
            padding: 0.2rem 0.4rem;
            border-radius: 0.2rem;
        }
        .stButton>button {
            background-color: #2563EB;
            color: white;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #1D4ED8;
            color: white;
        }
        .upload-section {
            text-align: center;
            padding: 2rem;
            border: 2px dashed #CBD5E1;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        .footer {
            text-align: center;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #E2E8F0;
            color: #64748B;
            font-size: 0.8rem;
        }
        .text-area-header {
            font-weight: 600;
            color: #1E3A8A;
            margin-bottom: 0.5rem;
        }
        .feature-section {
            margin-top: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

def add_logo():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <h1 style="color: #2563EB; font-weight: 800; font-size: 3rem;">PDF<span style="color: #1E3A8A;">AI</span></h1>
    </div>
    """, unsafe_allow_html=True)

def get_text_download_link(text):
    """Gera um link para download do texto extraído"""
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="texto_extraido.txt">Baixar texto extraído</a>'

def get_pdf_preview(pdf_path):
    """Retorna HTML para exibir uma prévia do PDF"""
    try:
        return f'<embed src="data:application/pdf;base64,{get_base64_encoded_bytes(pdf_path)}" width="100%" height="400" type="application/pdf">'
    except Exception as e:
        return f"Não foi possível gerar a prévia do PDF: {str(e)}"

def get_base64_encoded_bytes(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def extract_keywords(text):
    """Extrai palavras-chave do texto (implementação simples)"""
    words = re.findall(r'\b\w{4,}\b', text.lower())
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    
    # Filtrar palavras comuns em português
    common_words = ['para', 'como', 'este', 'esta', 'pelo', 'pela', 'isso', 'mais', 'todos', 'quando']
    filtered_count = {k: v for k, v in word_count.items() if k not in common_words}
    
    # Retornar as top palavras-chave
    return sorted(filtered_count.items(), key=lambda x: x[1], reverse=True)[:10]

def summarize_text(text, max_length=500):
    
    sentences = re.split(r'(?<=[.!?])\s+', text)
    if len(sentences) <= 3:
        return text[:max_length] + "..." if len(text) > max_length else text
    
    return ' '.join(sentences[:3]) + "..."

def main():
    local_css()
    add_logo()
    
    st.markdown('<h1 class="main-header">Leitor de PDF com Extração de dados</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<h2 class="sub-header">Sobre</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card sidebar">
            <p style="color: #1F2937;">Esta ferramenta ajuda você a:</p>
            <ul style="color: #1F2937;">
                <li>Extrair texto de arquivos PDF</li>
                <li>Identificar palavras-chave</li>
                <li>Gerar resumos automáticos</li>
                <li>Fazer análises básicas do conteúdo</li>
            </ul>
            <p class="info-text" style="color: #4B5563;">Desenvolvido com Streamlit e Python.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<h2 class="sub-header">Instruções</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card sidebar">
            <ol style="color: #1F2937;">
                <li>Faça upload de um arquivo PDF</li>
                <li>Aguarde o processamento</li>
                <li>Explore o texto extraído</li>
                <li>Use as ferramentas de análise disponíveis</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    # Área de upload
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Selecione um arquivo PDF para análise", type="pdf")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Se um arquivo foi enviado
    if uploaded_file:
        with st.spinner("Processando o PDF, aguarde um momento..."):
            # Salvar o arquivo temporariamente
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_path = temp_file.name
                temp_file.write(uploaded_file.read())
            
            # Extrair texto
            texto = extract_text_from_pdf(temp_path)
            
            # Resumo e análise
            resumo = summarize_text(texto)
            palavras_chave = extract_keywords(texto)
            
            # Layout com tabs para organizar o conteúdo
            tab1, tab2, tab3, tab4 = st.tabs(["📄 Prévia do PDF", "📝 Texto Extraído", "🔍 Análise", "📊 Estatísticas"])
            
            with tab1:
                st.markdown('<h3 class="text-area-header">Visualização do documento</h3>', unsafe_allow_html=True)
                st.markdown(get_pdf_preview(temp_path), unsafe_allow_html=True)
            
            with tab2:
                st.markdown('<h3 class="text-area-header">Texto Completo Extraído</h3>', unsafe_allow_html=True)
                st.text_area("", texto, height=400)
                st.markdown(get_text_download_link(texto), unsafe_allow_html=True)
                
                # Opções de filtro
                st.markdown('<div class="feature-section">', unsafe_allow_html=True)
                st.markdown('<h3 class="text-area-header">Filtros e Pesquisa</h3>', unsafe_allow_html=True)
                termo_busca = st.text_input("Buscar no texto:")
                if termo_busca:
                    st.markdown("### Resultados da busca:")
                    matches = re.finditer(termo_busca, texto, re.IGNORECASE)
                    for i, match in enumerate(matches):
                        start = max(0, match.start() - 50)
                        end = min(len(texto), match.end() + 50)
                        context = texto[start:end]
                        highlighted = context.replace(match.group(), f"<span class='highlight'>{match.group()}</span>")
                        st.markdown(f"**Ocorrência {i+1}:** ...{highlighted}...", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab3:
                st.markdown('<h3 class="text-area-header">Resumo Automático</h3>', unsafe_allow_html=True)
                st.markdown(f"<div class='card'>{resumo}</div>", unsafe_allow_html=True)
                
                st.markdown('<h3 class="text-area-header">Palavras-chave</h3>', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                
                with col1:
                    for palavra, frequencia in palavras_chave[:5]:
                        st.markdown(f"• {palavra}: {frequencia} ocorrências")
                
                with col2:
                    for palavra, frequencia in palavras_chave[5:]:
                        st.markdown(f"• {palavra}: {frequencia} ocorrências")
            
            with tab4:
                st.markdown('<h3 class="text-area-header">Estatísticas do documento</h3>', unsafe_allow_html=True)
                
                # Calcular estatísticas
                num_caracteres = len(texto)
                num_palavras = len(texto.split())
                num_linhas = len(texto.splitlines())
                
                # Exibir em colunas
                col1, col2, col3 = st.columns(3)
                col1.metric("Caracteres", num_caracteres)
                col2.metric("Palavras", num_palavras)
                col3.metric("Linhas", num_linhas)
                
                # Informações adicionais
                st.markdown('<h3 class="text-area-header">Estrutura do documento</h3>', unsafe_allow_html=True)
                
                # Detectar possíveis seções
                possiveis_secoes = re.findall(r'^[A-ZÀ-Ú][A-ZÀ-Ú\s]{0,30}$', texto, re.MULTILINE)
                if possiveis_secoes:
                    st.markdown("### Possíveis seções detectadas:")
                    for i, secao in enumerate(possiveis_secoes[:10]):
                        st.markdown(f"- {secao.strip()}")
                    if len(possiveis_secoes) > 10:
                        st.markdown(f"*...e mais {len(possiveis_secoes) - 10} seções*")
            
            # Remover arquivo temporário
            os.unlink(temp_path)
    else:
        # Exibir uma mensagem informativa quando nenhum arquivo for carregado
        st.markdown("""
        <div class="card">
            <h3 class="text-area-header">Tente algo como:</h3>
            <p>Faça upload de um arquivo PDF usando o seletor acima para começar.</p>
            <p>A ferramenta irá automaticamente:</p>
            <ul>
                <li>Extrair todo o texto do documento</li>
                <li>Gerar uma visualização prévia</li>
                <li>Identificar palavras-chave e padrões</li>
                <li>Criar um resumo automático</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>PDFAI - Leitor Inteligente de PDFs © 2025</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()