import streamlit as st
from supabase import create_client, Client
from datetime import date
from collections import defaultdict
from pathlib import Path

# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="CRONOGRAMA",
    page_icon="🌳",
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

    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }

    .metric-box {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 18px;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.04);
        aspect-ratio: 1 / 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 1rem;
    }

    .metric-label {
        color: #6B7280;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.4px;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }

    .metric-number {
        color: #111827;
        font-size: clamp(28px, 2.5vw, 42px);
        font-weight: 800;
        line-height: 1.1;
    }

    .metric-delta {
        color: #4B5563;
        font-size: 12px;
        font-weight: 600;
        margin-top: 0.5rem;
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

    .student-schedule-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }

    .schedule-card {
        border-radius: 18px;
        padding: 1rem;
        border-left: 6px solid;
        aspect-ratio: 1 / 1;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        overflow: hidden;
        box-sizing: border-box;
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
        font-size: 17px;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 10px;
        line-height: 1.3;
    }

    .schedule-activity {
        font-size: 14px;
        color: #374151;
        margin: 4px 0;
        padding-left: 4px;
        line-height: 1.3;
    }

    .schedule-location {
        font-size: 13px;
        font-weight: 700;
        color: #374151;
        margin-top: auto;
        padding-top: 10px;
        border-top: 1px solid rgba(0,0,0,0.08);
    }

    .schedule-observation {
        font-size: 12px;
        color: #6B7280;
        margin-top: 8px;
        font-style: italic;
        line-height: 1.4;
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

    @media (max-width: 1100px) {
        .student-schedule-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

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

        .student-schedule-grid {
            grid-template-columns: 1fr;
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

logo_path = Path(__file__).parent / "images" / "ecovida_logo.png"
if not logo_path.exists():
    logo_path = Path(__file__).parent / "ecovida_logo.png"

header_content, header_logo = st.columns([5, 1])

with header_content:
    st.markdown(
        '<div class="main-title"> 🌳CRONOGRAMA DE ACTIVIDADES </div>',
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

with header_logo:
    if logo_path.exists():
        st.image(str(logo_path), width=150)


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


# ============================================================
# TARJETAS DEL RESUMEN
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Actividades programadas",
        value=total_actividades,
        delta="Total"
    )

with col2:
    st.metric(
        label="Actividades pendientes",
        value=pendientes,
        delta="Por atender"
    )

with col3:
    st.metric(
        label="Actividades completadas",
        value=completadas,
        delta="OK"
    )


# ============================================================
# CRONOGRAMA POR ESTUDIANTES
# ============================================================

st.divider()

st.subheader("📅 Cronograma por estudiantes")


estudiantes = [
    "Daniela",
    "Salomé",
    "Gabriela"
]


for estudiante in estudiantes:


    # ========================================================
    # COLOR DEL ESTUDIANTE
    # ========================================================

    if estudiante == "Daniela":

        clase_color = "daniela-card"

    elif estudiante == "Salomé":

        clase_color = "salome-card"

    else:

        clase_color = "gabriela-card"


    # ========================================================
    # CONTENEDOR DEL ESTUDIANTE
    # ========================================================

    emoji_por_estudiante = {
        "Daniela": "🌱",
        "Salomé": "🦋",
        "Gabriela": "💧"
    }

    st.markdown(f"### {emoji_por_estudiante[estudiante]} {estudiante}")


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
        # MOSTRAR CADA FECHA EN COLUMNAS NATIVAS
        # ----------------------------------------------------

        fechas_ordenadas = sorted(
            actividades_por_fecha
        )

        for indice in range(0, len(fechas_ordenadas), 4):

            columnas = st.columns(4)

            for posicion in range(4):

                if indice + posicion >= len(fechas_ordenadas):
                    break

                fecha_str = fechas_ordenadas[indice + posicion]
                fecha_obj = date.fromisoformat(fecha_str)

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

                actividades_fecha = actividades_por_fecha[fecha_str]

                predios = list(
                    set(
                        actividad["predio"]
                        for actividad in actividades_fecha
                    )
                )
                predios_texto = " / ".join(predios)

                with columnas[posicion]:

                    color_style = {
                        "Daniela": "background-color: #DFF3FF; border: 1px solid #B7E3F9; border-radius: 16px; padding: 16px; margin-bottom: 12px;",
                        "Salomé": "background-color: #FFE4EC; border: 1px solid #F6C2D4; border-radius: 16px; padding: 16px; margin-bottom: 12px;",
                        "Gabriela": "background-color: #FFF7CC; border: 1px solid #F2E39F; border-radius: 16px; padding: 16px; margin-bottom: 12px;",
                    }[estudiante]

                    actividades_html = "".join(
                        f"<div style='margin-top: 8px;'><strong>{'✅' if actividad['estado'] == 'Completada' else '▫️'}</strong> {actividad['actividad']}</div>"
                        for actividad in actividades_fecha
                    )

                    observaciones = [
                        actividad["observaciones"]
                        for actividad in actividades_fecha
                        if actividad.get("observaciones")
                    ]

                    observaciones_html = ""
                    if observaciones:
                        observaciones_html = (
                            "<div style='margin-top: 8px; color: #6B7280; font-size: 12px; font-style: italic;'>"
                            f"📝 {' | '.join(observaciones)}"
                            "</div>"
                        )

                    st.markdown(
                        f"<div style='{color_style}'>"
                        f"<div><strong>📅 {fecha_formateada}</strong></div>"
                        f"<div style='margin-top: 10px;'>{actividades_html}</div>"
                        f"<div style='margin-top: 12px;'><strong>📍</strong> {predios_texto}</div>"
                        f"{observaciones_html}"
                        "</div>",
                        unsafe_allow_html=True,
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
                "Salomé",
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


        actividad = st.text_input(
            "Actividad",
            placeholder="Ej: Monitoreo de cultivos, inspección de predio..."
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

    estudiante_seleccionado = st.selectbox(
        "Selecciona estudiante",
        ["Daniela", "Salomé", "Gabriela"],
        index=0
    )

    actividades_filtradas = [
        actividad
        for actividad in actividades
        if actividad["estudiante"] == estudiante_seleccionado
    ]

    if not actividades_filtradas:
        st.info(f"No hay actividades registradas para {estudiante_seleccionado}.")

    else:
        for actividad in actividades_filtradas:

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

                if actividad.get("observaciones"):
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
