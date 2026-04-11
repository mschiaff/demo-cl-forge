from __future__ import annotations

import streamlit as st
from cl_forge import verify
from streamlit import session_state as state

st.set_page_config(
    page_title="Cálculo y Validación de Patente",
    page_icon="🔍"
)

st.markdown(
    """
    <style>
        .st-key-validate-result .stAlertContainer {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


if "calculate_ppu_reset_counter" not in state:
    state.calculate_ppu_reset_counter: int = 0 # type: ignore

if "validate_ppu_reset_counter" not in state:
    state.validate_ppu_reset_counter: int = 0 # type: ignore


def _increment_calculate_ppu_reset_counter() -> None:
    state.calculate_ppu_reset_counter += 1

def _get_calculate_ppu_input_key() -> str:
    return f"calculate_ppu_input_{state.calculate_ppu_reset_counter}"

def _increment_validate_ppu_reset_counter() -> None:
    state.validate_ppu_reset_counter += 1

def _get_validate_ppu_input_key() -> str:
    return f"validate_ppu_input_{state.validate_ppu_reset_counter}"


def calculate_digit():
    col1, col2 = st.columns(
        spec=2,
        vertical_alignment="center"
    )

    with col1:
        raw_ppu = st.text_input(
            label="Ingrese Patente",
            placeholder="Ej: PHZF55",
            key=_get_calculate_ppu_input_key(),
        )
        
        ppu: verify.Ppu | None = (
            verify.Ppu(raw_ppu)
            if raw_ppu else None
        )

    with col2:
        st.text_input(
            label="Dígito Verificador",
            value=ppu.verifier if ppu else "",
            disabled=True,
        )

    if ppu:
        st.code(f"{ppu.normalized}-{ppu.verifier}")
    
    st.button(
        label="Reset",
        key="calculate_ppu_reset",
        type="primary",
        on_click=_increment_calculate_ppu_reset_counter,
        use_container_width=True,
    )


def validate_digit():
    col1, col2 = st.columns(
        spec=2,
        vertical_alignment="bottom"
    )

    with col1:
        ppu_digit = st.text_input(
            label="Ingrese Patente",
            placeholder="Ej: PHZF55-3",
            key=_get_validate_ppu_input_key(),
        )

        raw_ppu, raw_digit = (
            ppu_digit.split("-")
            if ppu_digit else (None, None)
        )

        ppu: verify.Ppu | None = (
            verify.Ppu(raw_ppu)
            if raw_ppu else None
        )
    
    with col2:
        if ppu and isinstance(raw_digit, str):
            status = ppu.verifier == raw_digit.upper()

            with st.container(key="validate-result"):
                if status:
                    st.success("Patente válida")
                else:
                    st.error("Patente inválida")

    st.button(
        label="Reset",
        key="validate_ppu_reset",
        type="primary",
        on_click=_increment_validate_ppu_reset_counter,
        use_container_width=True,
    )


st.title("Cálculo y Validación de Patente")

st.subheader("Calcular dígito verificador")
calculate_digit()

st.subheader("Validar dígito verificador")
validate_digit()
