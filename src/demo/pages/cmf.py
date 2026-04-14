from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict, cast

import streamlit as st
from cl_forge import cmf
from cl_forge.exceptions import BadStatus
from streamlit import session_state as state
from streamlit.column_config import DateColumn, NumberColumn

if TYPE_CHECKING:
    from datetime import datetime


DEFAULT_IPC_DATA: IpcData = {"Fecha": [], "Valor": []}


class IpcData(TypedDict):
    Fecha: list[datetime]
    Valor: list[float]


st.set_page_config(
    page_title="Clientes API | CMF",
    page_icon="🏦"
)


if "ipc_current_data" not in state:
    state.ipc_current_data: IpcData = DEFAULT_IPC_DATA # type: ignore

if "ipc_year_data" not in state:
    state.ipc_year_data: IpcData = DEFAULT_IPC_DATA # type: ignore

if "cmf_api_key_stored" not in state:
    state.cmf_api_key_stored: str = "" # type: ignore


def avg(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def _set_token() -> None:
    api_key = state.cmf_api_key
    
    try:
        if api_key:
            cmf.IpcEndpoint(api_key).current()
            st.toast("✅ API Key válida")
            state.cmf_api_key_stored = api_key
        else:
            state.cmf_api_key_stored = ""
    except BadStatus:
        st.toast("❌ API Key inválida")
        state.cmf_api_key = ""
        state.cmf_api_key_stored = ""


with st.sidebar:
    st.text_input(
        label="API Key",
        placeholder="Ingrese su API Key de la CMF",
        type="password",
        value=state.cmf_api_key_stored,
        key="cmf_api_key",
        on_change=_set_token,
        help=(
            "⚠️ No es almacenada ni compartida. Solo "
            "se utiliza para esta sesión, y se borra "
            "al cerrar la aplicación o al recargar "
            "la página."
        ),
    )


st.header("Índice de Precios al Consumidor (IPC)")

if not state.cmf_api_key_stored:
    st.warning(
        "Por favor, ingrese su API Key de la CMF "
        "en la barra lateral para consultar datos."
    )


st.subheader("Valor Actual", help="Último valor disponible del IPC publicado por la CMF")

with st.container(horizontal=True, vertical_alignment="bottom"):
    if st.button(
            label="Consultar",
            disabled=not state.cmf_api_key_stored,
            key="ipc_current_button"
    ):
        ipc_current = cmf.IpcEndpoint(state.cmf_api_key_stored).current()

        state.ipc_current_data = {
            "Fecha": [ipc_current.date],
            "Valor": [ipc_current.value],
        }
    
    if st.button(label="Reset", type="primary", key="ipc_current_reset"):
        state.ipc_current_data = DEFAULT_IPC_DATA

st.dataframe( # type: ignore
    data=state.ipc_current_data or DEFAULT_IPC_DATA,
    column_config={
        "Fecha": DateColumn("Fecha", format="MMMM DD, YYYY"),
        "Valor": NumberColumn("Valor", format="percent"),
    },
)

st.divider()

st.subheader("Año Completo", help="Valores del IPC para todo el año seleccionado")

with st.container(horizontal=True, vertical_alignment="bottom"):
    ipc_selected_year = st.number_input(
        label="Seleccionar Año",
        min_value=2000,
        max_value=2026,
        value=2025,
        step=1,
        key="ipc_selected_year",
        on_change=lambda: state.update(
            {"ipc_year_data": DEFAULT_IPC_DATA}
        )
    )

    if st.button("Consultar", disabled=not state.cmf_api_key_stored, key="ipc_year_button"):
        ipc_year = cmf.IpcEndpoint(state.cmf_api_key_stored).year(state.ipc_selected_year) # type: ignore

        state.ipc_year_data: IpcData = { # type: ignore
            "Fecha": [v.date for v in ipc_year] if ipc_year else [],
            "Valor": [v.value for v in ipc_year] if ipc_year else [],
        }
    
    if st.button("Reset", type="primary", key="ipc_year_reset"):
        state.ipc_year_data = DEFAULT_IPC_DATA

if st.toggle(label="Gráfico"):
    st.line_chart( # type: ignore
        data=state.ipc_year_data or DEFAULT_IPC_DATA,
        x="Fecha",
        y="Valor",
        use_container_width=True,
    )
else:
    st.dataframe( # type: ignore
        data=state.ipc_year_data or DEFAULT_IPC_DATA,
        column_config={
            "Fecha": DateColumn("Fecha", format="MMMM DD, YYYY"),
            "Valor": NumberColumn("Valor", format="percent"),
        },
    )

if state.ipc_year_data != DEFAULT_IPC_DATA:
    state.ipc_year_data = cast(
        "IpcData",
        state.ipc_year_data
    )
    
    st.markdown(
        f"**Total {state.ipc_selected_year}:** {sum(state.ipc_year_data['Valor']):.2%}\n\n"
        f"**Promedio {state.ipc_selected_year}:** {avg(state.ipc_year_data['Valor']):.2%}"
    )
