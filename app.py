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

modulos = st.sidebar.selectbox ("Selecione un Modulo", ["Ejercicio 1: Flujo de caja", "Ejercicio 2: Registro de Laboratorio", "Ejercicio 3", "Ejercicio 4"])


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


# ============================================
# EJERCICIO 2: REGISTRO DE EXÁMENES DE LABORATORIO
# CON NUMPY, ARRAYS Y DATAFRAME
# ============================================

st.subheader("🧪 Módulo de Registro de Exámenes de Laboratorio")
st.markdown("""
En este módulo podrás registrar **exámenes de laboratorio** de pacientes utilizando 
**arreglos de NumPy** como estructura de almacenamiento. Cada registro se convierte 
luego en un **DataFrame** para su visualización y análisis clínico.
""")

# ----------------------------------------------------
# Inicialización de arrays en session_state
# ----------------------------------------------------
if "arr_paciente" not in st.session_state:
    st.session_state.arr_paciente = np.array([], dtype=object)
if "arr_examen" not in st.session_state:
    st.session_state.arr_examen = np.array([], dtype=object)
if "arr_categoria" not in st.session_state:
    st.session_state.arr_categoria = np.array([], dtype=object)
if "arr_resultado" not in st.session_state:
    st.session_state.arr_resultado = np.array([], dtype=float)
if "arr_referencia" not in st.session_state:
    st.session_state.arr_referencia = np.array([], dtype=float)
if "arr_unidad" not in st.session_state:
    st.session_state.arr_unidad = np.array([], dtype=object)
if "arr_estado" not in st.session_state:
    st.session_state.arr_estado = np.array([], dtype=object)

# Valores para los widgets (permite limpiarlos)
if "lab_paciente" not in st.session_state:
    st.session_state.lab_paciente = ""
if "lab_examen" not in st.session_state:
    st.session_state.lab_examen = "Glucosa en ayunas"
if "lab_categoria" not in st.session_state:
    st.session_state.lab_categoria = "Química sanguínea"
if "lab_resultado" not in st.session_state:
    st.session_state.lab_resultado = 0.0
if "lab_referencia" not in st.session_state:
    st.session_state.lab_referencia = 0.0
if "lab_unidad" not in st.session_state:
    st.session_state.lab_unidad = "mg/dL"

# ----------------------------------------------------
# Formulario de ingreso
# ----------------------------------------------------
st.markdown("### Registrar nuevo examen de laboratorio")

categorias_examen = [
    "Hematología",
    "Química sanguínea",
    "Perfil lipídico",
    "Examen de orina",
    "Marcadores inflamatorios",
    "Función hepática",
    "Función renal",
    "Electrolitos"
]

examenes_sugeridos = {
    "Hematología": ["Hemoglobina", "Hematocrito", "Leucocitos", "Plaquetas"],
    "Química sanguínea": ["Glucosa en ayunas", "HbA1c", "Urea", "Creatinina", "Ácido úrico"],
    "Perfil lipídico": ["Colesterol total", "HDL", "LDL", "Triglicéridos"],
    "Examen de orina": ["Proteínas en orina", "Glucosa en orina", "Densidad"],
    "Marcadores inflamatorios": ["PCR", "VSG", "Procalcitonina"],
    "Función hepática": ["AST (TGO)", "ALT (TGP)", "Bilirrubina total", "Albúmina"],
    "Función renal": ["Depuración de creatinina", "Microalbuminuria"],
    "Electrolitos": ["Sodio", "Potasio", "Calcio", "Magnesio"]
}

unidades_sugeridas = {
    "Hemoglobina": "g/dL", "Hematocrito": "%", "Leucocitos": "x10^3/µL",
    "Plaquetas": "x10^3/µL", "Glucosa en ayunas": "mg/dL", "HbA1c": "%",
    "Urea": "mg/dL", "Creatinina": "mg/dL", "Ácido úrico": "mg/dL",
    "Colesterol total": "mg/dL", "HDL": "mg/dL", "LDL": "mg/dL",
    "Triglicéridos": "mg/dL", "PCR": "mg/L", "VSG": "mm/h",
    "AST (TGO)": "U/L", "ALT (TGP)": "U/L", "Bilirrubina total": "mg/dL",
    "Albúmina": "g/dL", "Sodio": "mEq/L", "Potasio": "mEq/L",
    "Calcio": "mg/dL", "Magnesio": "mg/dL"
}

col1, col2 = st.columns(2)

with col1:
    paciente = st.text_input(
        "👤 Nombre del paciente",
        value=st.session_state.lab_paciente,
        key="input_paciente_lab",
        placeholder="Ej: Juan Pérez García"
    )
    categoria = st.selectbox(
        "📋 Categoría del examen",
        categorias_examen,
        index=categorias_examen.index(st.session_state.lab_categoria),
        key="input_categoria_lab"
    )

with col2:
    # Lista de exámenes según la categoría seleccionada
    examenes_disponibles = examenes_sugeridos.get(categoria, ["Otro"])
    if st.session_state.lab_examen not in examenes_disponibles:
        st.session_state.lab_examen = examenes_disponibles[0]

    examen = st.selectbox(
        "🔬 Tipo de examen",
        examenes_disponibles,
        index=examenes_disponibles.index(st.session_state.lab_examen),
        key="input_examen_lab"
    )

    # Unidad sugerida según el examen
    unidad_sugerida = unidades_sugeridas.get(examen, "UI")
    unidad = st.text_input(
        "📏 Unidad de medida",
        value=unidad_sugerida,
        key="input_unidad_lab"
    )

col3, col4 = st.columns(2)

with col3:
    resultado = st.number_input(
        "📊 Resultado obtenido",
        min_value=0.0,
        step=0.01,
        format="%.2f",
        value=st.session_state.lab_resultado,
        key="input_resultado_lab"
    )

with col4:
    referencia = st.number_input(
        "📐 Valor de referencia (límite superior)",
        min_value=0.0,
        step=0.01,
        format="%.2f",
        value=st.session_state.lab_referencia,
        key="input_referencia_lab"
    )

# Determinar estado automáticamente
if referencia > 0:
    if resultado <= referencia:
        estado = "Normal"
        color_estado = "🟢"
    else:
        estado = "Alterado"
        color_estado = "🔴"
    st.info(f"💡 Estado calculado automáticamente: **{color_estado} {estado}** (resultado vs. valor de referencia)")
else:
    estado = "Sin evaluar"
    color_estado = "⚪"

# ----------------------------------------------------
# Botones de acción
# ----------------------------------------------------
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    agregar = st.button("➕ Agregar examen", use_container_width=True)

with col_btn2:
    limpiar = st.button("🧹 Limpiar campos", use_container_width=True)

# Acción: Agregar examen a los arrays
if agregar:
    if paciente.strip() == "" or resultado <= 0:
        st.error("⚠️ Por favor, ingresa el nombre del paciente y un resultado válido.")
    else:
        # Agregar valores a cada array de NumPy
        st.session_state.arr_paciente = np.append(st.session_state.arr_paciente, paciente.strip())
        st.session_state.arr_examen = np.append(st.session_state.arr_examen, examen)
        st.session_state.arr_categoria = np.append(st.session_state.arr_categoria, categoria)
        st.session_state.arr_resultado = np.append(st.session_state.arr_resultado, resultado)
        st.session_state.arr_referencia = np.append(st.session_state.arr_referencia, referencia)
        st.session_state.arr_unidad = np.append(st.session_state.arr_unidad, unidad)
        st.session_state.arr_estado = np.append(st.session_state.arr_estado, estado)

        st.success(f"✅ Examen '{examen}' del paciente '{paciente}' registrado correctamente.")

# Acción: Limpiar campos
if limpiar:
    st.session_state.lab_paciente = ""
    st.session_state.lab_examen = "Glucosa en ayunas"
    st.session_state.lab_categoria = "Química sanguínea"
    st.session_state.lab_resultado = 0.0
    st.session_state.lab_referencia = 0.0
    st.session_state.lab_unidad = "mg/dL"
    st.info("🧹 Campos limpiados. Puedes ingresar un nuevo examen.")
    st.rerun()

# ----------------------------------------------------
# Mostrar DataFrame construido desde los arrays
# ----------------------------------------------------
st.markdown("### Tabla de exámenes registrados (DataFrame)")

if len(st.session_state.arr_paciente) > 0:
    # Construir DataFrame desde los arrays de NumPy
    df_examenes = pd.DataFrame({
        "Paciente": st.session_state.arr_paciente,
        "Examen": st.session_state.arr_examen,
        "Categoría": st.session_state.arr_categoria,
        "Resultado": st.session_state.arr_resultado,
        "Referencia": st.session_state.arr_referencia,
        "Unidad": st.session_state.arr_unidad,
        "Estado": st.session_state.arr_estado
    })

    st.dataframe(df_examenes, use_container_width=True)

    # ----------------------------------------------------
    # Métricas y análisis con NumPy
    # ----------------------------------------------------
    st.markdown("### Resumen del laboratorio")

    total_examenes = len(st.session_state.arr_paciente)
    examenes_normales = int(np.sum(st.session_state.arr_estado == "Normal"))
    examenes_alterados = int(np.sum(st.session_state.arr_estado == "Alterado"))
    pacientes_unicos = len(np.unique(st.session_state.arr_paciente))
    promedio_resultados = float(np.mean(st.session_state.arr_resultado))

    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)

    with col_m1:
        st.metric("🔬 Exámenes registrados", total_examenes)

    with col_m2:
        st.metric("👥 Pacientes únicos", pacientes_unicos)

    with col_m3:
        st.metric("🟢 Resultados normales", examenes_normales)

    with col_m4:
        st.metric("🔴 Resultados alterados", examenes_alterados)

    with col_m5:
        st.metric("📊 Promedio resultados", f"{promedio_resultados:.2f}")

    # Análisis por categoría usando NumPy
    st.markdown("### Análisis por categoría de examen")
    categorias_unicas = np.unique(st.session_state.arr_categoria)

    for cat in categorias_unicas:
        mask = st.session_state.arr_categoria == cat
        cantidad_cat = int(np.sum(mask))
        alterados_cat = int(np.sum(
            (st.session_state.arr_categoria == cat) & (st.session_state.arr_estado == "Alterado")
        ))
        promedio_cat = float(np.mean(st.session_state.arr_resultado[mask]))
        st.write(f"- **{cat}**: {cantidad_cat} exámenes | Alterados: {alterados_cat} | Promedio: {promedio_cat:.2f}")

    # Análisis por paciente
    st.markdown("### Análisis por paciente")
    pacientes_unicos_lista = np.unique(st.session_state.arr_paciente)

    for pac in pacientes_unicos_lista:
        mask_pac = st.session_state.arr_paciente == pac
        examenes_pac = int(np.sum(mask_pac))
        alterados_pac = int(np.sum(
            (st.session_state.arr_paciente == pac) & (st.session_state.arr_estado == "Alterado")
        ))
        st.write(f"- **{pac}**: {examenes_pac} exámenes | Alterados: {alterados_pac}")

else:
    st.info("ℹ️ Aún no has registrado exámenes. Comienza agregando uno arriba.")

# Botón para reiniciar todo
if st.button("🗑️ Reiniciar registros de laboratorio"):
    st.session_state.arr_paciente = np.array([], dtype=object)
    st.session_state.arr_examen = np.array([], dtype=object)
    st.session_state.arr_categoria = np.array([], dtype=object)
    st.session_state.arr_resultado = np.array([], dtype=float)
    st.session_state.arr_referencia = np.array([], dtype=float)
    st.session_state.arr_unidad = np.array([], dtype=object)
    st.session_state.arr_estado = np.array([], dtype=object)
    st.session_state.lab_paciente = ""
    st.session_state.lab_examen = "Glucosa en ayunas"
    st.session_state.lab_categoria = "Química sanguínea"
    st.session_state.lab_resultado = 0.0
    st.session_state.lab_referencia = 0.0
    st.session_state.lab_unidad = "mg/dL"
    st.rerun()  
