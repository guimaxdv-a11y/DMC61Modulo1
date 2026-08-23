import streamlit as st
import numpy as np
import pandas as pd

# ============================================
# IMPORTACIONES SEGURAS DE LIBRERÍAS EXTERNAS
# ============================================
try:
    from libreria_funciones_proyecto1 import calcular_imc, calcular_superficie_corporal
except ImportError:
    calcular_imc = None
    calcular_superficie_corporal = None

try:
    from libreria_clases_proyecto1 import Paciente
except ImportError:
    Paciente = None

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================
st.set_page_config(page_title="Python for Analytics - Proyecto 1", page_icon="🧠", layout="wide")

def init_state(key, default):
    if key not in st.session_state:
        st.session_state[key] = default

init_state("modulo_seleccionado", "🏠 Home")

opciones_menu = [
    "🏠 Home", 
    "📊 Ejercicio 1: Flujo de caja", 
    "📦 Ejercicio 2: Registro de Laboratorio con NumPy",
    "🔧 Ejercicio 3: Funciones externas", 
    "🗂️ Ejercicio 4: Clases y CRUD"
]

# ============================================
# SIDEBAR
# ============================================
st.sidebar.image("Neurolab solo logo.png", use_container_width=True)
st.sidebar.subheader("📋 Menú de Ejercicios")
st.sidebar.markdown("---")

if st.sidebar.button("🏠 Volver al inicio", use_container_width=True):
    st.session_state.modulo_seleccionado = "🏠 Home"
    st.rerun()

st.sidebar.markdown("---")

modulos = st.sidebar.selectbox(
    "Seleccione un módulo", 
    opciones_menu,
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
    st.markdown("""
    ### 📝 Descripción del Proyecto
    Aplicación interactiva que integra los conceptos fundamentales del Módulo 1:
    variables, estructuras de datos, control de flujo, funciones, POO y Streamlit con apoyo de IA.

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
    init_state("ej1_concepto", "")
    init_state("ej1_tipo", "Ingreso")
    init_state("ej1_valor", 0.0)

    st.markdown("### Registrar nuevo movimiento")
    c1, c2, c3 = st.columns(3)
    with c1:
        concepto = st.text_input("Concepto", key="ej1_concepto", placeholder="Ej: Consulta médica")
    with c2:
        tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"], key="ej1_tipo")
    with c3:
        valor = st.number_input("Valor (S/.)", min_value=0.0, step=0.01, format="%.2f", key="ej1_valor")

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
        st.session_state.ej1_concepto = ""
        st.session_state.ej1_tipo = "Ingreso"
        st.session_state.ej1_valor = 0.0
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
        st.session_state.ej1_concepto = ""
        st.session_state.ej1_tipo = "Ingreso"
        st.session_state.ej1_valor = 0.0
        st.rerun()

# ============================================
# EJERCICIO 2 - EXÁMENES DE LABORATORIO 
# ============================================
elif modulos == "📦 Ejercicio 2: Registro de Laboratorio con NumPy":
    st.subheader("🧪 Módulo de Registro de Exámenes de Laboratorio")
    st.markdown("Registra exámenes de laboratorio usando **arrays de NumPy** y visualízalos como DataFrame.")

    for key, dtype in [("arr_paciente", object), ("arr_examen", object), ("arr_categoria", object),
                       ("arr_resultado", float), ("arr_referencia", float), ("arr_unidad", object), ("arr_estado", object)]:
        init_state(key, np.array([], dtype=dtype))

    for key, default in [("ej2_paciente", ""), ("ej2_categoria", "Hematología"), ("ej2_examen", "Hemoglobina"),
                         ("ej2_resultado", 0.0), ("ej2_referencia", 0.0)]:
        init_state(key, default)

    examenes = {
        "Hematología": {"items": ["Hemoglobina", "Hematocrito", "Leucocitos", "Plaquetas"],
                        "unidades": {"Hemoglobina": "g/dL", "Hematocrito": "%", "Leucocitos": "x10^3/µL", "Plaquetas": "x10^3/µL"}},
        "Química sanguínea": {"items": ["Glucosa en ayunas", "HbA1c", "Creatinina", "Ácido úrico"],
                              "unidades": {"Glucosa en ayunas": "mg/dL", "HbA1c": "%", "Creatinina": "mg/dL", "Ácido úrico": "mg/dL"}},
        "Perfil lipídico": {"items": ["Colesterol total", "HDL", "LDL", "Triglicéridos"],
                            "unidades": {k: "mg/dL" for k in ["Colesterol total", "HDL", "LDL", "Triglicéridos"]}},
        "Función hepática": {"items": ["AST (TGO)", "ALT (TGP)", "Bilirrubina total", "Albúmina"],
                             "unidades": {"AST (TGO)": "U/L", "ALT (TGP)": "U/L", "Bilirrubina total": "mg/dL", "Albúmina": "g/dL"}}
    }

    st.markdown("### Registrar nuevo examen")
    c1, c2 = st.columns(2)
    with c1:
        paciente = st.text_input("👤 Paciente", key="ej2_paciente", placeholder="Ej: Juan Pérez")
        categoria = st.selectbox("📋 Categoría", list(examenes.keys()), key="ej2_categoria")
    with c2:
        examen_opts = examenes[categoria]["items"]
        examen = st.selectbox("🔬 Examen", examen_opts, key="ej2_examen")
        unidad = examenes[categoria]["unidades"][examen]
        st.text_input("📏 Unidad", value=unidad, disabled=True)

    c3, c4 = st.columns(2)
    with c3:
        resultado = st.number_input("📊 Resultado", min_value=0.0, step=0.01, format="%.2f", key="ej2_resultado")
    with c4:
        referencia = st.number_input("📐 Valor de referencia", min_value=0.0, step=0.01, format="%.2f", key="ej2_referencia")

    if referencia > 0:
        estado = "Normal" if resultado <= referencia else "Alterado"
        icono = "🟢" if estado == "Normal" else "🔴"
        st.info(f"💡 Estado: **{icono} {estado}**")
    else:
        estado = "Sin evaluar"
        st.warning("⚠️ Ingresa un valor de referencia para evaluar el estado.")

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
        st.session_state.ej2_paciente = ""
        st.session_state.ej2_categoria = "Hematología"
        st.session_state.ej2_examen = "Hemoglobina"
        st.session_state.ej2_resultado = 0.0
        st.session_state.ej2_referencia = 0.0
        st.rerun()

    st.markdown("### Tabla de exámenes (DataFrame)")
    if len(st.session_state.arr_paciente) > 0:
        df = pd.DataFrame({
            "Paciente": st.session_state.arr_paciente, "Examen": st.session_state.arr_examen,
            "Categoría": st.session_state.arr_categoria, "Resultado": st.session_state.arr_resultado,
            "Referencia": st.session_state.arr_referencia, "Unidad": st.session_state.arr_unidad,
            "Estado": st.session_state.arr_estado
        })
        st.dataframe(df, use_container_width=True)

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("🔬 Exámenes", len(st.session_state.arr_paciente))
        c2.metric("👥 Pacientes", len(np.unique(st.session_state.arr_paciente)))
        c3.metric("🟢 Normales", int(np.sum(st.session_state.arr_estado == "Normal")))
        c4.metric("🔴 Alterados", int(np.sum(st.session_state.arr_estado == "Alterado")))
        c5.metric("📊 Promedio", f"{np.mean(st.session_state.arr_resultado):.2f}")

        st.markdown("### Análisis por categoría")
        for cat in np.unique(st.session_state.arr_categoria):
            mask = st.session_state.arr_categoria == cat
            st.write(f"- **{cat}**: {int(np.sum(mask))} exámenes | "
                     f"Alterados: {int(np.sum((mask) & (st.session_state.arr_estado == 'Alterado')))} | "
                     f"Promedio: {np.mean(st.session_state.arr_resultado[mask]):.2f}")

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
        st.session_state.ej2_paciente = ""
        st.session_state.ej2_categoria = "Hematología"
        st.session_state.ej2_examen = "Hemoglobina"
        st.session_state.ej2_resultado = 0.0
        st.session_state.ej2_referencia = 0.0
        st.rerun()

# ============================================
# EJERCICIO 3 - FUNCIONES EXTERNAS
# ============================================
elif modulos == "🔧 Ejercicio 3: Funciones externas":
    st.subheader("🧬 Cálculo de IMC y Superficie Corporal")
    st.markdown("Usa funciones de `libreria_funciones_proyecto1.py` para calcular IMC, clasificación y superficie corporal (Mosteller).")

    init_state("historial_imc", [])
    init_state("ej3_peso", 70.0)
    init_state("ej3_altura", 1.75)

    st.markdown("### Ingresa tus datos")
    c1, c2 = st.columns(2)
    with c1:
        peso = st.number_input("⚖️ Peso (kg)", min_value=1.0, max_value=300.0, step=0.5, format="%.1f", key="ej3_peso")
    with c2:
        altura = st.number_input("📏 Altura (m)", min_value=0.50, max_value=2.50, step=0.01, format="%.2f", key="ej3_altura")

    col1, col2, col3 = st.columns(3)
    with col1:
        calcular = st.button("🧮 Calcular", use_container_width=True)
    with col2:
        limpiar = st.button("🧹 Limpiar campos", use_container_width=True)
    with col3:
        reiniciar = st.button("🗑️ Reiniciar historial", use_container_width=True)

    if calcular:
        if calcular_imc is None or calcular_superficie_corporal is None:
            st.error("⚠️ Error: No se encontró `libreria_funciones_proyecto1.py`. Asegúrate de que el archivo esté en la misma carpeta.")
        else:
            try:
                imc = calcular_imc(peso, altura)
                sc = calcular_superficie_corporal(peso, altura * 100)
                st.session_state.historial_imc.append({
                    "Peso (kg)": peso, "Altura (m)": altura,
                    "IMC": imc["imc"], "Clasificación": imc["clasificacion"],
                    "Superficie Corporal (m²)": sc["superficie_corporal_m2"]
                })
                st.success("✅ Cálculo guardado.")
            except Exception as e:
                st.error(f"⚠️ Error en el cálculo: {e}")

    if limpiar:
        st.session_state.ej3_peso = 70.0
        st.session_state.ej3_altura = 1.75
        st.rerun()

    if reiniciar:
        st.session_state.historial_imc = []
        st.rerun()

    if st.session_state.historial_imc:
        df = pd.DataFrame(st.session_state.historial_imc)
        st.markdown("### 📋 Historial de cálculos")
        st.dataframe(df, use_container_width=True)

        st.markdown("#### 📈 Resumen")
        c1, c2, c3 = st.columns(3)
        c1.metric("Promedio IMC", f"{df['IMC'].mean():.2f}")
        c2.metric("Mínimo IMC", f"{df['IMC'].min():.2f}")
        c3.metric("Máximo IMC", f"{df['IMC'].max():.2f}")

        st.markdown("#### 🧾 Distribución por clasificación")
        conteo = df["Clasificación"].value_counts().reset_index()
        conteo.columns = ["Clasificación", "Cantidad"]
        st.dataframe(conteo, use_container_width=True)
    else:
        st.info("ℹ️ No hay cálculos registrados. Presiona 'Calcular' para empezar.")

# ============================================
# EJERCICIO 4 - CLASES Y CRUD (PACIENTE)
# ============================================
elif modulos == "🗂️ Ejercicio 4: Clases y CRUD":
    st.subheader("🏥 Módulo de Pacientes (CRUD con Clases)")
    st.markdown("""
    Gestiona pacientes usando la clase `Paciente` de `libreria_clases_proyecto1.py`.
    - **Crear**: registrar nuevo paciente.
    - **Leer**: ver todos los pacientes y sus cálculos.
    - **Actualizar**: modificar datos de un paciente existente.
    - **Eliminar**: borrar un paciente de la lista.
    """)

    init_state("pacientes", [])
    init_state("ej4_nombre", "")
    init_state("ej4_peso", 70.0)
    init_state("ej4_altura", 1.75)
    init_state("ej4_edit_index", None)

    if Paciente is None:
        st.error("⚠️ Error: No se encontró `libreria_clases_proyecto1.py`. Asegúrate de que el archivo esté en la misma carpeta.")
    else:
        def agregar_paciente(nombre, peso, altura):
            try:
                paciente = Paciente(nombre, peso, altura)
                st.session_state.pacientes.append(paciente)
                return True, "✅ Paciente agregado."
            except Exception as e:
                return False, f"⚠️ {e}"

        def actualizar_paciente(index, nombre, peso, altura):
            try:
                paciente = Paciente(nombre, peso, altura)
                st.session_state.pacientes[index] = paciente
                return True, "✅ Paciente actualizado."
            except Exception as e:
                return False, f"⚠️ {e}"

        def eliminar_paciente(index):
            if 0 <= index < len(st.session_state.pacientes):
                del st.session_state.pacientes[index]
                return True, "🗑️ Paciente eliminado."
            return False, "⚠️ Índice no válido."

        st.markdown("### 📝 Datos del paciente")
        c1, c2, c3 = st.columns(3)
        with c1:
            nombre = st.text_input("👤 Nombre", key="ej4_nombre", placeholder="Ej: Juan Pérez")
        with c2:
            peso = st.number_input("⚖️ Peso (kg)", min_value=1.0, max_value=300.0, step=0.5, format="%.1f", key="ej4_peso")
        with c3:
            altura = st.number_input("📏 Altura (m)", min_value=0.50, max_value=2.50, step=0.01, format="%.2f", key="ej4_altura")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            crear = st.button("➕ Crear", use_container_width=True)
        with col2:
            actualizar = st.button("🔄 Actualizar", use_container_width=True)
        with col3:
            limpiar = st.button("🧹 Limpiar", use_container_width=True)
        with col4:
            cancelar = st.button("❌ Cancelar edición", use_container_width=True)

        if crear:
            if not nombre.strip():
                st.warning("⚠️ El nombre es obligatorio.")
            else:
                ok, msg = agregar_paciente(nombre.strip(), peso, altura)
                if ok:
                    st.success(msg)
                    # CORREGIDO: Asignaciones individuales en lugar de tuple unpacking
                    st.session_state.ej4_nombre = ""
                    st.session_state.ej4_peso = 70.0
                    st.session_state.ej4_altura = 1.75
                    st.session_state.ej4_edit_index = None
                    st.rerun()
                else:
                    st.error(msg)

        if actualizar:
            idx = st.session_state.ej4_edit_index
            if idx is None:
                st.warning("⚠️ Selecciona un paciente de la tabla (botón ✏️).")
            elif not nombre.strip():
                st.warning("⚠️ El nombre es obligatorio.")
            else:
                ok, msg = actualizar_paciente(idx, nombre.strip(), peso, altura)
                if ok:
                    st.success(msg)
                    # CORREGIDO: Asignaciones individuales
                    st.session_state.ej4_nombre = ""
                    st.session_state.ej4_peso = 70.0
                    st.session_state.ej4_altura = 1.75
                    st.session_state.ej4_edit_index = None
                    st.rerun()
                else:
                    st.error(msg)

        if limpiar or cancelar:
            # CORREGIDO: Asignaciones individuales
            st.session_state.ej4_nombre = ""
            st.session_state.ej4_peso = 70.0
            st.session_state.ej4_altura = 1.75
            st.session_state.ej4_edit_index = None
            st.rerun()

        st.markdown("### 📋 Lista de pacientes")
        if not st.session_state.pacientes:
            st.info("ℹ️ No hay pacientes registrados.")
        else:
            data = []
            for i, p in enumerate(st.session_state.pacientes):
                r = p.resumen()
                data.append({
                    "ID": i, "Nombre": r["paciente"], "Peso (kg)": p.peso_kg, "Altura (m)": p.altura_m,
                    "IMC": r["imc"], "Clasificación": r["clasificacion_imc"], "Superficie (m²)": r["superficie_corporal_m2"]
                })
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)

            st.markdown("#### 🔧 Acciones")
            col_sel, col_acc = st.columns([2, 1])
            with col_sel:
                id_sel = st.selectbox("Selecciona paciente por ID", options=df["ID"].tolist(),
                                      format_func=lambda x: f"ID {x}: {df[df['ID']==x]['Nombre'].values[0]}")
            with col_acc:
                accion = st.radio("Acción", ["✏️ Editar", "🗑️ Eliminar"], horizontal=True)

            if st.button("▶️ Ejecutar", use_container_width=True):
                if accion == "✏️ Editar":
                    paciente = st.session_state.pacientes[id_sel]
                    st.session_state.ej4_nombre = paciente.nombre
                    st.session_state.ej4_peso = paciente.peso_kg
                    st.session_state.ej4_altura = paciente.altura_m
                    st.session_state.ej4_edit_index = id_sel
                    st.success("✏️ Datos cargados para editar. Modifica y presiona 'Actualizar'.")
                else:
                    ok, msg = eliminar_paciente(id_sel)
                    if ok:
                        st.success(msg)
                        if st.session_state.ej4_edit_index == id_sel:
                            st.session_state.ej4_edit_index = None
                            # CORREGIDO: Asignaciones individuales
                            st.session_state.ej4_nombre = ""
                            st.session_state.ej4_peso = 70.0
                            st.session_state.ej4_altura = 1.75
                        st.rerun()
                    else:
                        st.error(msg)

            if st.session_state.ej4_edit_index is not None and st.session_state.ej4_edit_index < len(st.session_state.pacientes):
                p = st.session_state.pacientes[st.session_state.ej4_edit_index]
                st.info(f"✏️ Editando: **{p.nombre}** (ID {st.session_state.ej4_edit_index})")

        if st.session_state.pacientes:
            st.markdown("### 📊 Resumen")
            imcs = [p.calcular_imc() for p in st.session_state.pacientes]
            clasif = [p.clasificacion_imc() for p in st.session_state.pacientes]
            c1, c2, c3 = st.columns(3)
            c1.metric("👥 Total", len(st.session_state.pacientes))
            c2.metric("📊 IMC promedio", f"{np.mean(imcs):.2f}")
            c3.metric("🟢 Peso normal", clasif.count("Peso normal"))
