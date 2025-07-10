# app.py

import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA DE STREAMLIT
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Generador de Noticias Económicas",
    page_icon="📰",
    layout="wide"
)

# -----------------------------------------------------------------------------
# LÓGICA DE EXTRACCIÓN Y PROCESAMIENTO
# -----------------------------------------------------------------------------
@st.cache_data
def cargar_y_procesar_datos():
    """
    Esta función contiene toda la lógica de extracción de datos del HTML.
    Al estar cacheada, no se volverá a ejecutar cada vez que el usuario interactúe.
    """
    html_content = """
    <section class="u-estructura-home__seccion"><div class="c-board c-board-indicadores" data-mrf-recirculation="Indicadores"><div class="c-board__header"><h2 class="c-board__header__titulo">INDICADORES</h2><a href="/economia" class="c-board-indicadores__link" data-mrf-link="https://www.eltiempo.com/economia" cmp-ltrk="Indicadores" cmp-ltrk-idx="0" mrfobservableid="f5410de9-fc10-453b-8d21-aa6494e28520">> Más Economía</a></div>    <div class="c-board-indicadores__contenedor">
                                                    <div class="c-board-indicadores__item c-board-indicadores__item--down">
                        <span class="c-board-indicadores__item__titulo">Dólar</span><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">$  4.004,30</span><span class="c-board-indicadores__item__previo">-$ 13,2</span><span class="c-board-indicadores__item__diferencia">-$ 0,33</span></div><div class="c-board-indicadores__item c-board-indicadores__item--down"><span class="c-board-indicadores__item__titulo">TRM</span><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">$  4.026,09</span><span class="c-board-indicadores__item__previo">-$ 28,0398</span><span class="c-board-indicadores__item__diferencia"> </span></div><div class="c-board-indicadores__item c-board-indicadores__item--down"><span class="c-board-indicadores__item__titulo">Euro</span><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">$  4.708,51</span><span class="c-board-indicadores__item__previo">-$ 29,09</span><span class="c-board-indicadores__item__diferencia">-$ 0,62</span></div><div class="c-board-indicadores__item c-board-indicadores__item--up"><span class="c-board-indicadores__item__titulo">Bolívar</span><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">US$  113,466124</span><span class="c-board-indicadores__item__previo">+$ 0,919695</span><span class="c-board-indicadores__item__diferencia">+$ 0,82</span></div><div class="c-board-indicadores__item c-board-indicadores__item--up"><span class="c-board-indicadores__item__titulo">Peso mexicano</span><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">US$  0,463</span><span class="c-board-indicadores__item__previo"> </span><span class="c-board-indicadores__item__diferencia"> </span></div><div class="c-board-indicadores__item c-board-indicadores__item--up"><span class="c-board-indicadores__item__titulo">Café</span><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">US$  287,8</span><span class="c-board-indicadores__item__previo">+$ 1,95</span><span class="c-board-indicadores__item__diferencia">+$ 0,68</span></div><div class="c-board-indicadores__item c-board-indicadores__item--up"><span class="c-board-indicadores__item__titulo">Oro</span><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">US$  3318,3147</span><span class="c-board-indicadores__item__previo">+$ 4,9675</span><span class="c-board-indicadores__item__diferencia">+$ 0,15</span></div><div class="c-board-indicadores__item c-board-indicadores__item--up"><span class="c-board-indicadores__item__titulo">Tasa de usura en Colombia</span><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">24,78  %</span><span class="c-board-indicadores__item__previo"> </span><span class="c-board-indicadores__item__diferencia"> </span></div><div class="c-board-indicadores__item" data-position="9"><div class="c-board-indicadores__item c-board-indicadores__item--up"><span class="c-board-indicadores__item__titulo">Tasa de interés del Banrep</span><div class="c-board-indicadores__item__compress"><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">9,25  %</span></div><span class="c-board-indicadores__item__previo"> </span><span class="c-board-indicadores__item__diferencia"> </span></div><div class="c-board-indicadores__item c-board-indicadores__item--up"><span class="c-board-indicadores__item__titulo">ICOLCAP</span><div class="c-board-indicadores__item__compress"><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">$  16.660,50</span></div><span class="c-board-indicadores__item__previo">+$ 80,5</span><span class="c-board-indicadores__item__diferencia">+$ 0,49</span></div></div></div></div></section>
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    contenedor = soup.find('div', class_='c-board-indicadores__contenedor')
    indicadores_html = contenedor.find_all('div', class_='c-board-indicadores__item', recursive=False)
    datos_indicadores = []
    for item in indicadores_html:
        nombre_tag = item.find('span', class_='c-board-indicadores__item__titulo')
        precio_tag = item.find('span', class_='c-board-indicadores__item__precio')
        if nombre_tag and precio_tag:
            nombre = nombre_tag.get_text(strip=True)
            precio = precio_tag.get_text(strip=True).replace('\xa0', 'N/A')
            variacion_tag = item.find('span', class_='c-board-indicadores__item__previo')
            diferencia_tag = item.find('span', class_='c-board-indicadores__item__diferencia')
            variacion = variacion_tag.get_text(strip=True).replace('\xa0', 'N/A') if variacion_tag else 'N/A'
            diferencia_pct = diferencia_tag.get_text(strip=True).replace('\xa0', 'N/A') if diferencia_tag else 'N/A'
            datos_indicadores.append({ "Indicador": nombre, "Valor": precio, "Variacion": variacion, "Diferencia_Pct": diferencia_pct })
    
    df = pd.DataFrame(datos_indicadores)
    indicadores_dict = df.set_index('Indicador').to_dict('index')
    return df, indicadores_dict

# -----------------------------------------------------------------------------
# PLANTILLAS DE GENERACIÓN DE NOTICIAS
# -----------------------------------------------------------------------------

# --- Bloques de Contexto ---
CONTEXTO_DOLAR = "El valor del dólar frente al peso colombiano es un indicador fundamental para la economía del país. Su fluctuación tiene un impacto directo en el costo de los productos importados, los precios de los tiquetes aéreos, la tecnología y las materias primas. Asimismo, afecta el valor de las exportaciones colombianas, como el petróleo y el café, y el envío de remesas."
CONTEXTO_ICOLCAP = "El MSCI COLCAP es el principal índice de la Bolsa de Valores de Colombia (bvc) y agrupa a las acciones más líquidas y de mayor capitalización bursátil. Su desempeño refleja la confianza de los inversionistas en las grandes empresas del país y en la economía colombiana en general. Una tendencia al alza suele indicar optimismo, mientras que una baja puede señalar preocupación."

fuente = "El Tiempo"
attribution_line = f"<i>*Este contenido fue reescrito con la asistencia de una inteligencia artificial, basado en información de {fuente}.</i>"

def generar_noticia_dolar(datos, fecha):
    valor, variacion = datos['Valor'], datos['Variacion']
    tendencia_verbo = "registró una baja" if variacion.startswith('-') else "presentó un alza"
    titulo = f"Dólar en Colombia: así cerró la cotización el {fecha}"
    subtitulo = f"La divisa estadounidense {tendencia_verbo} durante la jornada, finalizando con un valor de {valor}."
    return f"""<h1>{titulo}</h1><h2>{subtitulo}</h2><hr>
               <p>El dólar estadounidense finalizó la jornada de negociación del <strong>{fecha}</strong> en Colombia con un valor de <strong>{valor}</strong>. Este resultado representa una modificación de <strong>{variacion} pesos</strong>.</p>
               <h2>Datos clave del dólar hoy</h2>
               <ul><li><strong>Valor de cierre:</strong> {valor}</li><li><strong>Variación diaria:</strong> {variacion}</li><li><strong>Variación porcentual:</strong> {datos['Diferencia_Pct']}%</li></ul>
               <h2>Importancia del dólar en la economía</h2><p>{CONTEXTO_DOLAR}</p>{attribution_line}"""

def generar_noticia_icolcap(datos, fecha):
    valor, variacion = datos['Valor'].replace('$', '').strip(), datos['Variacion'].replace('$', '').strip()
    tendencia_txt = "a la baja" if variacion.startswith('-') else "al alza"
    titulo = f"Índice MSCI COLCAP: Bolsa de Colombia cierra {tendencia_txt} el {fecha}"
    subtitulo = f"El principal índice bursátil del país concluyó la sesión en {valor} puntos."
    return f"""<h1>{titulo}</h1><h2>{subtitulo}</h2><hr>
               <p>El mercado de acciones colombiano, representado por el índice MSCI COLCAP, concluyó las operaciones del <strong>{fecha}</strong> en <strong>{valor} puntos</strong>.</p>
               <h2>Desempeño del MSCI COLCAP en cifras</h2>
               <ul><li><strong>Puntos de cierre:</strong> {valor}</li><li><strong>Variación en puntos:</strong> {variacion}</li><li><strong>Variación porcentual:</strong> {datos['Diferencia_Pct']}%</li></ul>
               <h2>¿Qué es el MSCI COLCAP?</h2><p>{CONTEXTO_ICOLCAP}</p>{attribution_line}"""

def generar_resumen_economico(datos_completos, fecha):
    dolar_data, icolcap_data, cafe_data = datos_completos.get('Dólar', {}), datos_completos.get('ICOLCAP', {}), datos_completos.get('Café', {})
    titulo = f"Cierre de mercados en Colombia: Resumen de la jornada del {fecha}"
    subtitulo = f"El dólar cerró en {dolar_data.get('Valor', 'N/A')}, el índice MSCI COLCAP se ubicó en {icolcap_data.get('Valor', 'N/A')} y el café finalizó en {cafe_data.get('Valor', 'N/A')}."
    return f"""<h1>{titulo}</h1><h2>{subtitulo}</h2><hr>
               <h2>Mercado Cambiario</h2><p>El <strong>dólar</strong> cerró en <strong>{dolar_data.get('Valor', 'N/A')}</strong>. El <strong>euro</strong> se cotizó en <strong>{datos_completos.get('Euro', {}).get('Valor', 'N/A')}</strong>.</p>
               <h2>Bolsa y Materias Primas</h2><p>El índice <strong>MSCI COLCAP</strong> cerró en <strong>{icolcap_data.get('Valor', 'N/A')}</strong> puntos. El <strong>café</strong> se cotizó en <strong>{cafe_data.get('Valor', 'N/A')}</strong> y el <strong>oro</strong> en <strong>{datos_completos.get('Oro', {}).get('Valor', 'N/A')}</strong>.</p>
               {attribution_line}"""

# -----------------------------------------------------------------------------
# CONSTRUCCIÓN DE LA INTERFAZ DE USUARIO (UI)
# -----------------------------------------------------------------------------

st.title("📰 Generador de Noticias Económicas")
st.markdown("Esta aplicación extrae datos económicos y genera artículos periodísticos automáticamente.")

# Cargar los datos (usará el caché después de la primera vez)
df, indicadores_dict = cargar_y_procesar_datos()

# Mostrar la tabla de datos en un expander
with st.expander("Ver tabla de datos extraídos"):
    st.dataframe(df)

# Configuración de fecha
fecha_hoy_obj = datetime.now()
meses_es = { 1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio", 7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre" }
fecha_hoy = f"{fecha_hoy_obj.day} de {meses_es[fecha_hoy_obj.month]} de {fecha_hoy_obj.year}"

# Mapeo de opciones para el selectbox a las funciones generadoras
opciones_noticias = {
    "Noticia del Dólar": generar_noticia_dolar,
    "Noticia del ICOLCAP": generar_noticia_icolcap,
    "Resumen Económico General": generar_resumen_economico
}

st.header("Seleccione la noticia que desea generar")
opcion_seleccionada = st.selectbox(
    "Elegir artículo:",
    options=list(opciones_noticias.keys())
)

# Cuando el usuario selecciona una opción, se ejecuta el siguiente bloque
if opcion_seleccionada:
    funcion_generadora = opciones_noticias[opcion_seleccionada]
    
    # Determinar si la función necesita datos individuales o el conjunto completo
    if "Resumen" in opcion_seleccionada:
        # Las funciones de resumen reciben el diccionario completo
        articulo_html = funcion_generadora(indicadores_dict, fecha_hoy)
    else:
        # Las funciones individuales reciben los datos de su indicador específico
        nombre_indicador = opcion_seleccionada.split(" ")[2]
        if nombre_indicador in indicadores_dict:
            datos_indicador = indicadores_dict[nombre_indicador]
            articulo_html = funcion_generadora(datos_indicador, fecha_hoy)
        else:
            articulo_html = f"<p>Error: No se encontraron datos para el indicador '{nombre_indicador}'.</p>"
    
    st.divider()
    # Usamos st.markdown para renderizar el HTML del artículo
    st.markdown(articulo_html, unsafe_allow_html=True)
