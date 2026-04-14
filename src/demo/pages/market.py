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

if "market_client" not in state:
    state.market_client: market.MarketClient | None = None # type: ignore


def _is_concurrent_request_error(error: BadStatus) -> bool:
    """Check if the error is a concurrent requests error (status 500, code 10500)."""
    return bool(
        error.args and 'Unexpected status 500: {"Codigo":10500' in error.args[0]
    )


def _set_token() -> None:
    api_key = state.market_api_key
    
    if not api_key:
        state.market_api_key_stored = ""
        state.market_client = None
        return

    try:
        client = market.MarketClient(api_key)
        client.get("/licitaciones")
        st.toast("✅ API Key válida")
        state.market_api_key_stored = api_key
        state.market_client = client
    except BadStatus as error:
        if _is_concurrent_request_error(error):
            st.toast(
                "⚠️ Existen peticiones simultáneas con la API Key "
                "de prueba. Intente nuevamente."
            )
            state.market_api_key = ""
            state.market_api_key_stored = ""
            state.market_client = None
        else:
            st.toast("❌ API Key inválida")
            state.market_api_key = ""
            state.market_api_key_stored = ""
            state.market_client = None


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
        try:
            tenders_latest = state.market_client.get("/licitaciones") # type: ignore
            state.tenders_latest_data = tenders_latest.get("Listado", [DEFAULT_TENDER_DATA])
            state.tenders_latest_data.sort(key=lambda x: x.get("FechaCierre") or "", reverse=True) # type: ignore
        except BadStatus as error:
            if _is_concurrent_request_error(error):
                st.toast(
                    "⚠️ Existen peticiones simultáneas con la API Key "
                    "de prueba. Intente nuevamente."
                )
            else:
                st.toast(f"❌ {error}")
    
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
                tender_detail = state.market_client.get( # type: ignore
                    "/licitaciones",
                    params={"codigo": tender_code}
                )
                state.tender_detail_data = tender_detail.get("Listado", [])[0] # type: ignore
            except BadStatus as error:
                if _is_concurrent_request_error(error):
                    st.toast(
                        "⚠️ Existen peticiones simultáneas con la API Key "
                        "de prueba. Intente nuevamente."
                    )
                else:
                    st.toast(f"❌ {error}")

    if st.button(label="Reset", type="primary", key="tender_detail_reset"):
        state.tender_detail_data = {}

if state.tender_detail_data: # type: ignore
    st.json(state.tender_detail_data) # type: ignore
