import streamlit as st
import numpy as np
import pandas as pd
import libreria_funciones_proyecto1 as lf

st.title("Desarrollo del aprendizaje en Python for Analytics")
st.subheader("Módulo 1 – Python Fundamentals")
st.header("Elaborado por: Guillermo Donayre Vásquez")
st.subheader("Medico Neurólogo - Hospital Regional de Loreto")
st.subheader("2026")

st.sidebar.image("Neurolab solo logo.png")
st.sidebar.title("Ejercicios")



modulos = st.sidebar.selectbox ("Selecione un Modulo", ["Ejercicio 1: Flujo de caja", "Ejercicio 2: Registro de pacientes", "Ejercicio 3", "Ejercicio 4"])

if modulos == "Módulo Listas":
  
  st.write("Bienvenido al módulo Listas")
  
  valor_inicial = st.number_input("Ingrese el valor inicial")
  valor_final = st.number_input("Ingrese el valor final")
  
  lista_numeros = list(range(int(valor_inicial), int(valor_final)))
  st.write(lista_numeros)
  
elif modulos == "Módulo Arreglos":
  
  st.write("Bienvenido al módulo de Arreglos")

  cantidad_elementos = st.slider("Selecione la cantidad de elementos de su arreglo", 1,100)
  cantidad_arreglo= np.arange(cantidad_elementos)
  st.write(cantidad_arreglo)

elif modulos == "Archivos":
  
  archivo = st.sidebar.file_uploader("Seleccione su archivo")

  if archivo is not None:
    st.write("Su archivo ha sido cargado")

    if archivo.name.endswith(".csv"):
      datos = pd.read_csv(archivo)
      st.write(datos)
    elif archivo.name.endswith(".xlsx"):
      datos = pd.read_excel(archivo)
      st.write(datos)

  else:
    st.write("Cargue su archivo")





else:
  
  st.write("Bienvenido al módulo de Funciones")

  capital_inicial = st.number_input("Capital inicial", min_value=0.0, value=1000.0)
  tiempo_meses = st.number_input("Tiempo en meses", min_value=1, value=12)
  tasa_porcentaje = st.number_input("Tasa de interés anual (%)", min_value=0.0, value=0.05)

  resultado_interes_simple = lf.interes_simple(capital_inicial, tiempo_meses,tasa_porcentaje )
  st.write(resultado_interes_simple)

  
