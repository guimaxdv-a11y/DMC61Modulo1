import streamlit as st
import numpy as np
import pandas as pd

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================
st.set_page_config(page_title="Python for Analytics - Proyecto 1", page_icon="🧠", layout="wide")

# Función auxiliar para inicializar session_state
def init_state(key, default):
    if key not in st.session_state:
        st.session_state[key] = default

# Inicializar selección del módulo (HOME por defecto)
init_state("modulo_seleccionado", "🏠 Home")

opciones_menu = ["🏠 Home", "📊 Ejercicio 1: Flujo de caja", "📦 Ejercicio 2: Registro de Laboratorio con NumPy",
                 "🔧 Ejercicio 3: Funciones externas", "🗂️ Ejercicio 4: Clases y CRUD"]

# ============================================
# SIDEBAR
# ============================================
st.sidebar.image("Neurolab solo logo.png", use_container_width=True)
st.sidebar.subheader("📋 Menú de Ejercicios")

if st.sidebar.button("🏠 Volver al inicio", use_container_width=True):
    st.session_state.modulo_seleccionado = "🏠 Home"
    st.rerun()
modulos = st.sidebar.selectbox(
    "Seleccione un módulo", opciones_menu,
    key="modulo_seleccionado",
    index=opciones_menu.index(st.session_state.modulo_seleccionado)
)
# ============================================
# HOME
# ============================================
if modulos == "🏠 Home":
    st.title("Desarrollo del aprendizaje en Python for Analytics")
    st.subheader("Módulo 1 – Python Fundamentals")
    st.markdown("**Sistema de asistencia del consultorio**")
    st.header("Elaborado por: Guillermo Donayre Vásquez")
    st.subheader("Médico Neurólogo - Hospital Regional de Loreto")
    st.subheader("2026")
    st.markdown("---")
    st.markdown("""
    ### 📝 Descripción del Proyecto
    Aplicación interactiva que integra los conceptos fundamentales del Módulo 1:
    variables, estructuras de datos, control de flujo, funciones, POO y Streamlit.

    ### 🛠️ Tecnologías utilizadas
    - **Python 3.x** | **Streamlit** | **NumPy** | **Pandas**

    ### 📋 Estructura
    1. **📊 Ejercicio 1**: Flujo de caja con listas
    2. **📦 Ejercicio 2**: Registro con NumPy, arrays y DataFrame
    3. **🔧 Ejercicio 3**: Uso de funciones desde librería externa
    4. **🗂️ Ejercicio 4**: Uso de clases con operaciones CRUD
    """)

# ============================================
# EJERCICIO 1 - FLUJO DE CAJA
# ============================================
elif modulos == "📊 Ejercicio 1: Flujo de caja":
    st.subheader("📊 Módulo de Flujo de Caja")
    st.markdown("Registra movimientos financieros (ingresos/gastos) y visualiza el saldo en tiempo real.")

    init_state("movimientos", [])
    init_state("ej1_campos", {"concepto": "", "tipo": "Ingreso", "valor": 0.0})

    st.markdown("### Registrar nuevo movimiento")
    c1, c2, c3 = st.columns(3)
    with c1:
        concepto = st.text_input("Concepto", value=st.session_state.ej1_campos["concepto"],
                                 key="ej1_concepto", placeholder="Ej: Consulta médica")
    with c2:
        tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"], key="ej1_tipo")
    with c3:
        valor = st.number_input("Valor (S/.)", min_value=0.0, step=0.01, format="%.2f",
                                value=st.session_state.ej1_campos["valor"], key="ej1_valor")

    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        agregar = st.button("➕ Agregar movimiento", use_container_width=True)
    with c_btn2:
        limpiar = st.button("🧹 Limpiar campos", use_container_width=True)

    if agregar:
        if concepto.strip() == "" or valor <= 0:
            st.error("⚠️ Ingresa un concepto válido y un valor mayor a 0.")
        else:
            st.session_state.movimientos.append({"Concepto": concepto.strip(), "Tipo": tipo, "Valor": valor})
            st.success(f"✅ Movimiento '{concepto}' agregado.")

    if limpiar:
        st.session_state.ej1_campos = {"concepto": "", "tipo": "Ingreso", "valor": 0.0}
        st.rerun()

    st.markdown("### Historial de movimientos")
    if st.session_state.movimientos:
        df = pd.DataFrame(st.session_state.movimientos)
        st.dataframe(df, use_container_width=True)

        total_ing = sum(m["Valor"] for m in st.session_state.movimientos if m["Tipo"] == "Ingreso")
        total_gas = sum(m["Valor"] for m in st.session_state.movimientos if m["Tipo"] == "Gasto")
        saldo = total_ing - total_gas

        c_m1, c_m2, c_m3 = st.columns(3)
        c_m1.metric("💰 Total Ingresos", f"S/. {total_ing:.2f}")
        c_m2.metric("💸 Total Gastos", f"S/. {total_gas:.2f}")
        c_m3.metric("📈 Saldo Final", f"S/. {saldo:.2f}")

        if saldo > 0:
            st.success(f"✅ Flujo **A FAVOR**: S/. {saldo:.2f}")
        elif saldo < 0:
            st.error(f"❌ Flujo **EN CONTRA**: S/. {abs(saldo):.2f}")
        else:
            st.warning("⚠️ Flujo **EQUILIBRADO** (saldo = 0)")
    else:
        st.info("ℹ️ No hay movimientos registrados.")

    if st.button("🗑️ Reiniciar flujo de caja"):
        st.session_state.movimientos = []
        st.session_state.ej1_campos = {"concepto": "", "tipo": "Ingreso", "valor": 0.0}
        st.rerun()

# ============================================
# EJERCICIO 2 - EXÁMENES DE LABORATORIO
# ============================================
elif modulos == "📦 Ejercicio 2: Registro con NumPy":
    st.subheader("🧪 Módulo de Registro de Exámenes de Laboratorio")
    st.markdown("Registra exámenes de laboratorio usando **arrays de NumPy** y visualízalos como DataFrame.")

    # Inicializar arrays
    for key, dtype in [("arr_paciente", object), ("arr_examen", object), ("arr_categoria", object),
                       ("arr_resultado", float), ("arr_referencia", float),
                       ("arr_unidad", object), ("arr_estado", object)]:
        init_state(key, np.array([], dtype=dtype))

    # Datos de exámenes (versión simplificada)
    examenes = {
        "Hematología": {"items": ["Hemoglobina", "Hematocrito", "Leucocitos", "Plaquetas"],
                        "unidades": {"Hemoglobina": "g/dL", "Hematocrito": "%",
                                     "Leucocitos": "x10^3/µL", "Plaquetas": "x10^3/µL"}},
        "Química sanguínea": {"items": ["Glucosa en ayunas", "HbA1c", "Creatinina", "Ácido úrico"],
                              "unidades": {"Glucosa en ayunas": "mg/dL", "HbA1c": "%",
                                           "Creatinina": "mg/dL", "Ácido úrico": "mg/dL"}},
        "Perfil lipídico": {"items": ["Colesterol total", "HDL", "LDL", "Triglicéridos"],
                            "unidades": {k: "mg/dL" for k in ["Colesterol total", "HDL", "LDL", "Triglicéridos"]}},
        "Función hepática": {"items": ["AST (TGO)", "ALT (TGP)", "Bilirrubina total", "Albúmina"],
                             "unidades": {"AST (TGO)": "U/L", "ALT (TGP)": "U/L",
                                          "Bilirrubina total": "mg/dL", "Albúmina": "g/dL"}}
    }

    st.markdown("### Registrar nuevo examen")
    c1, c2 = st.columns(2)
    with c1:
        paciente = st.text_input("👤 Paciente", key="ej2_paciente", placeholder="Ej: Juan Pérez")
        categoria = st.selectbox("📋 Categoría", list(examenes.keys()), key="ej2_categoria")
    with c2:
        examen_opts = examenes[categoria]["items"]
        examen = st.selectbox("🔬 Examen", examen_opts, key="ej2_examen")
        unidad = st.text_input("📏 Unidad", value=examenes[categoria]["unidades"][examen], key="ej2_unidad")

    c3, c4 = st.columns(2)
    with c3:
        resultado = st.number_input("📊 Resultado", min_value=0.0, step=0.01, format="%.2f", key="ej2_resultado")
    with c4:
        referencia = st.number_input("📐 Valor de referencia", min_value=0.0, step=0.01, format="%.2f", key="ej2_referencia")

    # Estado automático
    if referencia > 0:
        estado = "Normal" if resultado <= referencia else "Alterado"
        icono = "🟢" if estado == "Normal" else "🔴"
        st.info(f"💡 Estado: **{icono} {estado}**")
    else:
        estado = "Sin evaluar"

    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        agregar = st.button("➕ Agregar examen", use_container_width=True)
    with c_btn2:
        limpiar = st.button("🧹 Limpiar campos", use_container_width=True)

    if agregar:
        if paciente.strip() == "" or resultado <= 0:
            st.error("⚠️ Ingresa paciente y resultado válido.")
        else:
            st.session_state.arr_paciente = np.append(st.session_state.arr_paciente, paciente.strip())
            st.session_state.arr_examen = np.append(st.session_state.arr_examen, examen)
            st.session_state.arr_categoria = np.append(st.session_state.arr_categoria, categoria)
            st.session_state.arr_resultado = np.append(st.session_state.arr_resultado, resultado)
            st.session_state.arr_referencia = np.append(st.session_state.arr_referencia, referencia)
            st.session_state.arr_unidad = np.append(st.session_state.arr_unidad, unidad)
            st.session_state.arr_estado = np.append(st.session_state.arr_estado, estado)
            st.success(f"✅ Examen '{examen}' registrado.")

    if limpiar:
        st.rerun()

    st.markdown("### Tabla de exámenes (DataFrame)")
    if len(st.session_state.arr_paciente) > 0:
        df = pd.DataFrame({
            "Paciente": st.session_state.arr_paciente,
            "Examen": st.session_state.arr_examen,
            "Categoría": st.session_state.arr_categoria,
            "Resultado": st.session_state.arr_resultado,
            "Referencia": st.session_state.arr_referencia,
            "Unidad": st.session_state.arr_unidad,
            "Estado": st.session_state.arr_estado
        })
        st.dataframe(df, use_container_width=True)

        # Métricas
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("🔬 Exámenes", len(st.session_state.arr_paciente))
        c2.metric("👥 Pacientes", len(np.unique(st.session_state.arr_paciente)))
        c3.metric("🟢 Normales", int(np.sum(st.session_state.arr_estado == "Normal")))
        c4.metric("🔴 Alterados", int(np.sum(st.session_state.arr_estado == "Alterado")))
        c5.metric("📊 Promedio", f"{np.mean(st.session_state.arr_resultado):.2f}")

        # Análisis por categoría
        st.markdown("### Análisis por categoría")
        for cat in np.unique(st.session_state.arr_categoria):
            mask = st.session_state.arr_categoria == cat
            st.write(f"- **{cat}**: {int(np.sum(mask))} exámenes | "
                     f"Alterados: {int(np.sum((mask) & (st.session_state.arr_estado == 'Alterado')))} | "
                     f"Promedio: {np.mean(st.session_state.arr_resultado[mask]):.2f}")

        # Análisis por paciente
        st.markdown("### Análisis por paciente")
        for pac in np.unique(st.session_state.arr_paciente):
            mask = st.session_state.arr_paciente == pac
            st.write(f"- **{pac}**: {int(np.sum(mask))} exámenes | "
                     f"Alterados: {int(np.sum((mask) & (st.session_state.arr_estado == 'Alterado')))}")
    else:
        st.info("ℹ️ No hay exámenes registrados.")

    if st.button("🗑️ Reiniciar registros"):
        for key in ["arr_paciente", "arr_examen", "arr_categoria", "arr_unidad", "arr_estado"]:
            st.session_state[key] = np.array([], dtype=object)
        for key in ["arr_resultado", "arr_referencia"]:
            st.session_state[key] = np.array([], dtype=float)
        st.rerun()

# ============================================
# EJERCICIOS 3 Y 4 (PENDIENTES)
# ============================================
elif modulos == "🔧 Ejercicio 3: Funciones externas":
    st.subheader("🔧 Módulo de Funciones desde Librería Externa")
    st.info("ℹ️ Próximamente: Requiere revisar `libreria_funciones_proyecto1.py`")

elif modulos == "🗂️ Ejercicio 4: Clases y CRUD":
    st.subheader("🗂️ Módulo de Clases y Operaciones CRUD")
    st.info("ℹ️ Próximamente: Requiere revisar `libreria_clases_proyecto1.py`")
