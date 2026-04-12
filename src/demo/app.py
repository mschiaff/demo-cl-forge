from __future__ import annotations

import streamlit as st

home_page = st.Page("pages/home.py", title="Inicio", icon="🏠")
rut_page = st.Page("pages/rut.py", title="Rut", icon=":material/person:")
ppu_page = st.Page("pages/ppu.py", title="Patente", icon=":material/airport_shuttle:")

pg = st.navigation(
    {
        "Bienvenido": [home_page],
        "Validación": [rut_page, ppu_page],
    }
)

pg.run()
