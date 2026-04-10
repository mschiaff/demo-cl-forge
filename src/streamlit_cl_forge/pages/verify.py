from __future__ import annotations

import streamlit as st
from cl_forge import verify
from streamlit import session_state as state


if "calculate_reset_counter" not in state:
    state.calculate_reset_counter: int = 0 # type: ignore


def _increment_reset_counter() -> None:
    state.calculate_reset_counter += 1

def _get_calculate_input_key() -> str:
    return f"calculate_rut_input_{state.calculate_reset_counter}"


def calculate_digit():
    col1, col2 = st.columns(
        spec=2,
        vertical_alignment="center"
    )

    with col1:
        rut = st.text_input(
            label="Ingrese RUT",
            placeholder="Ej: 8750720",
            key=_get_calculate_input_key(),
        )

    with col2:
        digit = st.text_input(
            label="Dígito Verificador",
            value=verify.calculate_verifier(
                int(rut)
            ) if rut else "",
            disabled=True,
        )
    
    st.button(
        label="Reset",
        key="calculate_reset",
        on_click=_increment_reset_counter
    )

    if rut and digit:
        st.code(f"{rut}-{digit}")


def validate_digit():
    col1, col2 = st.columns(
        spec=2,
        vertical_alignment="center"
    )

    with col1:
        rut_digit = st.text_input(
            label="Ingrese RUT",
            placeholder="Ej: 8755183-0"
        )
    
    with col2:
        rut, digit = (
            rut_digit.split("-")
            if rut_digit else (None, None)
        )
        
        if rut and digit:
            status = verify.validate_rut(
                digits=int(rut),
                verifier=digit
            )

            st.text_input(
                label="Resultado",
                value="Válido" if status else "Inválido",
                disabled=True,
            )


st.title("Módulo de RUT")

st.subheader("Calcular dígito verificador")
calculate_digit()


st.subheader("Validar dígito verificador")
validate_digit()
