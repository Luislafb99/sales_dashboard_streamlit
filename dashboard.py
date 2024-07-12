import streamlit as st
import pandas as pd
import Grafico_mapa as graf1
import grafico_lineas as graf2
import grafico_barras as graf3
import grafico_pizza as graf4

st.set_page_config(layout='wide')

st.title("Dashboard de Ventas :shopping_trolley: ")

def formata_numero(valor,prefijo = ''):
	for unidad in ['','k']:
		if valor < 1000:
			return f'{prefijo} {valor:.2f} {unidad}'
		valor /= 1000
	return f'{prefijo} {valor:.2f} M'


#Abrimos las bases de datos
#Si leemos db en linea agregamos raw antes de la pagina de git
#Despues de github se agrega usercontent, ademas se quita blob del directorio
df_ventas = pd.read_csv('https://raw.githubusercontent.com/Luislafb99/sales_dashboard_streamlit/main/base_ventas.csv')
df_ventas['valor_total'] = ((df_ventas.price*df_ventas.cantidad_itens)+(df_ventas.freight_value*df_ventas.cantidad_itens)) 
df_ventas['order_purchase_timestamp']=pd.to_datetime(df_ventas['order_purchase_timestamp'])
df_ventas['tipo_producto'] = df_ventas['product_category_name'].str.split('_').str[0]



#Configuramos los filtros
st.sidebar.image('https://img.freepik.com/vector-gratis/logotipo-empresa-comercial-supermercado_23-2148462314.jpg?size=626&ext=jpg')
st.sidebar.title('Filtros')


estados = sorted(list(df_ventas['geolocation_state'].unique()))
ciudades = st.sidebar.multiselect('Estados', estados)
productos = sorted(list(df_ventas['tipo_producto'].dropna().unique()))
productos.insert(0,'All')
producto = st.sidebar.selectbox('Productos',productos)


años = st.sidebar.checkbox('Histórico completo',value = True)
if not años:
	año = st.sidebar.slider('Año', df_ventas['order_purchase_timestamp'].dt.year.min(),df_ventas['order_purchase_timestamp'].dt.year.max())


#Filtrando los datos

if ciudades:
	df_ventas = df_ventas[df_ventas['geolocation_state'].isin(ciudades)]

if producto!='All':
	df_ventas = df_ventas[df_ventas['tipo_producto']==producto]
if not años:
	df_ventas = df_ventas[df_ventas['order_purchase_timestamp'].dt.year == año]



#Hacemos programación modular y creamos los gráficos
graf_mapa = graf1.crear_grafico(df_ventas)
graf_lineas = graf2.crear_grafico(df_ventas)
graf_barras = graf3.crear_grafico(df_ventas)
graf_pizza = graf4.crear_grafico(df_ventas)


#Damos formato a estas métricas
col1, col2 = st.columns(2)
with col1:
	st.metric('**Total de Revenues**',formata_numero(df_ventas["valor_total"].sum(),'$'))
	st.plotly_chart(graf_mapa,use_container_width=True)
	st.plotly_chart(graf_barras,use_container_width=True)
with col2:
	st.metric('**Total de Ventas**',formata_numero(df_ventas['cantidad_itens'].sum(),))
	st.plotly_chart(graf_lineas,use_container_width=True)
	st.plotly_chart(graf_pizza,use_container_width=True)






