import os
from dotenv import load_dotenv
from google import genai

# 1. Descobre o caminho absoluto para a pasta raiz do projeto
caminho_atual = os.path.dirname(os.path.abspath(__file__))
caminho_raiz = os.path.dirname(caminho_atual)
caminho_env = os.path.join(caminho_raiz, '.env')

# 2. Força a leitura do ficheiro .env no caminho exato
load_dotenv(caminho_env)

# 3. Extrai a chave
chave_api = os.getenv("GEMINI_API_KEY")

# 4. Trava de segurança para avisar se ainda estiver vazia
if not chave_api:
    raise ValueError(f"O Python não conseguiu ler a chave no ficheiro: {caminho_env}. Recrie o ficheiro .env no VS Code.")

# 5. Inicializa o cliente
client = genai.Client(api_key=chave_api)

def preparar_contexto_conversa(df, limite_linhas=150):
    """
    Transforma as linhas do DataFrame em texto legível para o LLM.
    Limitamos o número de linhas para não estourar o limite de tokens da API
    e focar no contexto mais recente.
    """
    # Pegamos as últimas mensagens (mais recentes) para a análise
    df_recente = df.tail(limite_linhas)
    
    texto_formatado = ""
    for _, linha in df_recente.iterrows():
        texto_formatado += f"[{linha['Data'].strftime('%d/%m/%Y')} {linha['Hora']}] {linha['Remetente']}: {linha['Mensagem']}\n"
        
    return texto_formatado

def gerar_resumo_e_sentimento(df):
    """
    Envia o texto da conversa para o Gemini 3.8 Flash e retorna a análise.
    Possui fallback (mocking) para limite de cota (429) ou indisponibilidade (503).
    """
    contexto = preparar_contexto_conversa(df)
    
    # Prática de Engenharia de Prompts: Dar um papel claro e instruções estruturadas
    prompt = f"""
    Você é um Engenheiro de Dados e IA analisando uma conversa de WhatsApp.
    Abaixo está um extrato recente dessa conversa.
    
    Analise o texto e retorne:
    1. **Resumo dos Assuntos**: Quais foram os tópicos principais discutidos?
    2. **Tom da Conversa**: Qual é o sentimento e o tom geral? (ex: profissional, amigável, tenso).
    3. **Padrão de Comunicação**: Existe algum padrão notável de interação entre os participantes?
    
    Por favor, seja objetivo e responda em formato Markdown estruturado.
    
    Conversa:
    {contexto}
    """
    
    try:
        # Chamada para o modelo otimizado
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        erro_str = str(e).upper()
        # Lógica de Fallback (Mock) para indisponibilidade (503) ou falta de cota (429)
        if "503" in erro_str or "UNAVAILABLE" in erro_str or "429" in erro_str or "RESOURCE_EXHAUSTED" in erro_str:
            return """
> ⚠️ **Aviso do Sistema:** Limite de uso da API atingido ou serviço temporariamente indisponível. Exibindo análise estrutural simulada para fins de demonstração da interface:

**1. Resumo dos Assuntos:**
* Alinhamento sobre ferramentas de desenvolvimento (Python, Streamlit).
* Resolução de bugs e configuração de chaves de API.
* Discussões sobre estruturação de dados.

**2. Tom da Conversa:**
* Colaborativo, técnico e focado em resolução de problemas. Ocasionalmente informal.

**3. Padrão de Comunicação:**
* Trocas rápidas de mensagens curtas. Concentração de respostas nos períodos da noite e madrugada.
            """
        
        # Para outros erros reais
        return f"⚠️ Ocorreu um erro ao conectar com a IA: {e}"