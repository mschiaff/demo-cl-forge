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


if state.cmf_api_key and st.button("Obtener"):
    ipc = cmf.IpcEndpoint(state.cmf_api_key)
    obj = ipc.current()
    df_ipc_current = st.dataframe(
        data={
            "Fecha": [obj.date],
            "Valor": [obj.value],
        },
        column_config={
            "Fecha": DateColumn("Fecha", format="MMMM DD, YYYY"),
            "Valor": NumberColumn("Valor", format="percent"),
        }
    )

if state.cmf_api_key and st.button("Obtener Año"):
    ipc = cmf.IpcEndpoint(state.cmf_api_key)
    obj = ipc.year(2025)
    df_ipc_year = st.dataframe(
        data={
            "Fecha": [v.date for v in obj],
            "Valor": [v.value for v in obj],
        },
        column_config={
            "Fecha": DateColumn("Fecha", format="MMMM DD, YYYY"),
            "Valor": NumberColumn("Valor", format="percent"),
        }
    )

st.write(state)