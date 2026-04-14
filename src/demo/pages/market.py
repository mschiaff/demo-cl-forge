from __future__ import annotations

from typing import Any, TypedDict

import streamlit as st
from cl_forge import market
from cl_forge.exceptions import BadStatus
from streamlit import session_state as state

DEFAULT_TENDER_DATA: TenderData = {
    "CodigoExterno": "",
    "Nombre": "",
    "CodigoEstado": 0,
    "FechaCierre": ""
}


class TenderData(TypedDict):
    CodigoExterno: str
    Nombre: str
    CodigoEstado: int
    FechaCierre: str


st.set_page_config(
    page_title="Clientes API | Mercado Público",
    page_icon="🏪"
)

st.markdown(
    """
    <style>
        .st-key-tender-detail-container .stAlertContainer {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


if "tenders_latest_data" not in state:
    state.tenders_latest_data: list[TenderData] = [DEFAULT_TENDER_DATA] # type: ignore

if "tender_detail_data" not in state:
    state.tender_detail_data: dict[str, Any] = {} # type: ignore

if "market_api_key_stored" not in state:
    state.market_api_key_stored: str = "" # type: ignore


def _set_token() -> None:
    api_key = state.market_api_key
    
    try:
        if api_key:
            market.MarketClient(api_key).get("/licitaciones")
            st.toast("✅ API Key válida")
            state.market_api_key_stored = api_key
        else:
            state.market_api_key_stored = ""
    except BadStatus:
        st.toast("❌ API Key inválida")
        state.market_api_key = ""
        state.market_api_key_stored = ""


with st.sidebar:
    st.text_input(
        label="API Key",
        placeholder="Ingrese su API Key de Mercado Público",
        type="password",
        value=state.market_api_key_stored,
        key="market_api_key",
        on_change=_set_token,
        help=(
            "⚠️ No es almacenada ni compartida. Solo "
            "se utiliza para esta sesión, y se borra "
            "al cerrar la aplicación o al recargar "
            "la página."
        ),
    )


st.header("Licitaciones de Mercado Público")

if not state.market_api_key_stored:
    st.warning(
        "Por favor, ingrese su API Key de Mercado Público "
        "en la barra lateral para consultar datos. "
        "Si no tienes una, puedes obtenerla gratis solicitándola aquí 👉 "
        "[Solicitar API Key](https://api.mercadopublico.cl/modules/IniciarSesion.aspx).\n\n"
        "También puedes usar la API Key de prueba de Mercado Público 👇"
    )
    st.code('F8537A18-6766-4DEF-9E59-426B4FEE2844')


st.subheader(
    "Últimas Licitaciones",
    help="Listado de las últimas licitaciones publicadas en Mercado Público"
)

with st.container(horizontal=True, vertical_alignment="bottom"):
    if st.button(
            label="Consultar",
            disabled=not state.market_api_key_stored,
            key="tenders_latest_button"
    ):
        tenders_latest = market.MarketClient(state.market_api_key_stored).get("/licitaciones")
        state.tenders_latest_data = tenders_latest.get("Listado", [DEFAULT_TENDER_DATA])
        state.tenders_latest_data.sort(key=lambda x: x.get("FechaCierre") or "", reverse=True) # type: ignore
    
    if st.button(label="Reset", type="primary", key="tenders_latest_reset"):
        state.tenders_latest_data = [DEFAULT_TENDER_DATA]

st.dataframe( # type: ignore
    state.tenders_latest_data or [DEFAULT_TENDER_DATA]
)

st.divider()

st.subheader(
    "Detalle Licitación",
    help="Consulta los detalles de una licitación específica por su código externo"
)

with st.container(horizontal=True, vertical_alignment="bottom", key="tender-detail-container"):
    tender_code = st.text_input(
        label="Código Externo",
        placeholder="Ingrese el código externo de la licitación",
        key="tender_detail_code"
    )

    if st.button(
            label="Consultar",
            disabled=not state.market_api_key_stored,
            key="tender_detail_button"
    ):
        if not tender_code:
            st.warning("Ingrese un código externo.")
        else:
            try:
                tender_detail = market.MarketClient(state.market_api_key_stored).get( # type: ignore
                    "/licitaciones",
                    params={"codigo": tender_code}
                )
                state.tender_detail_data = tender_detail.get("Listado", [])[0] # type: ignore
            except BadStatus:
                st.error("Licitación no encontrada.")

    if st.button(label="Reset", type="primary", key="tender_detail_reset"):
        state.tender_detail_data = {}

if state.tender_detail_data: # type: ignore
    st.json(state.tender_detail_data) # type: ignore
