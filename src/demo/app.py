from __future__ import annotations

import streamlit as st

home_page = st.Page("pages/home.py", title="Inicio", icon="🏠")
rut_page = st.Page("pages/rut.py", title="Cálculo y Validación de RUT", icon="🔍")
ppu_page = st.Page("pages/ppu.py", title="Cálculo y Validación de Patente", icon="🔍")

pg = st.navigation([home_page, rut_page, ppu_page])

pg.run()
