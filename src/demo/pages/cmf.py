from __future__ import annotations

import locale

import streamlit as st
from cl_forge import cmf
from streamlit import session_state as state
from streamlit.column_config import DateColumn, NumberColumn

st.set_page_config(
    page_title="Clientes API | CMF",
    page_icon="🏦"
)

locale.setlocale(locale.LC_ALL, "es_ES")

if "cmf_api_key" not in state:
    state.cmf_api_key: str | None = None # type: ignore


with st.sidebar:
    st.text_input(
        label="API Key",
        placeholder="Ingrese su API Key de la CMF",
        type="password",
        help=(
            "⚠️ No es almacenada ni compartida. Solo "
            "se utiliza para esta sesión, y se borra "
            "al cerrar la aplicación o al recargar "
            "la página."
        ),
        key="cmf_api_key",
    )


st.header("Índice de Precios al Consumidor (IPC)")


st.subheader("Valor Actual")

df_ipc_current = st.dataframe( # type: ignore
        data={
            "Fecha": [],
            "Valor": [],
        },
        column_config={
            "Fecha": DateColumn(
                "Fecha",
                format="MMMM DD, YYYY"
            ),
            "Valor": NumberColumn(
                "Valor",
                format="percent"
            ),
        },
        key="ipc_current_df",
    )

if st.button(label="Consultar", disabled=state.cmf_api_key is None):
    ipc_current = cmf.IpcEndpoint(
        state.cmf_api_key # type: ignore
    ).current()
    
    ipc_current_data = {
        "Fecha": [ipc_current.date],
        "Valor": [ipc_current.value],
    }
    df_ipc_current.add_rows( # type: ignore
        ipc_current_data
    )


st.number_input(
    label="Año",
    min_value=2000,
    max_value=2026,
    value=2025,
    step=1,
    key="ipc_selected_year",
)

df_ipc_year = st.dataframe( # type: ignore
        data={
            "Fecha": [],
            "Valor": [],
        },
        column_config={
            "Fecha": DateColumn(
                "Fecha",
                format="MMMM DD, YYYY"
            ),
            "Valor": NumberColumn(
                "Valor",
                format="percent"
            ),
        },
        key="ipc_year_df",
    )

ipc_year_container = st.container()
if st.button("Consultar Año", disabled=state.cmf_api_key is None):
    ipc_year = cmf.IpcEndpoint(
        state.cmf_api_key # type: ignore
    ).year(
        state.ipc_selected_year
    )
    
    ipc_year_data = {
        "Fecha": [v.date for v in ipc_year],
        "Valor": [v.value for v in ipc_year],
    }
    df_ipc_year.add_rows( # type: ignore
        ipc_year_data
    )

    if df_ipc_year:
        ipc_year_container.markdown(
            f"**Total {state.ipc_selected_year}:** "
            f"{sum(v.value for v in ipc_year):.2%}"
        )


st.write(state)