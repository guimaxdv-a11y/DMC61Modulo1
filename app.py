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
st.markdown("Bienvenidos al sistema de asistencia del consultorio")



modulos = st.sidebar.selectbox ("Selecione un Modulo", ["Ejercicio 1: Flujo de caja", "Ejercicio 2: Registro de pacientes", "Ejercicio 3", "Ejercicio 4"])

import streamlit as st
import pandas as pd

# ============================================
# EJERCICIO 1: FLUJO DE CAJA CON LISTAS
# ============================================

st.subheader("📊 Módulo de Flujo de Caja")
st.markdown("""
En este módulo podrás registrar movimientos financieros (ingresos y gastos) 
y visualizar el estado actual de tu flujo de caja en tiempo real.
""")

# Inicializar la lista de movimientos en session_state
if "movimientos" not in st.session_state:
    st.session_state.movimientos = []

# Widgets de entrada
st.markdown("### Registrar nuevo movimiento")

col1, col2, col3 = st.columns(3)

with col1:
    concepto = st.text_input("Concepto", placeholder="Ej: Consulta médica")

with col2:
    tipo = st.selectbox("Tipo de movimiento", ["Ingreso", "Gasto"])

with col3:
    valor = st.number_input("Valor (S/.)", min_value=0.0, step=0.01, format="%.2f")

# Botón para agregar movimiento
if st.button("➕ Agregar movimiento"):
    if concepto == "" or valor <= 0:
        st.error("⚠️ Por favor, ingresa un concepto válido y un valor mayor a 0.")
    else:
        nuevo_movimiento = {
            "Concepto": concepto,
            "Tipo": tipo,
            "Valor": valor
        }
        st.session_state.movimientos.append(nuevo_movimiento)
        st.success(f"✅ Movimiento '{concepto}' agregado correctamente.")

# Mostrar tabla de movimientos
st.markdown("### Historial de movimientos")

if len(st.session_state.movimientos) > 0:
    df_movimientos = pd.DataFrame(st.session_state.movimientos)
    st.dataframe(df_movimientos, use_container_width=True)

    # Cálculos
    total_ingresos = sum(m["Valor"] for m in st.session_state.movimientos if m["Tipo"] == "Ingreso")
    total_gastos = sum(m["Valor"] for m in st.session_state.movimientos if m["Tipo"] == "Gasto")
    saldo_final = total_ingresos - total_gastos

    # Métricas
    st.markdown("### Resumen financiero")
    col_m1, col_m2, col_m3 = st.columns(3)

    with col_m1:
        st.metric("💰 Total Ingresos", f"S/. {total_ingresos:.2f}")

    with col_m2:
        st.metric("💸 Total Gastos", f"S/. {total_gastos:.2f}")

    with col_m3:
        st.metric("📈 Saldo Final", f"S/. {saldo_final:.2f}")

    # Estado del flujo de caja
    st.markdown("### Estado del flujo de caja")
    if saldo_final > 0:
        st.success(f"✅ El flujo de caja está **A FAVOR** con un saldo de S/. {saldo_final:.2f}")
    elif saldo_final < 0:
        st.error(f"❌ El flujo de caja está **EN CONTRA** con un déficit de S/. {abs(saldo_final):.2f}")
    else:
        st.warning("⚠️ El flujo de caja está **EQUILIBRADO** (saldo = 0)")

else:
    st.info("ℹ️ Aún no has registrado movimientos. Comienza agregando uno arriba.")

# Botón para reiniciar
if st.button("🗑️ Reiniciar flujo de caja"):
    st.session_state.movimientos = []
    st.rerun()

  
