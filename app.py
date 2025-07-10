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
# LÓGICA DE EXTRACCIÓN Y PROCESAMIENTO (SIN CACHÉ)
# -----------------------------------------------------------------------------
def cargar_y_procesar_datos():
    """
    Esta función se ejecuta bajo demanda para obtener los datos más recientes.
    """
    # Aquí iría una llamada a requests.get(url) para obtener el HTML en tiempo real.
    # Por ahora, usamos el contenido estático que proporcionaste.
    html_content = """
    <section class="u-estructura-home__seccion"><div class="c-board c-board-indicadores" data-mrf-recirculation="Indicadores"><div class="c-board__header"><h2 class="c-board__header__titulo">INDICADORES</h2><a href="/economia" class="c-board-indicadores__link" data-mrf-link="https://www.eltiempo.com/economia" cmp-ltrk="Indicadores" cmp-ltrk-idx="0" mrfobservableid="f5410de9-fc10-453b-8d21-aa6494e28520">> Más Economía</a></div>    <div class="c-board-indicadores__contenedor">
                                                    <div class="c-board-indicadores__item c-board-indicadores__item--down"><span class="c-board-indicadores__item__titulo">Dólar</span><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">$  4.004,30</span><span class="c-board-indicadores__item__previo">-$ 13,2</span><span class="c-board-indicadores__item__diferencia">-$ 0,33</span></div><div class="c-board-indicadores__item c-board-indicadores__item--down"><span class="c-board-indicadores__item__titulo">TRM</span><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">$  4.026,09</span><span class="c-board-indicadores__item__previo">-$ 28,0398</span><span class="c-board-indicadores__item__diferencia"> </span></div><div class="c-board-indicadores__item c-board-indicadores__item--down"><span class="c-board-indicadores__item__titulo">Euro</span><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">$  4.708,51</span><span class="c-board-indicadores__item__previo">-$ 29,09</span><span class="c-board-indicadores__item__diferencia">-$ 0,62</span></div><div class="c-board-indicadores__item c-board-indicadores__item--up"><span class="c-board-indicadores__item__titulo">Bolívar</span><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">US$  113,466124</span><span class="c-board-indicadores__item__previo">+$ 0,919695</span><span class="c-board-indicadores__item__diferencia">+$ 0,82</span></div><div class="c-board-indicadores__item c-board-indicadores__item--up"><span class="c-board-indicadores__item__titulo">Peso mexicano</span><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">US$  0,463</span><span class="c-board-indicadores__item__previo"> </span><span class="c-board-indicadores__item__diferencia"> </span></div><div class="c-board-indicadores__item c-board-indicadores__item--up"><span class="c-board-indicadores__item__titulo">Café</span><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">US$  287,8</span><span class="c-board-indicadores__item__previo">+$ 1,95</span><span class="c-board-indicadores__item__diferencia">+$ 0,68</span></div><div class="c-board-indicadores__item c-board-indicadores__item--up"><span class="c-board-indicadores__item__titulo">Oro</span><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">US$  3318,3147</span><span class="c-board-indicadores__item__previo">+$ 4,9675</span><span class="c-board-indicadores__item__diferencia">+$ 0,15</span></div><div class="c-board-indicadores__item c-board-indicadores__item--up"><span class="c-board-indicadores__item__titulo">Tasa de usura en Colombia</span><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">24,78  %</span><span class="c-board-indicadores__item__previo"> </span><span class="c-board-indicadores__item__diferencia"> </span></div><div class="c-board-indicadores__item" data-position="9"><div class="c-board-indicadores__item c-board-indicadores__item--up"><span class="c-board-indicadores__item__titulo">Tasa de interés del Banrep</span><div class="c-board-indicadores__item__compress"><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">9,25  %</span></div><span class="c-board-indicadores__item__previo"> </span><span class="c-board-indicadores__item__diferencia"> </span></div><div class="c-board-indicadores__item c-board-indicadores__item--up"><span class="c-board-indicadores__item__titulo">ICOLCAP</span><div class="c-board-indicadores__item__compress"><span class="c-board-indicadores__item__indicador">d</span><span class="c-board-indicadores__item__precio">$  16.660,50</span></div><span class="c-board-indicadores__item__previo">+$ 80,5</span><span class="c-board-indicadores__item__diferencia">+$ 0,49</span></div></div></div></div></section>
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
CONTEXTO_DOLAR = "El valor del dólar frente al peso colombiano es un indicador fundamental para la economía del país. Su fluctuación tiene un impacto directo en el costo de los productos importados, los precios de los tiquetes aéreos, la tecnología y las materias primas. Asimismo, afecta el valor de las exportaciones colombianas, como el petróleo y el café, y el envío de remesas."
CONTEXTO_EURO = "La cotización del euro es un referente clave, especialmente para el comercio con la Unión Europea, uno de los socios comerciales más importantes de Colombia. Su valor influye en las transacciones comerciales, el turismo y las inversiones entre ambas regiones."
CONTEXTO_ICOLCAP = "El MSCI COLCAP es el principal índice de la Bolsa de Valores de Colombia (bvc) y agrupa a las acciones más líquidas y de mayor capitalización bursátil. Su desempeño refleja la confianza de los inversionistas en las grandes empresas del país y en la economía colombiana en general. Una tendencia al alza suele indicar optimismo, mientras que una baja puede señalar preocupación."
CONTEXTO_CAFE = "El café es uno de los productos de exportación más emblemáticos de Colombia. Su precio en los mercados internacionales tiene un impacto directo en la economía de miles de familias caficultoras y en el ingreso de divisas al país. Factores como el clima global, la producción en otros países y la demanda mundial determinan su valor."
CONTEXTO_ORO = "El oro es considerado un 'activo refugio' a nivel mundial. En tiempos de incertidumbre económica o volatilidad en los mercados, los inversionistas tienden a comprar oro para proteger su capital, lo que puede influir en su precio. Por ello, su cotización es un termómetro de la confianza en la economía global."

fuente = "El Tiempo"
attribution_line = f"<i>*Este contenido fue reescrito con la asistencia de una inteligencia artificial, basado en información de {fuente}.</i>"

# --- Funciones generadoras ---
def generar_noticia_dolar(datos, fecha):
    valor, variacion = datos['Valor'], datos['Variacion']
    tendencia_verbo = "registró una baja" if variacion.startswith('-') else "presentó un alza"
    titulo = f"Dólar en Colombia: así cerró la cotización el {fecha}"
    subtitulo = f"La divisa estadounidense {tendencia_verbo} durante la jornada, finalizando con un valor de {valor}."
    return f"""<h1>{titulo}</h1><h2>{subtitulo}</h2><hr><p>El dólar estadounidense finalizó la jornada de negociación del <strong>{fecha}</strong> en Colombia con un valor de <strong>{valor}</strong>. Este resultado representa una modificación de <strong>{variacion} pesos</strong>.</p><h2>Datos clave del dólar hoy</h2><ul><li><strong>Valor de cierre:</strong> {valor}</li><li><strong>Variación diaria:</strong> {variacion}</li><li><strong>Variación porcentual:</strong> {datos['Diferencia_Pct']}%</li></ul><h2>Importancia del dólar en la economía</h2><p>{CONTEXTO_DOLAR}</p>{attribution_line}"""

def generar_noticia_euro(datos, fecha):
    valor, variacion = datos['Valor'], datos['Variacion']
    tendencia_verbo = "registró una baja" if variacion.startswith('-') else "presentó un alza"
    titulo = f"Euro en Colombia: Cotización y cierre para el {fecha}"
    subtitulo = f"La moneda oficial de la Eurozona {tendencia_verbo} en el mercado colombiano, concluyendo la jornada con un valor de {valor}."
    return f"""<h1>{titulo}</h1><h2>{subtitulo}</h2><hr><p>El euro cerró su cotización en Colombia el <strong>{fecha}</strong> a <strong>{valor}</strong>. Este valor implica una variación de <strong>{variacion} pesos</strong>.</p><h2>Cifras del Euro hoy</h2><ul><li><strong>Valor de cierre:</strong> {valor}</li><li><strong>Variación diaria:</strong> {variacion}</li><li><strong>Variación porcentual:</strong> {datos['Diferencia_Pct']}%</li></ul><h2>Relevancia del Euro para Colombia</h2><p>{CONTEXTO_EURO}</p>{attribution_line}"""

def generar_noticia_cafe(datos, fecha):
    valor, variacion = datos['Valor'], datos['Variacion']
    tendencia_verbo = "cerró a la baja" if variacion.startswith('-') else "finalizó al alza"
    titulo = f"Precio del café hoy {fecha}: Así cerró la cotización del grano"
    subtitulo = f"El precio internacional del café {tendencia_verbo} y se ubicó en {valor} por carga."
    return f"""<h1>{titulo}</h1><h2>{subtitulo}</h2><hr><p>El precio de referencia para el café colombiano en los mercados internacionales se fijó en <strong>{valor}</strong> al cierre del <strong>{fecha}</strong>.</p><h2>Datos del café hoy</h2><ul><li><strong>Precio de cierre:</strong> {valor}</li><li><strong>Variación diaria:</strong> {variacion}</li><li><strong>Variación porcentual:</strong> {datos['Diferencia_Pct']}%</li></ul><h2>Contexto del mercado cafetero</h2><p>{CONTEXTO_CAFE}</p>{attribution_line}"""

def generar_noticia_oro(datos, fecha):
    valor, variacion = datos['Valor'], datos['Variacion']
    tendencia_verbo = "retrocedió" if variacion.startswith('-') else "avanzó"
    titulo = f"Oro hoy en Colombia: Valor de la onza para el {fecha}"
    subtitulo = f"El metal precioso {tendencia_verbo} en los mercados, alcanzando un valor de {valor} por onza."
    return f"""<h1>{titulo}</h1><h2>{subtitulo}</h2><hr><p>La cotización internacional del oro finalizó la jornada del <strong>{fecha}</strong> en <strong>{valor}</strong> por onza.</p><h2>Datos del oro hoy</h2><ul><li><strong>Precio de cierre (onza):</strong> {valor}</li><li><strong>Variación diaria:</strong> {variacion}</li><li><strong>Variación porcentual:</strong> {datos['Diferencia_Pct']}%</li></ul><h2>El oro como activo refugio</h2><p>{CONTEXTO_ORO}</p>{attribution_line}"""

def generar_noticia_icolcap(datos, fecha):
    valor, variacion = datos['Valor'].replace('$', '').strip(), datos['Variacion'].replace('$', '').strip()
    tendencia_txt = "a la baja" if variacion.startswith('-') else "al alza"
    titulo = f"Índice MSCI COLCAP: Bolsa de Colombia cierra {tendencia_txt} el {fecha}"
    subtitulo = f"El principal índice bursátil del país concluyó la sesión en {valor} puntos."
    return f"""<h1>{titulo}</h1><h2>{subtitulo}</h2><hr><p>El mercado de acciones colombiano, representado por el índice MSCI COLCAP, concluyó las operaciones del <strong>{fecha}</strong> en <strong>{valor} puntos</strong>.</p><h2>Desempeño del MSCI COLCAP en cifras</h2><ul><li><strong>Puntos de cierre:</strong> {valor}</li><li><strong>Variación en puntos:</strong> {variacion}</li><li><strong>Variación porcentual:</strong> {datos['Diferencia_Pct']}%</li></ul><h2>¿Qué es el MSCI COLCAP?</h2><p>{CONTEXTO_ICOLCAP}</p>{attribution_line}"""

def generar_resumen_economico(datos_completos, fecha):
    dolar_data, icolcap_data, cafe_data = datos_completos.get('Dólar', {}), datos_completos.get('ICOLCAP', {}), datos_completos.get('Café', {})
    titulo = f"Cierre de mercados en Colombia: Resumen de la jornada del {fecha}"
    subtitulo = f"El dólar cerró en {dolar_data.get('Valor', 'N/A')}, el índice MSCI COLCAP se ubicó en {icolcap_data.get('Valor', 'N/A')} y el café finalizó en {cafe_data.get('Valor', 'N/A')}."
    return f"""<h1>{titulo}</h1><h2>{subtitulo}</h2><hr><h2>Mercado Cambiario</h2><p>El <strong>dólar</strong> cerró en <strong>{dolar_data.get('Valor', 'N/A')}</strong>. El <strong>euro</strong> se cotizó en <strong>{datos_completos.get('Euro', {}).get('Valor', 'N/A')}</strong>.</p><h2>Bolsa y Materias Primas</h2><p>El índice <strong>MSCI COLCAP</strong> cerró en <strong>{icolcap_data.get('Valor', 'N/A')}</strong> puntos. El <strong>café</strong> se cotizó en <strong>{cafe_data.get('Valor', 'N/A')}</strong> y el <strong>oro</strong> en <strong>{datos_completos.get('Oro', {}).get('Valor', 'N/A')}</strong>.</p><h2>Tasas de Referencia</h2><p>La tasa de interés del Banco de la República se mantiene en <strong>{datos_completos.get('Tasa de interés del Banrep', {}).get('Valor', 'N/A')}</strong> y la tasa de usura vigente es de <strong>{datos_completos.get('Tasa de usura en Colombia', {}).get('Valor', 'N/A')}</strong>.</p>{attribution_line}"""

# -----------------------------------------------------------------------------
# CONSTRUCCIÓN DE LA INTERFAZ DE USUARIO (UI)
# -----------------------------------------------------------------------------

st.title("📰 Generador de Noticias Económicas")
st.markdown("Esta aplicación extrae datos económicos y genera artículos periodísticos automáticamente.")

# --- LÓGICA DE CONTROL CON SESSION STATE ---
# Inicializar el estado de la sesión si no existe
if 'datos_cargados' not in st.session_state:
    st.session_state.datos_cargados = False
    st.session_state.df = pd.DataFrame()
    st.session_state.indicadores_dict = {}

# Botón para iniciar la extracción de datos
if st.button("📊 Extraer Datos Actualizados"):
    with st.spinner("Extrayendo la información más reciente..."):
        # Llamar a la función de extracción y guardar los datos en el estado de la sesión
        df, indicadores_dict = cargar_y_procesar_datos()
        st.session_state.df = df
        st.session_state.indicadores_dict = indicadores_dict
        st.session_state.datos_cargados = True
        st.success("¡Datos extraídos con éxito!")

# Solo mostrar el resto de la app si los datos han sido cargados
if st.session_state.datos_cargados:
    # Mostrar la tabla de datos en un expander
    with st.expander("Ver tabla de datos extraídos"):
        st.dataframe(st.session_state.df)

    # Configuración de fecha
    fecha_hoy_obj = datetime.now()
    meses_es = { 1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio", 7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre" }
    fecha_hoy = f"{fecha_hoy_obj.day} de {meses_es[fecha_hoy_obj.month]} de {fecha_hoy_obj.year}"

    # --- NUEVA ESTRUCTURA ROBUSTA PARA LAS OPCIONES ---
    # Mapeo de opciones para el selectbox. Asocia un nombre de usuario a una función y una clave de datos.
    opciones_noticias = {
        "Noticia del Dólar":              {'func': generar_noticia_dolar, 'key': 'Dólar'},
        "Noticia del Euro":               {'func': generar_noticia_euro, 'key': 'Euro'},
        "Noticia del ICOLCAP":            {'func': generar_noticia_icolcap, 'key': 'ICOLCAP'},
        "Noticia del Café":               {'func': generar_noticia_cafe, 'key': 'Café'},
        "Noticia del Oro":                {'func': generar_noticia_oro, 'key': 'Oro'},
        "Resumen Económico General":      {'func': generar_resumen_economico, 'key': None} # 'key' es None para resúmenes
    }

    st.header("Seleccione la noticia que desea generar")
    opcion_seleccionada = st.selectbox(
        "Elegir artículo:",
        options=list(opciones_noticias.keys())
    )

    if opcion_seleccionada:
        config = opciones_noticias[opcion_seleccionada]
        funcion_generadora = config['func']
        data_key = config['key']
        
        # Lógica para llamar a la función con los datos correctos
        if data_key is not None: # Es una noticia individual
            if data_key in st.session_state.indicadores_dict:
                datos_indicador = st.session_state.indicadores_dict[data_key]
                articulo_html = funcion_generadora(datos_indicador, fecha_hoy)
            else:
                articulo_html = f"<p>Error: No se encontraron datos para el indicador '{data_key}'.</p>"
        else: # Es una noticia de resumen
            articulo_html = funcion_generadora(st.session_state.indicadores_dict, fecha_hoy)
        
        st.divider()
        st.markdown(articulo_html, unsafe_allow_html=True)
