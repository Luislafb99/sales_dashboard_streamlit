import pandas as pd
import plotly.express as px


def crear_grafico(df):
	#Crearemos las métricas para visualizar en streamlit
	#st.metric('**Total de Revenues**',df_ventas["valor total"].sum())
	#st.metric('**Total de Ventas**',df_ventas['cantidad_itens'].sum())
	df_mapa=df.groupby('geolocation_state').agg({
	'valor_total':'sum',
	'geolocation_lat':'mean',
	'geolocation_lng':'mean'
	}).reset_index().sort_values(by='valor_total',ascending=False)
	#Graficamos mapa de Brasil

	graf_mapa = px.scatter_geo(df_mapa,
		lat ='geolocation_lat',
		lon ='geolocation_lng',
		scope ='south america',
		template = 'seaborn',
		size = 'valor_total',
		hover_name = 'geolocation_state',
		hover_data = {'geolocation_lat':False,'geolocation_lng':False},
		title = 'Ingresos por estado'
		)
	return graf_mapa
	