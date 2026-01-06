# Magrathea Notebooks

This directory contains Jupyter notebooks for interactive development and visualization of the Magrathea project.

## Getting Started

1.  **Install Dependencies**: Ensure you have the development dependencies installed.
    ```bash
    uv sync
    ```

2.  **Launch Jupyter Lab**: Run the following command from the project root:
    ```bash
    uv run jupyter lab
    ```

3.  **Open Playground**: Navigate to `notebooks/playground.ipynb` in the Jupyter interface.

## Features

-   **Autoreload**: The playground notebook is configured to automatically reload changes made to the `magrathea` package, allowing for rapid iteration on the rendering engine.
-   **Visualization**: Uses `matplotlib` to verify map generation logic visually.
