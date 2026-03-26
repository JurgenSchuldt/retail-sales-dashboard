# Retail Sales Analytics Dashboard

Dashboard interactivo de análisis de ventas retail construido con Python y Streamlit.

Live demo: https://jurgenschuldt-retail-sales-dashboard.streamlit.app/

## Qué hace

Analiza más de 800,000 transacciones reales de una tienda online del Reino Unido entre 2009 y 2011. Permite explorar la evolución de ingresos, identificar los productos más rentables y segmentar clientes usando RFM.

## Funcionalidades

- KPIs en tiempo real: ingresos, clientes únicos, pedidos y ticket medio
- Evolución de ingresos mensual filtrable por año y país
- Top 10 productos por ingresos
- Ventas por país
- Segmentación RFM: Champions, Loyal, Recent, At Risk, Lost

## Tecnologías usadas

- Python 3.12
- pandas
- Plotly
- Streamlit
- Dataset: Online Retail II — UCI Machine Learning Repository

## Cómo ejecutarlo

git clone https://github.com/JurgenSchuldt/retail-sales-dashboard.git
cd retail-sales-dashboard
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py