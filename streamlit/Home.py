#Librerías
import streamlit as st
import pandas as pd
import numpy as np
import os
import datetime
import matplotlib.pyplot as plt
#from st_pages import Page, show_pages, add_page_title

# Lectura de los datasets y creación de los dataframes
datasets = os.listdir('../datasets_clean')
dataframes = {f'{csv}': pd.read_csv(f'../datasets_clean/{csv}') for csv in datasets} # Se crean y se guardan en un diccionario

#Se guardan los dataframes en variables para poder ser usados con más façilidad.
closed_deals = dataframes['closed_deals.csv']
conectividad= dataframes['conectividad_X_Estado.csv']
customers = dataframes['customers.csv']
geolocation = dataframes['geolocation.csv']
marketing_qualified_leads = dataframes['marketing_qualified_leads.csv']
orders_delivered = dataframes['orders_delivered.csv']
orders_No_delivered = dataframes['orders_No_delivered.csv']
order_items = dataframes['order_items.csv']
order_payments = dataframes['order_payments.csv']
order_reviews = dataframes['order_reviews.csv']
products = dataframes['products.csv']
sellers = dataframes['sellers.csv']
orders = pd.concat([orders_delivered, orders_No_delivered])


#Título y diseño inicial
st.set_page_config(page_title="Data Innovative")
st.title(':globe_with_meridians: Data Innovative')

st.sidebar.header('Menú') # Creaci´n del título "Menú" en la barra lateral

# Creación de botones en la barra lateral
button_powerbi = st.sidebar.button(':bar_chart: Reporte PowerBI')
button_ventas = st.sidebar.button(':heavy_dollar_sign: Análisis de Ventas')
button_clientes = st.sidebar.button(':male-office-worker: Análisis de clientes')
button_vendedores_clientes = st.sidebar.button(":currency_exchange: Clientes vs Vendedores")
button_resenias = st.sidebar.button(':scroll: Análisis de Reseñas')


# Configuración de los botones
if button_powerbi:
    st.markdown(f"## :bar_chart: Reporte en PowerBI")
    st.markdown(f"Para ver el reporte, ir al siguiente enlace:")
    st.markdown('[Reporte en PowerBI](https://app.powerbi.com/view?r=eyJrIjoiMThmZWVhZWEtMDczYy00NWMzLWJkYTktODU0NmIzZTFjYWJkIiwidCI6IjYxOGJhYjBmLTIwYTQtNGRlMy1hMTBjLWUyMGNlZTk2YmIzNSIsImMiOjR9)',unsafe_allow_html=True)

elif button_ventas:
    
    st.markdown(f"## :heavy_dollar_sign: Análisis de Ventas")

    #--------------Selección de fechas--------------
    col1, col2 = st.columns(2)
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    start_date = col1.date_input('Start date', today)
    end_date = col2.date_input('End date', tomorrow)
    if start_date < end_date:
        st.success('Fecha de inicio: `%s`\n\nFecha final:`%s`' % (start_date, end_date))
    else:
        st.error('Error: End date must fall after start date.')

    
    #Organizando los formatos de fecha en el dataframe de orders
    orders_delivered['date']=orders_delivered['order_purchase_timestamp'].str.split(" ").apply(lambda x: x[0])
    porcentaje_marketing = closed_deals.shape[0]/marketing_qualified_leads.shape[0]

    #--------------Métricasy KPI's--------------
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Variación Porcentual de Ventas", value='70 °F')
    col2.metric(label="Porcentaje de Marketing", value=f'{porcentaje_marketing*100}%')
    col3.metric(label="Variación Trimestral de Gancias", value="70 °F")
    
    #--------------Gráfico lineal: Ventas por mes--------------
    st.write("Cantidad de ventas por mes")
    data = orders_delivered['date'].value_counts()
    st.line_chart(data)

    #--------------Porcentaje de Capatación por Marketing--------------
    st.write("Porcentaje de captación de vendedores por marketing")
    df_temp = pd.DataFrame(marketing_qualified_leads['origin'].value_counts())
    st.table(df_temp)

    #--------------Gráfico circular--------------
    col1, col2 = st.columns(2)
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    payment_type = order_payments['payment_type'].unique().tolist()
    counts = order_payments['payment_type'].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(counts, labels=payment_type, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    col1.pyplot(fig1)

    #--------------Gráfico de Barras--------------
    # Fixing random state for reproducibility
    np.random.seed(19680801)

    plt.rcdefaults()
    fig, ax = plt.subplots()

    # Example data
    people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
    y_pos = np.arange(len(people))
    performance = 3 + 10 * np.random.rand(len(people))
    error = np.random.rand(len(people))

    ax.barh(y_pos, performance, xerr=error, align='center')
    ax.set_yticks(y_pos, labels=people)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Performance')
    ax.set_title('How fast do you want to go today?')

    col2.pyplot(fig)

elif button_clientes:
    st.markdown("## :male-office-worker: Análisis de clientes")
    #Organizando los formatos de fecha en el dataframe de orders
    orders_delivered['date']=orders_delivered['order_purchase_timestamp'].str.split(" ").apply(lambda x: x[0])
    orders_No_delivered['date']=orders_No_delivered['order_purchase_timestamp'].str.split(" ").apply(lambda x: x[0])
    porcentaje_cancelacion = round(orders_No_delivered.shape[0]/(orders_delivered.shape[0]+orders_No_delivered.shape[0])*100,2)

    #--------------Métricasy KPI's--------------
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Variación Porcentual de Ventas", value='70 °F')
    col2.metric(label="Porcentaje Cancelación de órdenes", value=f'{porcentaje_cancelacion}%')
    col3.metric(label="Variación Trimestral de Ventas completadas", value=100-porcentaje_cancelacion)

    #--------------Gráfico lineal--------------
    data = orders_delivered['date'].value_counts()
    st.line_chart(data)

    #--------------Gráfico lineal: Cancelaciones por mes--------------
    data = orders_No_delivered['date'].value_counts()
    st.line_chart(data)

    #--------------Top de mejores clientes--------------
    st.write("Top 10 mejores clientes")
    df_temp = pd.DataFrame(customers['customer_unique_id'].value_counts())
    df_temp=df_temp.reset_index()
    df_temp.rename(columns={'index':'customer_unique_ID','customer_unique_id': 'Cantidad de compras'}, inplace=True)
    #number = st.number_input('Indique la cantidad de clientes que desea ver', min_value = 1)
    st.table(df_temp.head(10))

elif button_vendedores_clientes:

    #Elegimos los dataframes que queremos trabajar con las columnas renombradas igual para poder hacer el merge 
    df_sellers = sellers.rename(columns={'seller_zip_code_prefix':'zip_code_prefix'})
    df_geo = geolocation.rename(columns={'geolocation_zip_code_prefix':'zip_code_prefix'})
    df_geo = df_geo[['zip_code_prefix','geolocation_lat','geolocation_lng']]
    df_customers = customers.rename(columns={'customer_zip_code_prefix':'zip_code_prefix'})
    
    #Merge (JOIN) de los dataframes
    df_sellers_geo = pd.merge(df_sellers,df_geo, on='zip_code_prefix')
    df_customers_geo = pd.merge(df_customers,df_geo, on='zip_code_prefix')

    #Creación de la métrica
    st.markdown("## :currency_exchange: Clientes vs Vendedores")
    col1, col2, col3 = st.columns(3)
    col2.metric(label="Promedio de demora en días", value='70 °F')
    
    # Creación de los mapas
    col1, col2 = st.columns(2) #Se crean dos columnas donde van los mapas
    col1.markdown("### Distribución geográfica de vendedores")
    map_data = pd.DataFrame(
      np.array([df_sellers_geo['geolocation_lat'].tolist(),df_sellers_geo['geolocation_lng'].tolist()]).transpose(),
        columns=['lat', 'lon'])
    col1.map(map_data)
    col2.markdown("### Distribución geográfica de compradores")
    map_data = pd.DataFrame(
      np.array([df_customers_geo['geolocation_lat'].tolist(),df_customers_geo['geolocation_lng'].tolist()]).transpose(),
        columns=['lat', 'lon'])
    col2.map(map_data)

elif button_resenias:
    
    #Creación de la relación de las tablas necesarias para encontrar la información correspondiente
    df = pd.merge(customers,pd.merge(order_reviews,orders_delivered, on='order_id'), on = 'customer_id')
  
    option = st.selectbox('Selecciona el estado que desee visualizar', (df['customer_state'].unique()))

    #Conteo de reviews para cada caso: positivos, negativos y neutros
    # negativo = df[df["review_score"]<3][df["customer_state"]==option].shape[0]
    # neutro = df[(df["review_score"]==3)][df["customer_state"]==option].shape[0]
    # positivo = df[(df["review_score"]>3)][df["customer_state"]==option].shape[0]

    negativo = df[df["review_score"]<3][df["customer_state"]=='AC'].shape[0]
    neutro = df[(df["review_score"]==3)][df["customer_state"]=='AC'].shape[0]
    positivo = df[(df["review_score"]>3)][df["customer_state"]=='AC'].shape[0]

    
    #Título de la página
    st.markdown(f"## :scroll: Análisis de Reseñas")

    #Creación de las métricas
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Score negativo",value=negativo)
    col2.metric(label="Score neutro", value=neutro)
    col3.metric(label="Score positivo", value=positivo)

    
    score_promedio = round(df[df['customer_state']=='AC']['review_score'].mean(),2)
    col1, col2, col3 = st.columns(3)
    col2.markdown(f'## El score promedio del estado de {option} es {score_promedio}')
    
    if score_promedio <=1.44:
        col2.markdown("## :star:")
    elif score_promedio <=2.44:
        col2.markdown("## :star: :star:")
    elif score_promedio <=3.44:
        col2.markdown("## :star: :star: :star:")
    elif score_promedio <=4.44:
        col2.markdown("## :star: :star: :star: :star:")
    elif score_promedio > 4.44:
        col2.markdown("## :star: :star: :star: :star:")

# left_column, right_column = st.columns(2)
# # You can use a column just like st.sidebar:
# left_column.button('Press me!')

# with right_column:
#     chosen = st.radio(
#         'Sorting hat',
#         ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
#     st.write(f"You are in {chosen} house!")