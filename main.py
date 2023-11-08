# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 09:38:58 2023

@author: L3PC12
"""

import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Listas de coordenadas x, y e duração das fixações
coordenadas_x = [200, 300, 400, 300, 500]
coordenadas_y = [100, 200, 300, 400, 500]
duracao_fixacoes = [100, 200, 50, 150, 300]

# Tamanho da imagem (resolução)
largura, altura = 800, 600

# Crie uma matriz vazia para o heatmap
heatmap = np.zeros((altura, largura))

# Crie o heatmap com base nas coordenadas e durações das fixações
for x, y, duracao in zip(coordenadas_x, coordenadas_y, duracao_fixacoes):
    # Normalize a duração para um valor entre 0 e 1
    tamanho_fixacao = duracao / max(duracao_fixacoes)

    # Crie uma matriz de máscara com base no tamanho da fixação
    tamanho_mascara = int(tamanho_fixacao * 25)
    mascara = np.ones((2 * tamanho_mascara + 1, 2 * tamanho_mascara + 1))

    # Calcule as coordenadas na matriz de heatmap
    x_min, x_max = max(0, x - tamanho_mascara), min(largura, x + tamanho_mascara + 1)
    y_min, y_max = max(0, y - tamanho_mascara), min(altura, y + tamanho_mascara + 1)

    # Aplique a máscara à região do heatmap correspondente às coordenadas
    heatmap[y_min:y_max, x_min:x_max] += tamanho_fixacao * mascara

# Normalize os valores para que estejam no intervalo [0, 1]
heatmap = heatmap / heatmap.max()

# Crie um aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div([
    dcc.Graph(
        id='heatmap',
        figure=px.imshow(heatmap, color_continuous_scale='hot', origin='lower')
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
