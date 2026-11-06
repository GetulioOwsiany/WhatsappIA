import pandas as pd

def obter_total_mensagens(df):
    return len(df)

def obter_mensagens_por_participante(df):
    contagem = df['Remetente'].value_counts().reset_index()
    contagem.columns = ['Remetente', 'Quantidade']
    return contagem

def obter_horarios_de_pico(df):
    # Extrai apenas as duas primeiras letras da string de hora (ex: "14" de "14:30:00")
    df['Hora_do_Dia'] = df['Hora'].str[:2]
    pico = df['Hora_do_Dia'].value_counts().sort_index().reset_index()
    pico.columns = ['Hora', 'Quantidade']
    return pico

def obter_frequencia_diaria(df):
    # Agrupa pelo dia e conta quantas mensagens ocorreram em cada data
    frequencia = df.groupby('Data').size().reset_index(name='Quantidade')
    return frequencia