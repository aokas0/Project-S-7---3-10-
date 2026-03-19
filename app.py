import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración básica de la app
st.set_page_config(page_title="Análisis de Vehículos", layout="wide")

# Crear un encabezado general
st.title('Análisis de Anuncios de Venta de Coches')
st.markdown("Explorador de datos interactivo para descubrir información sobre los vehículos en venta.")

# Leer los datos
# Aquí no usamos '../' porque app.py está en la misma carpeta
car_data = pd.read_csv('vehicles_us.csv') 

# Preprocesamiento: Extraer fabricante del modelo
# El fabricante es la primera palabra en la columna 'model'
car_data['manufacturer'] = car_data['model'].apply(lambda x: x.split()[0].capitalize())

st.markdown("---")

# 1. Gráficos Básicos Iniciales (Requisitos del proyecto básico)
st.subheader("Estadísticas Generales")
col_check1, col_check2 = st.columns(2)

with col_check1:
    build_histogram = st.checkbox('Construir un histograma (Odómetro)')
with col_check2:
    build_scatter = st.checkbox('Construir gráfico de dispersión (Precio)')

if build_histogram: # al hacer clic en la casilla
    st.write('Distribución del kilometraje (odómetro) de los vehículos')
    fig = px.histogram(car_data, x="odometer", title="Distribución de Kilometraje")
    st.plotly_chart(fig, use_container_width=True)

if build_scatter: # al hacer clic en la casilla
    st.write('Relación entre kilometraje y precio de los vehículos')
    fig2 = px.scatter(car_data, x="odometer", y="price", title="Precio vs Kilometraje")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# 2. Tipos de vehículos filtrados por fabricante
st.subheader("Tipos de Vehículos por Fabricante")
st.write("Selecciona un fabricante para ver la cantidad de vehículos en venta según su tipo.")

fabricantes_unicos = sorted(car_data['manufacturer'].unique())
fabricante_seleccionado = st.selectbox('Selecciona el Fabricante:', fabricantes_unicos)

# Filtramos y creamos la gráfica
datos_filtrados = car_data[car_data['manufacturer'] == fabricante_seleccionado]
fig3 = px.histogram(datos_filtrados, x="type", color="type",
                    title=f"Distribución de tipos de vehículos para el fabricante {fabricante_seleccionado}")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# 3. Histograma de la condición del vehículo por año del modelo
st.subheader("Condición del Vehículo vs Año del Modelo")
st.write("Visualiza cómo afecta el año del vehículo a su condición. Selecciona si deseas ver la distribución por un rango de años.")

fig4 = px.histogram(car_data, x="model_year", color="condition", 
                    barmode="stack", title="Condición de Vehículos según el Año de Fabricación")
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# 4. Comparación de precio entre dos fabricantes
st.subheader("Comparador Interactivo de Precios entre Fabricantes")
st.write("Selecciona dos fabricantes para comparar directamente la distribución de los precios de sus vehículos.")

col1, col2 = st.columns(2)

with col1:
    # Selecciona por defecto el índice 0 o 'Ford' si existe
    idx_1 = fabricantes_unicos.index('Ford') if 'Ford' in fabricantes_unicos else 0
    fab1 = st.selectbox('Elige el Fabricante 1:', fabricantes_unicos, index=idx_1)

with col2:
    # Selecciona por defecto el índice 1 o 'Chevrolet' si existe
    idx_2 = fabricantes_unicos.index('Chevrolet') if 'Chevrolet' in fabricantes_unicos else 1
    fab2 = st.selectbox('Elige el Fabricante 2:', fabricantes_unicos, index=idx_2)

# Filtrar los datos solo para esos dos fabricantes
datos_comparacion = car_data[car_data['manufacturer'].isin([fab1, fab2])]

# Crear el histograma superpuesto (barmode="overlay")
fig5 = px.histogram(datos_comparacion, x="price", color="manufacturer", 
                    barmode="overlay",
                    color_discrete_sequence=['#EF553B', '#00CC96'],
                    title=f"Distribución de Precios: {fab1} vs {fab2}")

# Aumentar la visibilidad regulando la opacidad
fig5.update_traces(opacity=0.75)
st.plotly_chart(fig5, use_container_width=True)
