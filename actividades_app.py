import streamlit as st
from supabase import create_client, Client
from datetime import date
from collections import defaultdict


# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Cronograma de Campo",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CONEXIÓN CON SUPABASE
# ============================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# ============================================================
# ESTILOS
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       CONFIGURACIÓN GENERAL
       ===================================================== */

    .stApp {
        background-color: #F8FAFC;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }


    /* =====================================================
       ENCABEZADO
       ===================================================== */

    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 4px;
    }

    .subtitle {
        font-size: 16px;
        color: #6B7280;
        margin-bottom: 30px;
    }


    /* =====================================================
       TARJETAS DEL RESUMEN
       ===================================================== */

    .metric-card {
        background-color: #FFFFFF;
        padding: 22px 15px;
        border-radius: 16px;
        border: 1px solid #E5E7EB;
        text-align: center;
        min-height: 120px;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.04);
    }

    .metric-title {
        color: #6B7280;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    .metric-value {
        color: #111827;
        font-size: 34px;
        font-weight: 700;
        margin-top: 8px;
    }


    /* =====================================================
       SECCIÓN DE ESTUDIANTE
       ===================================================== */

    .student-section {
        background-color: #FFFFFF;
        border-radius: 18px;
        padding: 25px;
        margin-bottom: 30px;
        border: 1px solid #E5E7EB;
        box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.04);
    }

    .student-title {
        font-size: 25px;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 20px;
    }


    /* =====================================================
       TARJETAS DE ACTIVIDADES
       ===================================================== */

    .schedule-card {
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 16px;
        border-left: 6px solid;
    }


    /* ---------------- DANIELA ---------------- */

    .daniela-card {
        background-color: #DFF3FF;
        border-left-color: #56B4E9;
    }


    /* ---------------- SALOME ---------------- */

    .salome-card {
        background-color: #FFE4EC;
        border-left-color: #F28BA8;
    }


    /* ---------------- GABRIELA ---------------- */

    .gabriela-card {
        background-color: #FFF7CC;
        border-left-color: #E8C547;
    }


    /* =====================================================
       CONTENIDO DE TARJETAS
       ===================================================== */

    .schedule-date {
        font-size: 18px;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 13px;
    }

    .schedule-activity {
        font-size: 15px;
        color: #374151;
        margin: 7px 0;
        padding-left: 5px;
    }

    .schedule-location {
        font-size: 14px;
        font-weight: 600;
        color: #374151;
        margin-top: 16px;
        padding-top: 10px;
        border-top: 1px solid rgba(0,0,0,0.08);
    }

    .schedule-observation {
        font-size: 13px;
        color: #6B7280;
        margin-top: 9px;
        font-style: italic;
    }


    /* =====================================================
       BOTONES
       ===================================================== */

    .stButton > button {
        border-radius: 9px;
        font-weight: 600;
    }


    /* =====================================================
       FORMULARIO
       ===================================================== */

    .form-container {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #E5E7EB;
    }


    /* =====================================================
       RESPONSIVE
       ===================================================== */

    @media (max-width: 768px) {

        .main-title {
            font-size: 30px;
        }

        .student-title {
            font-size: 22px;
        }

        .metric-value {
            font-size: 28px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FUNCIONES DE SUPABASE
# ============================================================

def obtener_actividades():

    respuesta = (
        supabase
        .table("actividades")
        .select("*")
        .order("fecha", desc=False)
        .execute()
    )

    return respuesta.data


def registrar_actividad(
    estudiante,
    predio,
    fecha,
    actividad,
    observaciones
):

    datos = {
        "estudiante": estudiante,
        "predio": predio,
        "fecha": str(fecha),
        "actividad": actividad,
        "observaciones": observaciones,
        "estado": "Pendiente"
    }

    supabase \
        .table("actividades") \
        .insert(datos) \
        .execute()


def cambiar_estado(
    actividad_id,
    nuevo_estado
):

    supabase \
        .table("actividades") \
        .update({
            "estado": nuevo_estado
        }) \
        .eq("id", actividad_id) \
        .execute()


def eliminar_actividad(
    actividad_id
):

    supabase \
        .table("actividades") \
        .delete() \
        .eq("id", actividad_id) \
        .execute()


# ============================================================
# CARGAR ACTIVIDADES
# ============================================================

try:

    actividades = obtener_actividades()

except Exception as error:

    st.error(
        "No fue posible conectarse con Supabase."
    )

    st.stop()


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    '<div class="main-title">🌱 Cronograma de Campo</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Planificación y seguimiento de actividades de campo
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# RESUMEN
# ============================================================

st.subheader("📊 Resumen")


# Total de actividades

total_actividades = len(actividades)


# Actividades pendientes

actividades_pendientes = [
    actividad
    for actividad in actividades
    if actividad["estado"] == "Pendiente"
]

pendientes = len(actividades_pendientes)


# Actividades completadas

actividades_completadas = [
    actividad
    for actividad in actividades
    if actividad["estado"] == "Completada"
]

completadas = len(actividades_completadas)


# Próximas visitas

hoy = date.today()

fechas_futuras = set()

for actividad in actividades:

    fecha_actividad = date.fromisoformat(
        actividad["fecha"]
    )

    if fecha_actividad >= hoy:

        fechas_futuras.add(
            fecha_actividad
        )

proximas_visitas = len(
    fechas_futuras
)


# ============================================================
# TARJETAS DEL RESUMEN
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-title">
                Actividades programadas
            </div>

            <div class="metric-value">
                {total_actividades}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-title">
                Actividades pendientes
            </div>

            <div class="metric-value">
                {pendientes}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-title">
                Actividades completadas
            </div>

            <div class="metric-value">
                {completadas}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-title">
                Próximas visitas
            </div>

            <div class="metric-value">
                {proximas_visitas}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CRONOGRAMA POR ESTUDIANTES
# ============================================================

st.divider()

st.subheader("📅 Cronograma por estudiantes")


estudiantes = [
    "Daniela",
    "Salome",
    "Gabriela"
]


for estudiante in estudiantes:


    # ========================================================
    # COLOR DEL ESTUDIANTE
    # ========================================================

    if estudiante == "Daniela":

        clase_color = "daniela-card"

    elif estudiante == "Salome":

        clase_color = "salome-card"

    else:

        clase_color = "gabriela-card"


    # ========================================================
    # CONTENEDOR DEL ESTUDIANTE
    # ========================================================

    st.markdown(
        f"""
        <div class="student-section">

            <div class="student-title">
                👤 {estudiante}
            </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # ACTIVIDADES DEL ESTUDIANTE
    # ========================================================

    actividades_estudiante = [

        actividad

        for actividad in actividades

        if actividad["estudiante"] == estudiante

    ]


    # ========================================================
    # SIN ACTIVIDADES
    # ========================================================

    if not actividades_estudiante:

        st.info(
            "No hay actividades programadas para este estudiante."
        )


    # ========================================================
    # CON ACTIVIDADES
    # ========================================================

    else:


        # ----------------------------------------------------
        # AGRUPAR ACTIVIDADES POR FECHA
        # ----------------------------------------------------

        actividades_por_fecha = defaultdict(list)


        for actividad in actividades_estudiante:

            actividades_por_fecha[
                actividad["fecha"]
            ].append(
                actividad
            )


        # ----------------------------------------------------
        # MOSTRAR CADA FECHA
        # ----------------------------------------------------

        for fecha_str in sorted(
            actividades_por_fecha
        ):


            fecha_obj = date.fromisoformat(
                fecha_str
            )


            # ------------------------------------------------
            # NOMBRES DE LOS MESES
            # ------------------------------------------------

            meses = {

                1: "enero",
                2: "febrero",
                3: "marzo",
                4: "abril",
                5: "mayo",
                6: "junio",
                7: "julio",
                8: "agosto",
                9: "septiembre",
                10: "octubre",
                11: "noviembre",
                12: "diciembre"

            }


            fecha_formateada = (

                f"{fecha_obj.day} de "
                f"{meses[fecha_obj.month]} de "
                f"{fecha_obj.year}"

            )


            actividades_fecha = (
                actividades_por_fecha[
                    fecha_str
                ]
            )


            # ------------------------------------------------
            # OBTENER PREDIOS
            # ------------------------------------------------

            predios = list(
                set(
                    actividad["predio"]

                    for actividad
                    in actividades_fecha
                )
            )


            predios_texto = " / ".join(
                predios
            )


            # ------------------------------------------------
            # LISTA DE ACTIVIDADES
            # ------------------------------------------------

            lista_actividades = ""


            for actividad in actividades_fecha:


                if actividad["estado"] == "Completada":

                    icono = "✅"

                else:

                    icono = "▫️"


                lista_actividades += (

                    f"""
                    <div class="schedule-activity">
                        {icono} {actividad["actividad"]}
                    </div>
                    """

                )


            # ------------------------------------------------
            # OBSERVACIONES
            # ------------------------------------------------

            observaciones = []


            for actividad in actividades_fecha:

                if actividad.get(
                    "observaciones"
                ):

                    observaciones.append(
                        actividad["observaciones"]
                    )


            observaciones_html = ""


            if observaciones:

                observaciones_html = (

                    f"""
                    <div class="schedule-observation">
                        📝 {" | ".join(observaciones)}
                    </div>
                    """

                )


            # ------------------------------------------------
            # TARJETA DE FECHA
            # ------------------------------------------------

            st.markdown(

                f"""
                <div class="schedule-card {clase_color}">

                    <div class="schedule-date">
                        📅 {fecha_formateada}
                    </div>

                    {lista_actividades}

                    <div class="schedule-location">
                        📍 {predios_texto}
                    </div>

                    {observaciones_html}

                </div>
                """,

                unsafe_allow_html=True

            )


    # ========================================================
    # CERRAR CONTENEDOR DEL ESTUDIANTE
    # ========================================================

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# REGISTRAR ACTIVIDAD
# ============================================================

st.divider()

st.subheader("➕ Registrar actividad")


with st.form(
    "formulario_actividad",
    clear_on_submit=True
):


    col1, col2 = st.columns(2)


    # ========================================================
    # COLUMNA 1
    # ========================================================

    with col1:


        estudiante = st.selectbox(
            "Estudiante",
            [
                "Daniela",
                "Salome",
                "Gabriela"
            ]
        )


        predio = st.selectbox(
            "Predio",
            [
                "Lomas de Dapa",
                "Horizontes"
            ]
        )


        fecha = st.date_input(
            "Fecha",
            value=date.today()
        )


    # ========================================================
    # COLUMNA 2
    # ========================================================

    with col2:


        actividad = st.selectbox(
            "Actividad",
            [
                "Actividad 1",
                "Actividad 2",
                "Actividad 3",
                "Actividad 4",
                "Actividad 5"
            ]
        )


        observaciones = st.text_area(
            "Observaciones",
            placeholder=(
                "Escriba observaciones "
                "relacionadas con la actividad..."
            )
        )


    # ========================================================
    # BOTÓN
    # ========================================================

    enviar = st.form_submit_button(
        "➕ Registrar actividad",
        use_container_width=True
    )


    if enviar:


        try:


            registrar_actividad(

                estudiante=estudiante,

                predio=predio,

                fecha=fecha,

                actividad=actividad,

                observaciones=observaciones

            )


            st.success(
                "✅ Actividad registrada correctamente."
            )


            st.rerun()


        except Exception as error:


            st.error(
                f"No fue posible registrar la actividad: {error}"
            )


# ============================================================
# GESTIÓN DE ACTIVIDADES
# ============================================================

st.divider()

st.subheader("⚙️ Gestión de actividades")


if actividades:


    for actividad in actividades:


        # ====================================================
        # FECHA
        # ====================================================

        fecha_obj = date.fromisoformat(
            actividad["fecha"]
        )


        fecha_formateada = fecha_obj.strftime(
            "%d/%m/%Y"
        )


        # ====================================================
        # COLUMNAS
        # ====================================================

        col1, col2, col3, col4 = st.columns(
            [2, 2, 3, 1]
        )


        # ====================================================
        # ESTUDIANTE
        # ====================================================

        with col1:

            st.write(
                f"**{actividad['estudiante']}**"
            )

            st.caption(
                fecha_formateada
            )


        # ====================================================
        # PREDIO
        # ====================================================

        with col2:

            st.write(
                f"📍 {actividad['predio']}"
            )


        # ====================================================
        # ACTIVIDAD
        # ====================================================

        with col3:

            st.write(
                actividad["actividad"]
            )


            if actividad.get(
                "observaciones"
            ):

                st.caption(
                    actividad["observaciones"]
                )


        # ====================================================
        # ACCIONES
        # ====================================================

        with col4:


            # -----------------------------------------------
            # CAMBIAR ESTADO
            # -----------------------------------------------

            if actividad["estado"] == "Pendiente":


                if st.button(

                    "✅",

                    key=f"complete_{actividad['id']}",

                    help="Marcar como completada"

                ):


                    cambiar_estado(

                        actividad["id"],

                        "Completada"

                    )


                    st.rerun()


            else:


                if st.button(

                    "↩️",

                    key=f"pending_{actividad['id']}",

                    help="Marcar como pendiente"

                ):


                    cambiar_estado(

                        actividad["id"],

                        "Pendiente"

                    )


                    st.rerun()


            # -----------------------------------------------
            # ELIMINAR
            # -----------------------------------------------

            if st.button(

                "🗑️",

                key=f"delete_{actividad['id']}",

                help="Eliminar actividad"

            ):


                eliminar_actividad(
                    actividad["id"]
                )


                st.rerun()


        st.divider()


else:

    st.info(
        "No hay actividades registradas."
    )
