import streamlit as st
import pandas as pd
import os
from src.ai_integration import gerar_resumo_e_sentimento
from src.data_parser import parse_whatsapp_chat
from src.analytics import (
    obter_total_mensagens, 
    obter_mensagens_por_participante, 
    obter_horarios_de_pico, 
    obter_frequencia_diaria
)

# Configuração inicial da página
st.set_page_config(page_title="WhatsApp AI Analytics", page_icon="📱", layout="wide")

st.title("📱 WhatsApp AI Analytics")
st.markdown("Faça o upload do seu arquivo **.txt** exportado do WhatsApp para gerar insights da conversa.")

# Componente de upload
arquivo_carregado = st.file_uploader("Escolha o arquivo de conversa", type=["txt"])

if arquivo_carregado is not None:
    # Salvando o arquivo temporariamente no disco para o nosso parser conseguir ler
    caminho_temp = "temp_chat.txt"
    with open(caminho_temp, "wb") as f:
        f.write(arquivo_carregado.getbuffer())
        
    try:
        # Processando os dados
        with st.spinner("Analisando mensagens..."):
            df = parse_whatsapp_chat(caminho_temp)
            
        st.success("Processamento concluído com sucesso!")
        
        # --- SEÇÃO DE ANALYTICS ---
        st.header("📊 Dashboard de Análise")
        
        # Dividindo a tela em duas colunas
        col1, col2 = st.columns(2)
        
        with col1:
            # Total de mensagens em um "card" de destaque
            total = obter_total_mensagens(df)
            st.metric(label="Total de Mensagens", value=total)
            
            st.subheader("Mensagens por Participante")
            df_participantes = obter_mensagens_por_participante(df)
            # st.dataframe cria uma tabela interativa ordenável
            st.dataframe(df_participantes, use_container_width=True, hide_index=True)
            
        with col2:
            st.subheader("🔥 Horários de Maior Atividade")
            df_pico = obter_horarios_de_pico(df)
            # O bar_chart do Streamlit precisa da coluna X como índice do DataFrame
            st.bar_chart(df_pico.set_index('Hora'), color="#25D366")
            
        # Linha inferior ocupando a largura total
        st.divider()
        st.subheader("📈 Frequência de Mensagens por Dia")
        df_freq = obter_frequencia_diaria(df)
        st.line_chart(df_freq.set_index('Data'), color="#128C7E")

        st.divider()
        st.header("🤖 Análise com Inteligência Artificial")

        if st.button("Gerar Resumo da Conversa"):
            with st.spinner("O Gemini está analisando os padrões da conversa..."):
                resposta_ia = gerar_resumo_e_sentimento(df)
                st.markdown(resposta_ia)
        
    finally:
        # Boas práticas: apagar o arquivo temporário após o uso para não acumular lixo
        if os.path.exists(caminho_temp):
            os.remove(caminho_temp)