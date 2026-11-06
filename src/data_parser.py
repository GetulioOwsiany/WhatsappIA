import re
import pandas as pd

def parse_whatsapp_chat(caminho_ficheiro):
    # Regex flexível: aceita 1 ou 2 dígitos para dia/mês, 2 ou 4 para ano, e horário com ou sem AM/PM
    padrao = r'^\[(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}:\d{2}(?: [AP]M)?)\] (.*?): (.*)'
    dados = []
    
    with open(caminho_ficheiro, 'r', encoding='utf-8') as ficheiro:
        data_atual, hora_atual, remetente_atual, mensagem_atual = None, None, None, ""
        
        for linha in ficheiro:
            linha = linha.strip()
            if not linha:
                continue
                
            match = re.match(padrao, linha)
            
            if match:
                # Salva a mensagem anterior na lista antes de começar a processar a nova
                if remetente_atual is not None:
                    dados.append([data_atual, hora_atual, remetente_atual, mensagem_atual.strip()])
                
                # Extrai os novos dados usando os grupos do Regex
                data_atual = match.group(1)
                hora_atual = match.group(2)
                remetente_atual = match.group(3)
                mensagem_atual = match.group(4)
            else:
                # Se a linha não tem o padrão de data/hora, é continuação (multilinha)
                if remetente_atual is not None:
                    mensagem_atual += f" {linha}"
                    
        # Garante que a última mensagem do ficheiro seja guardada
        if remetente_atual is not None:
            dados.append([data_atual, hora_atual, remetente_atual, mensagem_atual.strip()])
            
    # Estrutura os dados diretamente num DataFrame
    df = pd.DataFrame(dados, columns=['Data', 'Hora', 'Remetente', 'Mensagem'])
    
    # Normalização de Dados (Data Cleaning):
    # format='mixed' faz o Pandas identificar automaticamente se é DD/MM/YYYY ou M/D/YY
    df['Data'] = pd.to_datetime(df['Data'], format='mixed', dayfirst=True)
    
    # Converte qualquer formato de hora (ex: 6:26:29 PM) para o formato padrão 24h (18:26:29)
    # Isso garante que a nossa função de análise de horários de pico continue a funcionar perfeitamente
    df['Hora'] = pd.to_datetime(df['Hora'], format='mixed').dt.strftime('%H:%M:%S')
    
    return df