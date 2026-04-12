from __future__ import annotations

import streamlit as st

home_page = st.Page("pages/home.py", title="Inicio", icon="🏠")
rut_page = st.Page("pages/rut.py", title="Rut", icon=":material/person:")
ppu_page = st.Page("pages/ppu.py", title="Patente", icon=":material/airport_shuttle:")
cmf_page = st.Page("pages/cmf.py", title="CMF", icon=":material/account_balance:")
market_page = st.Page("pages/market.py", title="Mercado Público", icon=":material/store:")

pg = st.navigation(
    {
        "Bienvenido": [home_page],
        "Validación": [rut_page, ppu_page],
        "Clientes API": [cmf_page, market_page],
    }
)

pg.run()
