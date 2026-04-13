from __future__ import annotations

import os
from typing import TYPE_CHECKING, TypedDict, cast

import streamlit as st
from cl_forge import cmf
from cl_forge.settings import Token
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


token = Token()


def avg(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def _set_token() -> None:
    os.environ["CLFORGE_CMF_TOKEN"] = state.cmf_api_key


with st.sidebar:
    st.text_input(
        label="API Key",
        placeholder="Ingrese su API Key de la CMF",
        type="password",
        value=token.cmf or "",
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


st.subheader("Valor Actual", help="Último valor disponible del IPC publicado por la CMF")

if st.button(label="Consultar", disabled=not token.cmf):
    ipc_current = cmf.IpcEndpoint(token.cmf).current() # type: ignore

    state.ipc_current_data = {
        "Fecha": [ipc_current.date],
        "Valor": [ipc_current.value],
    }

st.dataframe( # type: ignore
    data=state.ipc_current_data or DEFAULT_IPC_DATA,
    column_config={
        "Fecha": DateColumn("Fecha", format="MMMM DD, YYYY"),
        "Valor": NumberColumn("Valor", format="percent"),
    },
)


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
            {"ipc_year_data": None}
        )
    )

    if st.button("Consultar Año", disabled=not token.cmf):
        ipc_year = cmf.IpcEndpoint(token.cmf).year(state.ipc_selected_year) # type: ignore

        state.ipc_year_data: IpcData = { # type: ignore
            "Fecha": [v.date for v in ipc_year] if ipc_year else [],
            "Valor": [v.value for v in ipc_year] if ipc_year else [],
        }

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

if state.ipc_year_data:
    state.ipc_year_data = cast(
        "IpcData",
        state.ipc_year_data
    )
    
    st.markdown(
        f"**Total {state.ipc_selected_year}:** {sum(state.ipc_year_data['Valor']):.2%}\n\n"
        f"**Promedio {state.ipc_selected_year}:** {avg(state.ipc_year_data['Valor']):.2%}"
    )
