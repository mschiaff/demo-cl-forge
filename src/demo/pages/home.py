from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="Bienvenido | Inicio",
    page_icon="🏠",
)

st.title(
    body="Demo [CL Forge](https://github.com/mschiaff/cl-forge) 👋",
    text_alignment="center",
)

st.markdown(
    "Una aplicación interactiva para explorar las funcionalidades de "
    "[**CL Forge**](https://github.com/mschiaff/cl-forge): herramientas "
    "chilenas de alto rendimiento escritas en **Rust** y **Python**."
)

st.divider()

# --- ¿Qué es CL Forge? ---

st.header("¿Qué es CL Forge?")

st.markdown(
    "`cl-forge` es una librería que ofrece utilidades de alto rendimiento para "
    "formatos de datos chilenos e integraciones con APIs públicas. Su lógica "
    "principal está implementada en **Rust** para máxima velocidad, con una "
    "interfaz **Python** limpia y fácil de usar."
)

col_gh, col_docs, col_pypi = st.columns(3)

with col_gh:
    st.link_button(
        label="📦 GitHub",
        url="https://github.com/mschiaff/cl-forge",
        use_container_width=True,
    )

with col_docs:
    st.link_button(
        label="📖 Documentación",
        url="https://mschiaff.github.io/cl-forge/",
        use_container_width=True,
    )

with col_pypi:
    st.link_button(
        label="🐍 PyPI",
        url="https://pypi.org/project/cl-forge/",
        use_container_width=True,
    )

st.divider()

# --- Funcionalidades ---

st.header("¿Qué puedes explorar?")

st.markdown("Usa la **barra lateral** para navegar entre las siguientes secciones:")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader(":material/person: RUT")
        st.markdown(
            "Calcula y valida el dígito verificador de un RUT/RUN chileno."
        )

    with st.container(border=True):
        st.subheader(":material/account_balance: CMF")
        st.markdown(
            "Consulta datos reales del Índice de Precios al Consumidor (IPC) "
            "desde la API de la Comisión para el Mercado Financiero."
        )

with col2:
    with st.container(border=True):
        st.subheader(":material/airport_shuttle: Patente")
        st.markdown(
            "Calcula y valida el dígito verificador de patentes vehiculares "
            "chilenas, con detección automática de formato."
        )

    with st.container(border=True):
        st.subheader(":material/store: Mercado Público")
        st.markdown(
            "Explora las últimas licitaciones del Estado y consulta sus "
            "detalles a través de la API de Mercado Público."
        )

st.divider()

# --- Nota sobre API Keys ---

st.info(
    "💡 Las páginas de **CMF** y **Mercado Público** requieren una API Key para "
    "consultar datos en vivo. Puedes ingresarla en la barra lateral de cada página. "
    "Consulta la [documentación de CL Forge](https://mschiaff.github.io/cl-forge/) "
    "para más detalles sobre cómo obtenerlas.",
    icon="🔑",
)
