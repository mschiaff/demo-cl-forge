from __future__ import annotations

import streamlit as st


home_page = st.Page("pages/home.py", title="Inicio", icon="🏠")
verify_page = st.Page("pages/verify.py", title="Cálculo y Validación de RUT", icon="🔍")

pg = st.navigation([home_page, verify_page])

pg.run()