import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def cargar_archivo():
    uploaded_file = st.file_uploader("Cargar archivo de registro sísmico", type=["txt"])
    if uploaded_file is not None:
        data = np.genfromtxt(uploaded_file, skip_header=37)
        st.success("Archivo cargado correctamente")
        return data, uploaded_file.name
    return None, None

import plotly.graph_objects as go

def generar_grafico(data, t_init, t_duration, file_name):
    dt = data[1, 0]
    t_init_index = int(t_init / dt)
    t_end = t_init + t_duration
    t_end_index = int(t_end / dt)

    t = data[t_init_index:t_end_index, 0]
    xg = data[t_init_index:t_end_index, 1]    # EW
    xg1 = data[t_init_index:t_end_index, 2]   # NS
    xg2 = data[t_init_index:t_end_index, 3]   # UD

    max_index1 = np.argmax(np.abs(xg))
    max_index2 = np.argmax(np.abs(xg1))
    max_index3 = np.argmax(np.abs(xg2))
    max1 = f"PGA = {round(max(abs(xg)), 2)} cm/s²"
    max2 = f"PGA = {round(max(abs(xg1)), 2)} cm/s²"
    max3 = f"PGA = {round(max(abs(xg2)), 2)} cm/s²"

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=t, y=xg, mode='lines', name='EW', line=dict(color='red')))
    fig1.add_trace(go.Scatter(x=[t[max_index1]], y=[xg[max_index1]], mode='markers+text', text=[max1], textposition='top right', name='Max EW', marker=dict(color='black')))
    fig1.update_layout(title=f'{file_name[:-4]} - EW', xaxis_title='Time (s)', yaxis_title='$S_a (cm/s^2)$', showlegend=True)
    st.plotly_chart(fig1)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=t, y=xg1, mode='lines', name='NS', line=dict(color='blue')))
    fig2.add_trace(go.Scatter(x=[t[max_index2]], y=[xg1[max_index2]], mode='markers+text', text=[max2], textposition='top right', name='Max NS', marker=dict(color='black')))
    fig2.update_layout(title=f'{file_name[:-4]} - NS', xaxis_title='Time (s)', yaxis_title='$S_a (cm/s^2)$', showlegend=True)
    st.plotly_chart(fig2)

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=t, y=xg2, mode='lines', name='UD', line=dict(color='green')))
    fig3.add_trace(go.Scatter(x=[t[max_index3]], y=[xg2[max_index3]], mode='markers+text', text=[max3], textposition='top right', name='Max UD', marker=dict(color='black')))
    fig3.update_layout(title=f'{file_name[:-4]} - UD', xaxis_title='Time (s)', yaxis_title='$S_a (cm/s^2)$', showlegend=True)
    st.plotly_chart(fig3)

# Streamlit UI
st.title("Generador de Gráfico de Registro Sísmico")

data, file_name = cargar_archivo()

if data is not None:
    t_init = st.number_input("Tiempo Inicial (seg)", min_value=0.0, value=15.0, step=0.1)
    t_duration = st.number_input("Tiempo Duración (seg)", min_value=0.1, value=30.0, step=0.1)
    
    if st.button("Generar Gráfico"):
        generar_grafico(data, t_init, t_duration, file_name)
