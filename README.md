# 📱 WhatsApp AI Analytics

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?logo=google&logoColor=white)

Um projeto de análise de dados e Inteligência Artificial Generativa desenvolvido para extrair insights de conversas do WhatsApp. Este projeto foi concebido como parte do meu portfólio para a candidatura à trilha de **AI Engineer do GenAI iFood**.

## 🎯 Objetivo
Transformar exportações brutas de texto do WhatsApp (`.txt`) num dashboard interativo, permitindo análises estatísticas de comportamento e a extração de padrões complexos utilizando Large Language Models (LLMs).

## ✨ Funcionalidades
- **Data Parsing:** Leitura e tratamento de ficheiros `.txt`, lidando com mensagens multilinhas e removendo notificações automáticas do sistema através de Expressões Regulares (Regex).
- **Analytics Básico:** Cálculo de volumetria (total de mensagens, participantes mais ativos) e análise temporal (horários de pico e frequência diária) utilizando `Pandas`.
- **Dashboard Interativo:** Interface web responsiva construída em `Streamlit`, permitindo o upload dinâmico de conversas sem necessidade de expor os dados.
- **Integração GenAI:** Chamada à API do **Google Gemini (3.8 Flash)** para gerar resumos automáticos, análise de sentimento e identificação de padrões de comunicação.

## 🛠️ Engenharia e Boas Práticas
Durante o desenvolvimento, foquei em práticas fundamentais de Engenharia de Software:
1. **Segurança de Credenciais:** As chaves de API nunca são expostas no código, sendo geridas de forma segura através de variáveis de ambiente (`.env` e `python-dotenv`).
2. **Separação de Responsabilidades (Clean Code):** O código não é um script único. Está dividido de forma lógica em `data_parser.py` (ETL), `analytics.py` (Regras de Negócio) e `ai_integration.py` (Conexões Externas).
3. **Resiliência (Fault Tolerance):** Implementação de blocos `try/except` com lógicas de *Fallback* (Mocking) para lidar de forma elegante com instabilidades da API externa (Erros 503) ou limitação de taxa/Rate Limits (Erro 429).
4. **Privacidade de Dados:** Os ficheiros carregados via interface são processados em memória/armazenamento temporário e excluídos imediatamente após a extração dos dados (bloco `finally`), garantindo a privacidade do utilizador.

## 🚀 Como Executar o Projeto

1. Clone este repositório:
```bash
git clone [https://github.com/GetulioOwsiany/whatsapp-ai-analytics.git](https://github.com/GetulioOwsiany/whatsapp-ai-analytics.git)
cd whatsapp-ai-analytics