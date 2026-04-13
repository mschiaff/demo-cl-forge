# Streamlit CL Forge Demo

> Interactive web app showcasing [**CL Forge**](https://github.com/mschiaff/cl-forge) — high-performance Chilean data tools written in Rust & Python.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app.streamlit.app)
[![cl-forge](https://img.shields.io/pypi/v/cl-forge?label=cl-forge&color=blue)](https://pypi.org/project/cl-forge/)
[![Python](https://img.shields.io/badge/python-≥3.13-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)

## Overview

This repository contains a **Streamlit web application** that demonstrates the capabilities of the [`cl-forge`](https://github.com/mschiaff/cl-forge) library. `cl-forge` provides a collection of high-performance utilities for common Chilean data formats and API integrations, with its core logic implemented in Rust and a clean Python interface.

The goal of this demo is to let you **interact** with the library's features directly in your browser — no installation required.

📖 **Library docs**: [mschiaff.github.io/cl-forge](https://mschiaff.github.io/cl-forge/)

## Live Demo

👉 **[Open the app](https://your-app.streamlit.app)** — hosted on Streamlit Community Cloud.

No setup needed. Just open the link and start exploring.

## Features Demonstrated

The app is organized into sections that showcase different parts of the library:

### Validation

- **RUT** — Calculate and validate the check digit of a Chilean RUT/RUN (national ID number) using `cl_forge.verify`.
- **License Plate (PPU)** — Calculate and validate the check digit of Chilean vehicle license plates, with automatic format detection.

### API Clients

- **CMF (Financial Market Commission)** — Query real Consumer Price Index (IPC) data from the [CMF API](https://api.cmfchile.cl/), view current values or full-year history, and toggle between table and chart views.
- **Mercado Público (Public Market)** — Browse the latest government tenders and look up tender details using the [Mercado Público API](https://api.mercadopublico.cl/).

## Run Locally

### Prerequisites

- **Python ≥ 3.13**
- [**uv**](https://docs.astral.sh/uv/) (recommended) or pip

### Steps

```bash
# Clone the repository
git clone https://github.com/mschiaff/demo-cl-forge.git
cd demo-cl-forge

# Install dependencies
uv sync

# Run the app (recommended)
uv run streamlit run src/demo/app.py

# Alternative (if not using uv)
python -m streamlit run src/demo/app.py
```

The app will open in your browser at `http://localhost:8501`.

> **Note**: The CMF and Mercado Público pages require API keys to fetch live data. You can enter them in the sidebar of each page. See the [cl-forge docs](https://mschiaff.github.io/cl-forge/) for details on how to obtain them.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Core library | [`cl-forge`](https://github.com/mschiaff/cl-forge) (Rust + Python) |
| Web framework | [Streamlit](https://streamlit.io/) |
| Python | ≥ 3.13 |
| Package manager | [uv](https://docs.astral.sh/uv/) |

## License

This project is licensed under the Apache 2.0 License — see the [LICENSE](LICENSE) file for details.