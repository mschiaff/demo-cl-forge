from __future__ import annotations

from typing import Any

import streamlit as st
from cl_forge import cmf
from streamlit import session_state as state
from streamlit.column_config import DateColumn, NumberColumn

st.set_page_config(
    page_title="Clientes API | CMF",
    page_icon="🏦"
)

if "cmf_api_key_stored" not in state:
    state.cmf_api_key_stored: str | None = None # type: ignore

if "ipc_current_data" not in state:
    state.ipc_current_data: dict[str, list[Any]] | None = None # type: ignore

if "ipc_year_data" not in state:
    state.ipc_year_data: dict[str, list[Any]] | None = None # type: ignore


with st.sidebar:
    st.text_input(
        label="API Key",
        placeholder="Ingrese su API Key de la CMF",
        type="password",
        value=state.cmf_api_key_stored or "",
        key="cmf_api_key",
        on_change=lambda: state.update({"cmf_api_key_stored": state.cmf_api_key}),
        help=(
            "⚠️ No es almacenada ni compartida. Solo "
            "se utiliza para esta sesión, y se borra "
            "al cerrar la aplicación o al recargar "
            "la página."
        ),
    )


st.header("Índice de Precios al Consumidor (IPC)")


st.subheader("Valor Actual")

if st.button(label="Consultar", disabled=state.cmf_api_key_stored is None):
    ipc_current = cmf.IpcEndpoint(state.cmf_api_key_stored).current() # type: ignore

    state.ipc_current_data = {
        "Fecha": [ipc_current.date],
        "Valor": [ipc_current.value],
    }

st.dataframe( # type: ignore
    data=state.ipc_current_data or {"Fecha": [], "Valor": []},
    column_config={
        "Fecha": DateColumn("Fecha", format="MMMM DD, YYYY"),
        "Valor": NumberColumn("Valor", format="percent"),
    },
)


st.subheader("Año Completo")

with st.container(horizontal=True, vertical_alignment="bottom"):
    ipc_selected_year = st.number_input(
        label="Seleccionar Año",
        min_value=2000,
        max_value=2026,
        value=2025,
        step=1,
        key="ipc_selected_year",
        on_change=lambda: state.update({"ipc_year_data": None})
    )

    if st.button("Consultar Año", disabled=state.cmf_api_key_stored is None):
        ipc_year = cmf.IpcEndpoint(state.cmf_api_key_stored).year(state.ipc_selected_year) # type: ignore

        state.ipc_year_data = {
            "Fecha": [v.date for v in ipc_year] if ipc_year else [],
            "Valor": [v.value for v in ipc_year] if ipc_year else [],
        }

st.dataframe( # type: ignore
    data=state.ipc_year_data or {"Fecha": [], "Valor": []},
    column_config={
        "Fecha": DateColumn("Fecha", format="MMMM DD, YYYY"),
        "Valor": NumberColumn("Valor", format="percent"),
    },
)

if state.ipc_year_data:
    st.markdown(
        f"**Total {state.ipc_selected_year}:** "
        f"{sum(state.ipc_year_data['Valor']):.2%}\n\n"
        f"**Promedio {state.ipc_selected_year}:** "
        f"{sum(state.ipc_year_data['Valor']) / len(state.ipc_year_data['Valor']):.2%}"
    )


st.write(state)