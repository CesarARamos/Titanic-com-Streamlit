import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

vcolor2 = sns.color_palette("Set2")
vcolor = sns.color_palette("Paired")

def criar_histograma(coluna, df):
    chart = alt.Chart(df, width=600).mark_bar().encode(
        alt.X(coluna, bin= True),
        y='count()', tooltip=[coluna, 'count()']
    ).interactive()
    return chart

def criar_barras(coluna_num, coluna_cat, df):
    bars = alt.Chart(df, width = 600).mark_bar().encode(
        x=alt.X(coluna_num, stack='zero'),
        y=alt.Y(coluna_cat),
        tooltip=[coluna_cat, coluna_num]
    ).interactive()
    return bars

def criar_scatterplot(x, y, color, df):
    scatter = alt.Chart(df, width=800, height=400).mark_circle().encode(
        alt.X(x),
        alt.Y(y),
        color = color,
        tooltip = [x, y]
    ).interactive()
    return scatter

def criar_infoclasse(df):
    df[df['Não sobreviveu'] == 1].groupby('Classe').sum()['Não sobreviveu'].plot(kind='bar',
                                                                                 title='Quantide de Não sobreviventes por Classe',
                                                                                 color=vcolor2, rot=0,
                                                                                 figsize=(15, 4)).set_xlabel('Classe')

    st.pyplot()

    df[df['Não sobreviveu'] == 0].groupby('Classe').sum()['Sobreviveu'].plot(kind='bar',
                                                                                 title='Quantide de sobreviventes por Classe',
                                                                                 color=vcolor, rot=0,
                                                                                 figsize=(15, 4)).set_xlabel('Classe')

    st.pyplot()

def criar_infosexo(df):
    df.pivot_table('PassengerId', ['Classe'], 'Sexo', aggfunc='count').sort_index().plot(kind='barh',
                                                                                         color=vcolor2,
                                                                                         title='Quantidade de Homens e Mulheres por Classe').legend(
        bbox_to_anchor=(1.0, 1.0))
    plt.xlabel('Quantidade')
    st.pyplot()

    df[df['Sobreviveu'] == 1].pivot_table('PassengerId', ['Classe'], 'Sexo', aggfunc='count').plot(kind='barh',
                                                                                                   color=vcolor,
                                                                                                   title='Quantidade de Sobrevientes Homens e Mulheres por Classe').legend(bbox_to_anchor=(1.0, 1.0))

    st.pyplot()

def criar_infoidade(df):
    df_histage = pd.DataFrame({'Total': df['Idade'],
                               'Não Sobreviveram': df[df['Não sobreviveu'] == 1]['Idade'],
                               'Sobreviveram': df[df['Sobreviveu'] == 1]['Idade']},

                              columns=['Total', 'Não Sobreviveram', 'Sobreviveram'])

    plt.figure();

    df_histage.plot.hist(bins=10, alpha=0.6, figsize=(10, 5), color=vcolor2,
                         title='Histogramas (Total, Sobreviventes e Não sobreviventes) por Idade')
    plt.xlabel('Idade')
    plt.ylabel('Frequência')
    plt.show()

    st.pyplot()

    df_criancas = df[(df['Idade'] <= 11) & (df['Sobreviveu'] == 1)].groupby('Classe').count()[['Sobreviveu']]
    df_criancas_tmp = df[(df['Idade'] <= 11) & (df['Sobreviveu'] == 0)].groupby('Classe').count()[['Sobreviveu']]
    result = pd.concat([df_criancas, df_criancas_tmp], axis=1)
    df_criancas_tmp2 = df[(df['Idade'] <= 11)].groupby('Classe').count()[['Sobreviveu']]
    result = pd.concat([result, df_criancas_tmp2], axis=1)
    result.columns.values[1] = 'Não sobreviveu'
    result.columns.values[2] = 'Total'
    st.table(result.fillna(0))

    result.fillna(0).plot(kind='bar', rot=0, figsize=(8, 4),
                          color=vcolor,
                          title='Quantidade de Crianças que Sobrevieram e Não Sobreviveram por Classe')
    plt.ylabel('Quantidade')
    st.pyplot()

def cria_correlationplot(df, colunas_numericas):
    cor_data = (df[colunas_numericas]).corr().stack().reset_index().rename(columns={0: 'correlation', 'level_0': 'variable', 'level_1': 'variable2'})
    cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format)  # Round to 2 decimal
    base = alt.Chart(cor_data, width=500, height=500).encode( x = 'variable2:O', y = 'variable:O')
    text = base.mark_text().encode(text = 'correlation_label',color = alt.condition(alt.datum.correlation > 0.5,alt.value('white'),
    alt.value('black')))

# The correlation heatmap itself
    cor_plot = base.mark_rect().encode(
    color = 'correlation:Q')

    return cor_plot + text

def main():
    st.title('DataSet Titanic')
    st.image('titanic.gif', width=600)
    st.subheader('Análise de Dados Exploratória')
    st.subheader('Dicionário de Dados')

    '''
    -Survived (Sobreviveu): 0 = Não, 1 = Sim

    -Pclass (Classe): Classe de ingresso 1 = 1º, 2 = 2º, 3 = 3º

    -Sex (Sexo): Sexo do passageiro

    -Age (Idade): Idade em anos

    -Sibsp: Quantidade de irmãos / cônjuges a bordo do Titanic

    -Parch: Quantidade de pais / crianças a bordo do Titanic

    -Ticket (Bilhete): Número do bilhete de embarque

    -Fare (Tarifa): Tarifa paga pelo Passageiro

    -Cabin (Cabine): Número de cabine

    -Embarked (Embarque): Porto de Embarque (C = Cherbourg, Q = Queenstown, S = Southampton)
    '''
    st.subheader('Notas sobre as variáveis')
    '''
    Pclass (Classe): 1º = Superior 2º = Médio 3º = inferior

    Age (Idade): A idade é fracionada se for inferior a 1. Se a idade for estimada, é na forma de xx.5

    Sibsp: O conjunto de dados define as relações familiares dessa maneira ...
    Sibling = Irmão, irmã, meio-irmão, irmandade
    Spouse (Cônjuge) = marido, esposa (amantes e desposados foram ignorados)

    Parch: O conjunto de dados define as relações familiares dessa maneira ...
    Parent (Pais) = mãe, pai
    Child (Criança) = filha, filho, enteada, enteado
    Algumas crianças viajaram apenas com uma babá, portanto, parch = 0 para elas.
    '''

    file  = st.file_uploader('Selecione o dataset do Titanic para as observações (.csv)', type = 'csv')
    if file is not None:
        df = pd.read_csv(file)
        df.columns = ['PassengerId', 'Sobreviveu', 'Classe', 'Nome', 'Sexo', 'Idade', 'SibSp',
                      'Parch', 'Num_Ticket', 'Tarifa', 'Cabine', 'Embarque']
        df['Sexo'] = df['Sexo'].map({'female': 'M',
                                     'male': 'H'})

        # Slider
        slider = st.slider('Valores', 1, 891)
        st.dataframe(df.head(slider))

        # Informação de linhas e colunas
        st.write('N° Linhas:', df.shape[0])
        st.write('N° Colunas:', df.shape[1])
        sobrevivi = df['Sobreviveu'].value_counts()[1]
        nsobrevivi = df['Sobreviveu'].value_counts()[0]
        st.write('Sobreviventes     :', sobrevivi)
        st.write('Não Sobreviventes :', nsobrevivi)
        porc = round((sobrevivi / df.shape[0]) * 100)
        porc2 = round((nsobrevivi / df.shape[0]) * 100)
        st.write('Porcentagem de Sobreviventes:', porc, '%')
        st.write('Porcentagem de Não Sobreviventes:', porc2, '%')

        st.subheader('Estatística Descritiva Univariada')
        aux = pd.DataFrame({"colunas": df.columns, 'tipos': df.dtypes})
        colunas_numericas = list(aux[aux['tipos'] != 'object']['colunas'])
        colunas_object = list(aux[aux['tipos'] == 'object']['colunas'])
        colunas = list(df.columns)
        df['Não sobreviveu'] = df['Sobreviveu'].map({1: 0,
                                                     0: 1})




        #Análise descritiva
        col = st.selectbox('Selecione a coluna a ser analisada:', colunas_numericas[:0:-3])
        if col is not None:
            st.markdown('O que deseja verificar :')
            mean = st.checkbox('Média')
            if mean:
                st.markdown(df[col].mean())
            median = st.checkbox('Mediana')
            if median:
                st.markdown(df[col].median())
            desvio_pad = st.checkbox('Desvio padrão')
            if desvio_pad:
                st.markdown(df[col].std())
            describe = st.checkbox('Describe')
            if describe:
                st.table(df[colunas_numericas].describe().transpose())
            info_classe = st.checkbox('Mostre-me as informações por CLASSE:')
            if info_classe:
                st.table(df.pivot_table(index='Classe',  values=('Sobreviveu','Não sobreviveu'), aggfunc=np.sum))
                criar_infoclasse(df)
            info_sexo = st.checkbox('Mostre-me as informações por SEXO:')
            if info_sexo:
                st.table(df.pivot_table('PassengerId', ["Sexo"], 'Classe', aggfunc='count'))
                criar_infosexo(df)
                st.table(df.groupby(['Sexo', 'Classe']).sum()[['Sobreviveu', 'Não sobreviveu']])
            info_idade = st.checkbox('Mostre-me as informações por IDADE:')
            if info_idade:
                st.write('Passageiros SEM idade preenchida:', df['Idade'].isnull().sum())
                st.write('Passageiros COM idade preenchida:', (~df['Idade'].isnull()).sum())
                criar_infoidade(df)

        #Criação dos plots
        st.subheader('Verificação Gráfica Interativa')
        st.markdown('Selecione o Tipo de Visualizacao')

        histograma = st.checkbox('Histograma')
        if histograma:
            col_num = st.selectbox('Selecione a Coluna Numérica: ', colunas_numericas[1:4],key = 'unique')
            st.markdown('Histograma da coluna : ' + str(col_num))
            st.write(criar_histograma(col_num, df))

        barras = st.checkbox('Gráfico de barras')
        if barras:
            col_num_barras = st.selectbox('Selecione a coluna numerica: ', colunas_numericas[1:7], key = 'unique')
            col_cat_barras = st.selectbox('Selecione uma coluna categorica : ', colunas_object, key = 'unique')
            st.markdown('Gráfico de barras da coluna ' + str(col_cat_barras) + ' pela coluna ' + col_num_barras)
            st.write(criar_barras(col_num_barras, col_cat_barras, df))

        scatter = st.checkbox('Scatterplot')
        if scatter:
            col_num_x = st.selectbox('Selecione o valor de x ', colunas_numericas, key = 'unique')
            col_num_y = st.selectbox('Selecione o valor de y ', colunas_numericas, key = 'unique')
            col_color = st.selectbox('Selecione a coluna para cor', colunas, key = 'unique')
            st.markdown('Selecione os valores de x e y')
            st.write(criar_scatterplot(col_num_x, col_num_y, col_color, df))

        correlacao = st.checkbox('Correlacao')
        if correlacao:
            st.markdown('Gráfico de correlação das colunas númericas')
            st.write(cria_correlationplot(df, colunas_numericas))


if __name__ == '__main__':
    main()
