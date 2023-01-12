import numpy as np
import pandas as pd
from scipy.integrate import odeint, solve_ivp

from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.models import Slider, Div, ColumnDataSource
from bokeh.layouts import row, column, gridplot

beta=0.6 #ilu ludzi spotyka przemnożone przez prawdopodobieństw0 zarażenia
gamma=0.3 #im mniejsze tym dłużej zaraża
N = 10000
I0=15
S0=N-I0
R0=0
p = (N,beta, gamma)  #parametry
y0 = [S0, I0, R0]  # warunki początkowe
t = np.arange(0.0, 50.0, 0.01)

def sir(t, state, N, beta, gamma):
    S,I,R = state
    dS=-beta*I*S/N
    dI=beta*I*S/N-gamma*I
    dR=gamma*I   
    return [dS, dI, dR]

result = odeint(sir, y0, t, p, tfirst=True)
display = pd.DataFrame({"t" : t, "S" : list(result[:,0]), "I" : list(result[:,1]), "R" : list(result[:,2])})
source = ColumnDataSource(display)

fig = figure(x_axis_label = "czas", y_axis_label = "liczba osób", width = 1000, aspect_ratio = 1.5)
fig.line("t", "S", color = 'slateblue', line_width = 3, source=source, legend_label = 'Podatni')
fig.line("t", "I", color = 'crimson', line_width = 3, source=source, legend_label = 'Zainfekowani')
fig.line("t",  "R", color = 'orchid', line_width = 3, source=source, legend_label = 'Usunięci')
fig.title.text = "SIR"
fig.title.align = "center"
fig.toolbar.autohide = True
fig.background_fill_color = "whitesmoke"

def updateBeta(attr,old,new):
    global beta
    beta = new
    result = odeint(sir, [S0, I0, R0], t, (N,beta, gamma), tfirst=True)
    display = pd.DataFrame({"t" : t, "S" : list(result[:,0]), "I" : list(result[:,1]), "R" : list(result[:,2])})
    source.data = ColumnDataSource.from_df(display)

def updateGamma(attr,old,new):
    global gamma
    gamma = new
    result = odeint(sir, [S0, I0, R0], t, (N,beta, gamma), tfirst=True)
    display = pd.DataFrame({"t" : t, "S" : list(result[:,0]), "I" : list(result[:,1]), "R" : list(result[:,2])})
    source.data = ColumnDataSource.from_df(display)
    
def updateI0(attr,old,new):
    global I0
    I0 = new
    result = odeint(sir, [S0, I0, R0], t, (N,beta, gamma), tfirst=True)
    display = pd.DataFrame({"t" : t, "S" : list(result[:,0]), "I" : list(result[:,1]), "R" : list(result[:,2])})
    source.data = ColumnDataSource.from_df(display)

s_beta = Slider(start = 0, end = 1, step = 0.05, value = beta, title = "Beta", bar_color = 'navy',  background = 'whitesmoke')
s_gamma = Slider(start = 0, end = 1, step = 0.05, value = gamma, title = "Gamma", bar_color = 'navy', background = 'whitesmoke')
s_I0 = Slider(start = 0, end = 100, step = 1, value = I0, title = "Początkowa liczba zainfekowanych", bar_color = 'navy', background = 'whitesmoke')

s_beta.on_change("value",updateBeta)
s_gamma.on_change("value",updateGamma)
s_I0.on_change("value",updateI0)

div = Div(text=r"""
SIR to fajny model:
<p \><p \>
- Zwiększ $$\beta$$, by zarażać więcej osób.
<p \><p \>
- Zmniejsz $$\gamma$$, by zarażać dłużej.
<p \><p \>
- Zobacz jak wpływa na statystykę zmiana liczby początkowo chorych.
""")

curdoc().add_root(row(fig, column(s_beta,s_gamma,s_I0, div)))