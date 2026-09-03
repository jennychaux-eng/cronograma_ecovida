import streamlit as st
from supabase import create_client, Client
from datetime import date
from collections import defaultdict


# ============================================================
# CONFIGURACIÓN GENERAL
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

    /* Fondo general */
    .stApp {
        background-color: #F7F9F8;
    }

    /* Título principal */
    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 16px;
        color: #6B7280;
        margin-bottom: 30px;
    }

    /* Tarjetas del resumen */
    .metric-card {
        background-color: white;
        padding: 22px;
        border-radius: 15px;
        border: 1px solid #E5E7EB;
        text-align: center;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
    }

    .metric-title {
        color: #6B7280;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .metric-value {
        color: #111827;
        font-size: 32px;
        font-weight: 700;
        margin-top: 5px;
    }

    /* Cronograma */
    .student-card {
        background-color: white;
        border-radius: 15px;
        padding: 25px;
        border: 1px solid #E5E7EB;
        margin-bottom: 25px;
    }

    .student-name {
        font-size: 24px;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 20px;
    }

    .date-title {
        font-size: 17px;
        font-weight: 700;
        color: #374151;
        margin-top: 15px;
        margin-bottom: 8px;
    }

    .activity-item {
        font-size: 15px;
        color: #4B5563;
        margin-left: 10px;
        margin-bottom: 4px;
    }

    .location {
        color: #059669;
        font-size: 14px;
        font-weight: 600;
        margin-top: 8px;
        margin-bottom: 15px;
    }

    .completed {
        color: #059669;
    }

    .pending {
        color: #D97706;
    }

    /* Separador */
    hr {
        border: none;
        border-top: 1px solid #E5E7EB;
        margin: 25px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FUNCIONES
# ============================================================

def obtener_actividades():
    """
    Obtiene todas las actividades almacenadas en Supabase.
    """

    response = (
        supabase
        .table("actividades")
        .select("*")
        .order("fecha", desc=False)
        .execute()
    )

    return response.data


def registrar_actividad(
    estudiante,
    predio,
    fecha,
    actividad,
    observaciones
):
    """
    Registra una nueva actividad.
    """

    datos = {
        "estudiante": estudiante,
        "predio": predio,
        "fecha": str(fecha),
        "actividad": actividad,
        "observaciones": observaciones,
        "estado": "Pendiente"
    }

    supabase.table("actividades").insert(datos).execute()


def cambiar_estado(actividad_id, nuevo_estado):
    """
    Cambia el estado de una actividad.
    """

    supabase \
        .table("actividades") \
        .update({"estado": nuevo_estado}) \
        .eq("id", actividad_id) \
        .execute()


def eliminar_actividad(actividad_id):
    """
    Elimina una actividad.
    """

    supabase \
        .table("actividades") \
        .delete() \
        .eq("id", actividad_id) \
        .execute()


# ============================================================
# CARGAR DATOS
# ============================================================

try:

    actividades = obtener_actividades()

except Exception as e:

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
    '<div class="subtitle">'
    'Planificación y seguimiento de actividades de campo'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# RESUMEN
# ============================================================

st.subheader("📊 Resumen")


total_actividades = len(actividades)

pendientes = len([
    a for a in actividades
    if a["estado"] == "Pendiente"
])

completadas = len([
    a for a in actividades
    if a["estado"] == "Completada"
])


# Próximas visitas = fechas futuras con actividades
hoy = date.today()

fechas_futuras = set()

for actividad in actividades:

    fecha_actividad = date.fromisoformat(
        actividad["fecha"]
    )

    if fecha_actividad >= hoy:
        fechas_futuras.add(fecha_actividad)


proximas_visitas = len(fechas_futuras)


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
# CRONOGRAMA
# ============================================================

st.divider()

st.subheader("📅 Cronograma por estudiantes")


estudiantes = [
    "Daniela",
    "Salome",
    "Gabriela"
]


for estudiante in estudiantes:

    st.markdown(
        f"""
        <div class="student-card">

            <div class="student-name">
                👤 {estudiante}
            </div>

        """,
        unsafe_allow_html=True
    )

    actividades_estudiante = [
        a for a in actividades
        if a["estudiante"] == estudiante
    ]

    # --------------------------------------------------------
    # Si no tiene actividades
    # --------------------------------------------------------

    if not actividades_estudiante:

        st.info(
            "No hay actividades programadas."
        )

    else:

        # Agrupar actividades por fecha
        actividades_por_fecha = defaultdict(list)

        for actividad in actividades_estudiante:

            actividades_por_fecha[
                actividad["fecha"]
            ].append(actividad)


        # ----------------------------------------------------
        # Mostrar fechas
        # ----------------------------------------------------

        for fecha_str in sorted(actividades_por_fecha):

            fecha_obj = date.fromisoformat(
                fecha_str
            )

            fecha_formateada = fecha_obj.strftime(
                "%d/%m/%Y"
            )

            st.markdown(
                f"""
                <div class="date-title">
                    📌 {fecha_formateada}
                </div>
                """,
                unsafe_allow_html=True
            )

            actividades_fecha = (
                actividades_por_fecha[fecha_str]
            )

            predios = set()

            for actividad in actividades_fecha:

                predios.add(
                    actividad["predio"]
                )

                estado = actividad["estado"]

                if estado == "Completada":
                    icono = "✅"
                else:
                    icono = "▫️"

                st.markdown(
                    f"""
                    <div class="activity-item">
                        {icono} {actividad["actividad"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Mostrar predio
            for predio in predios:

                st.markdown(
                    f"""
                    <div class="location">
                        📍 {predio}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# REGISTRAR ACTIVIDAD
# ============================================================

st.divider()

st.subheader("➕ Registrar actividad")


with st.form("formulario_actividad"):

    col1, col2 = st.columns(2)

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
            placeholder="Escriba observaciones relacionadas con la actividad..."
        )


    enviar = st.form_submit_button(
        "Registrar actividad",
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
                "Actividad registrada correctamente."
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"No fue posible registrar la actividad: {e}"
            )


# ============================================================
# ADMINISTRACIÓN DE ACTIVIDADES
# ============================================================

st.divider()

st.subheader("⚙️ Gestión de actividades")


if actividades:

    for actividad in actividades:

        fecha_obj = date.fromisoformat(
            actividad["fecha"]
        )

        fecha_formateada = fecha_obj.strftime(
            "%d/%m/%Y"
        )

        col1, col2, col3, col4 = st.columns(
            [2, 2, 3, 1]
        )

        with col1:

            st.write(
                f"**{actividad['estudiante']}**"
            )

            st.caption(
                fecha_formateada
            )

        with col2:

            st.write(
                f"📍 {actividad['predio']}"
            )

        with col3:

            st.write(
                actividad["actividad"]
            )

            if actividad["observaciones"]:

                st.caption(
                    actividad["observaciones"]
                )


        with col4:

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
