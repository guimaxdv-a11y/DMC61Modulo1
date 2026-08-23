import streamlit as st
import numpy as np
import pandas as pd

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================
st.set_page_config(page_title="Python for Analytics - Proyecto 1", page_icon="🧠", layout="wide")

# Función  para inicializar session_state
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
    st.title("**Sistema de asistencia del consultorio**")
    st.subheader("Elaborado por: Guillermo Donayre Vásquez")
    st.subheader("Médico Neurólogo - Hospital Regional de Loreto")
    st.subheader("2026")
    st.markdown("---")
   
    ### 📝 Descripción del Proyecto
    Aplicación interactiva que integra los conceptos fundamentales del Módulo 1:
    variables, estructuras de datos, control de flujo, funciones, POO y Streamlit con apoyo de IA

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
# ============================================
# EJERCICIO 1 - FLUJO DE CAJA (VERSIÓN CORREGIDA)
# ============================================
elif modulos == "📊 Ejercicio 1: Flujo de caja":
    # ------------------------------------------------------------
    # PASO 1: Encabezado del módulo
    # ------------------------------------------------------------
    st.subheader("📊 Módulo de Flujo de Caja")
    st.markdown("Registra movimientos financieros (ingresos/gastos) y visualiza el saldo en tiempo real.")

    # ------------------------------------------------------------
    # PASO 2: Inicialización del estado (session_state)
    # ------------------------------------------------------------
    init_state("movimientos", [])           # Lista de movimientos
    init_state("ej1_concepto", "")          # Clave para el concepto
    init_state("ej1_tipo", "Ingreso")       # Clave para el tipo (por defecto "Ingreso")
    init_state("ej1_valor", 0.0)            # Clave para el valor

    # ------------------------------------------------------------
    # PASO 3: Formulario de entrada (3 columnas)
    # ------------------------------------------------------------
    st.markdown("### Registrar nuevo movimiento")
    c1, c2, c3 = st.columns(3)
    with c1:
        # El valor se toma directamente de la clave, sin parámetro value
        concepto = st.text_input(
            "Concepto",
            key="ej1_concepto",
            placeholder="Ej: Consulta médica"
        )
    with c2:
        tipo = st.selectbox(
            "Tipo",
            ["Ingreso", "Gasto"],
            key="ej1_tipo"
        )
    with c3:
        valor = st.number_input(
            "Valor (S/.)",
            min_value=0.0,
            step=0.01,
            format="%.2f",
            key="ej1_valor"
        )

    # ------------------------------------------------------------
    # PASO 4: Botones de acción (Agregar y Limpiar)
    # ------------------------------------------------------------
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        agregar = st.button("➕ Agregar movimiento", use_container_width=True)
    with c_btn2:
        limpiar = st.button("🧹 Limpiar campos", use_container_width=True)

    # ------------------------------------------------------------
    # PASO 5: Lógica del botón "Agregar"
    # ------------------------------------------------------------
    if agregar:
        if concepto.strip() == "" or valor <= 0:
            st.error("⚠️ Ingresa un concepto válido y un valor mayor a 0.")
        else:
            st.session_state.movimientos.append({
                "Concepto": concepto.strip(),
                "Tipo": tipo,
                "Valor": valor
            })
            st.success(f"✅ Movimiento '{concepto}' agregado.")

    # ------------------------------------------------------------
    # PASO 6: Lógica del botón "Limpiar" (CORREGIDO)
    # ------------------------------------------------------------
    if limpiar:
        # Resetear las claves de los widgets directamente
        st.session_state.ej1_concepto = ""
        st.session_state.ej1_tipo = "Ingreso"
        st.session_state.ej1_valor = 0.0
        # No se necesita st.rerun()

    # ------------------------------------------------------------
    # PASO 7: Visualización del historial, estadísticas y reinicio
    # ------------------------------------------------------------
    st.markdown("### Historial de movimientos")
    if st.session_state.movimientos:
        df = pd.DataFrame(st.session_state.movimientos)
        st.dataframe(df, use_container_width=True)

        # Cálculo de totales y saldo
        total_ing = sum(m["Valor"] for m in st.session_state.movimientos if m["Tipo"] == "Ingreso")
        total_gas = sum(m["Valor"] for m in st.session_state.movimientos if m["Tipo"] == "Gasto")
        saldo = total_ing - total_gas

        # Métricas en 3 columnas
        c_m1, c_m2, c_m3 = st.columns(3)
        c_m1.metric("💰 Total Ingresos", f"S/. {total_ing:.2f}")
        c_m2.metric("💸 Total Gastos", f"S/. {total_gas:.2f}")
        c_m3.metric("📈 Saldo Final", f"S/. {saldo:.2f}")

        # Mensaje de estado del flujo
        if saldo > 0:
            st.success(f"✅ Flujo **A FAVOR**: S/. {saldo:.2f}")
        elif saldo < 0:
            st.error(f"❌ Flujo **EN CONTRA**: S/. {abs(saldo):.2f}")
        else:
            st.warning("⚠️ Flujo **EQUILIBRADO** (saldo = 0)")
    else:
        st.info("ℹ️ No hay movimientos registrados.")

    # Botón para reiniciar todo (CORREGIDO)
    if st.button("🗑️ Reiniciar flujo de caja"):
        st.session_state.movimientos = []
        st.session_state.ej1_concepto = ""
        st.session_state.ej1_tipo = "Ingreso"
        st.session_state.ej1_valor = 0.0
        # No se necesita st.rerun()
# ============================================
# EJERCICIO 2 - EXÁMENES DE LABORATORIO 
# ============================================
elif modulos == "📦 Ejercicio 2: Registro de Laboratorio con NumPy":
    # ------------------------------------------------------------
    # PASO 1: Encabezado del módulo
    # ------------------------------------------------------------
    st.subheader("🧪 Módulo de Registro de Exámenes de Laboratorio")
    st.markdown("Registra exámenes de laboratorio usando **arrays de NumPy** y visualízalos como DataFrame.")

    # ------------------------------------------------------------
    # PASO 2: Inicialización de arrays (con NumPy) y claves de widgets
    # ------------------------------------------------------------
    # Arrays para almacenar datos
    for key, dtype in [
        ("arr_paciente", object),
        ("arr_examen", object),
        ("arr_categoria", object),
        ("arr_resultado", float),
        ("arr_referencia", float),
        ("arr_unidad", object),
        ("arr_estado", object)
    ]:
        init_state(key, np.array([], dtype=dtype))

    # Claves de los widgets (para que se puedan resetear)
    for key, default in [
        ("ej2_paciente", ""),
        ("ej2_categoria", "Hematología"),
        ("ej2_examen", "Hemoglobina"),
        ("ej2_unidad", ""),      # Se usará solo como respaldo, pero se actualiza dinámicamente
        ("ej2_resultado", 0.0),
        ("ej2_referencia", 0.0)
    ]:
        init_state(key, default)

    # ------------------------------------------------------------
    # PASO 3: Datos de exámenes (diccionario)
    # ------------------------------------------------------------
    examenes = {
        "Hematología": {
            "items": ["Hemoglobina", "Hematocrito", "Leucocitos", "Plaquetas"],
            "unidades": {
                "Hemoglobina": "g/dL",
                "Hematocrito": "%",
                "Leucocitos": "x10^3/µL",
                "Plaquetas": "x10^3/µL"
            }
        },
        "Química sanguínea": {
            "items": ["Glucosa en ayunas", "HbA1c", "Creatinina", "Ácido úrico"],
            "unidades": {
                "Glucosa en ayunas": "mg/dL",
                "HbA1c": "%",
                "Creatinina": "mg/dL",
                "Ácido úrico": "mg/dL"
            }
        },
        "Perfil lipídico": {
            "items": ["Colesterol total", "HDL", "LDL", "Triglicéridos"],
            "unidades": {k: "mg/dL" for k in ["Colesterol total", "HDL", "LDL", "Triglicéridos"]}
        },
        "Función hepática": {
            "items": ["AST (TGO)", "ALT (TGP)", "Bilirrubina total", "Albúmina"],
            "unidades": {
                "AST (TGO)": "U/L",
                "ALT (TGP)": "U/L",
                "Bilirrubina total": "mg/dL",
                "Albúmina": "g/dL"
            }
        }
    }

    # ------------------------------------------------------------
    # PASO 4: Formulario de entrada (dos filas de 2 columnas)
    # ------------------------------------------------------------
    st.markdown("### Registrar nuevo examen")
    c1, c2 = st.columns(2)
    with c1:
        paciente = st.text_input("👤 Paciente", key="ej2_paciente", placeholder="Ej: Juan Pérez")
        categoria = st.selectbox("📋 Categoría", list(examenes.keys()), key="ej2_categoria")
    with c2:
        # El examen se actualiza según la categoría seleccionada
        examen_opts = examenes[categoria]["items"]
        examen = st.selectbox("🔬 Examen", examen_opts, key="ej2_examen")
        # Unidad: se calcula dinámicamente y no tiene key para evitar conflictos
        unidad = examenes[categoria]["unidades"][examen]
        st.text_input("📏 Unidad", value=unidad, disabled=True)  # Solo lectura

    c3, c4 = st.columns(2)
    with c3:
        resultado = st.number_input("📊 Resultado", min_value=0.0, step=0.01, format="%.2f", key="ej2_resultado")
    with c4:
        referencia = st.number_input("📐 Valor de referencia", min_value=0.0, step=0.01, format="%.2f", key="ej2_referencia")

    # ------------------------------------------------------------
    # PASO 5: Estado automático (según resultado y referencia)
    # ------------------------------------------------------------
    if referencia > 0:
        estado = "Normal" if resultado <= referencia else "Alterado"
        icono = "🟢" if estado == "Normal" else "🔴"
        st.info(f"💡 Estado: **{icono} {estado}**")
    else:
        estado = "Sin evaluar"
        st.warning("⚠️ Ingresa un valor de referencia para evaluar el estado.")

    # ------------------------------------------------------------
    # PASO 6: Botones de acción (Agregar y Limpiar)
    # ------------------------------------------------------------
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        agregar = st.button("➕ Agregar examen", use_container_width=True)
    with c_btn2:
        limpiar = st.button("🧹 Limpiar campos", use_container_width=True)

    # ------------------------------------------------------------
    # PASO 7: Lógica del botón "Agregar"
    # ------------------------------------------------------------
    if agregar:
        if paciente.strip() == "" or resultado <= 0:
            st.error("⚠️ Ingresa paciente y resultado válido.")
        else:
            # Actualizar arrays usando np.append
            st.session_state.arr_paciente = np.append(st.session_state.arr_paciente, paciente.strip())
            st.session_state.arr_examen = np.append(st.session_state.arr_examen, examen)
            st.session_state.arr_categoria = np.append(st.session_state.arr_categoria, categoria)
            st.session_state.arr_resultado = np.append(st.session_state.arr_resultado, resultado)
            st.session_state.arr_referencia = np.append(st.session_state.arr_referencia, referencia)
            st.session_state.arr_unidad = np.append(st.session_state.arr_unidad, unidad)
            st.session_state.arr_estado = np.append(st.session_state.arr_estado, estado)
            st.success(f"✅ Examen '{examen}' registrado.")

    # ------------------------------------------------------------
    # PASO 8: Lógica del botón "Limpiar" 
    # ------------------------------------------------------------
    if limpiar:
        # Resetear las claves de los widgets
        st.session_state.ej2_paciente = ""
        st.session_state.ej2_categoria = "Hematología"
        st.session_state.ej2_examen = "Hemoglobina"
        st.session_state.ej2_resultado = 0.0
        st.session_state.ej2_referencia = 0.0
        # Nota: la unidad no tiene key, se recalcula automáticamente
        # No se necesita st.rerun()

    # ------------------------------------------------------------
    # PASO 9: Visualización de la tabla y estadísticas
    # ------------------------------------------------------------
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

        # Métricas en 5 columnas
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

    # ------------------------------------------------------------
    # PASO 10: Botón "Reiniciar registros" (CORREGIDO)
    # ------------------------------------------------------------
    if st.button("🗑️ Reiniciar registros"):
        # Resetear arrays
        for key in ["arr_paciente", "arr_examen", "arr_categoria", "arr_unidad", "arr_estado"]:
            st.session_state[key] = np.array([], dtype=object)
        for key in ["arr_resultado", "arr_referencia"]:
            st.session_state[key] = np.array([], dtype=float)
        # Resetear también los widgets
        st.session_state.ej2_paciente = ""
        st.session_state.ej2_categoria = "Hematología"
        st.session_state.ej2_examen = "Hemoglobina"
        st.session_state.ej2_resultado = 0.0
        st.session_state.ej2_referencia = 0.0
        # No se necesita st.rerun()

# ============================================
# EJERCICIOS 3 Y 4 (PENDIENTES)
# ============================================
elif modulos == "🔧 Ejercicio 3: Funciones externas":
    st.subheader("🔧 Módulo de Funciones desde Librería Externa")
    st.info("ℹ️ Próximamente: Requiere revisar `libreria_funciones_proyecto1.py`")

elif modulos == "🗂️ Ejercicio 4: Clases y CRUD":
    st.subheader("🗂️ Módulo de Clases y Operaciones CRUD")
    st.info("ℹ️ Próximamente: Requiere revisar `libreria_clases_proyecto1.py`")
