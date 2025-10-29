import random
import reflex as rx

from rxconfig import config


# --- Datos Falsos (Hardcoded) ---

# Datos de ETRs por tramo
fake_etr_data = {
    "Tramo 1": [
        {"id": "ETR-101", "status": "green", "refs_total": 10, "refs_read": 10, "prisms_total": 50, "prisms_read": 48, "coords": {"x": 10, "y": 20}},
        {"id": "ETR-102", "status": "orange", "refs_total": 8, "refs_read": 7, "prisms_total": 60, "prisms_read": 55, "coords": {"x": 40, "y": 50}},
        {"id": "ETR-103", "status": "red", "refs_total": 9, "refs_read": 4, "prisms_total": 45, "prisms_read": 20, "coords": {"x": 70, "y": 30}}
    ],
    "Tramo 2": [
        {"id": "ETR-201", "status": "green", "refs_total": 12, "refs_read": 12, "prisms_total": 70, "prisms_read": 70, "coords": {"x": 25, "y": 40}},
        {"id": "ETR-202", "status": "green", "refs_total": 10, "refs_read": 10, "prisms_total": 65, "prisms_read": 64, "coords": {"x": 65, "y": 60}}
    ],
    "Tramo 3": [
        {"id": "ETR-301", "status": "orange", "refs_total": 7, "refs_read": 7, "prisms_total": 50, "prisms_read": 40, "coords": {"x": 50, "y": 50}}
    ]
}

# Generador de datos falsos de prismas para el mapa
fake_prism_data = {}
etr_colors = ["var(--blue-9)", "var(--green-9)", "var(--purple-9)", "var(--amber-9)", "var(--cyan-9)"]
color_idx = 0
for tramo_id, etrs in fake_etr_data.items():
    fake_prism_data[tramo_id] = {}
    for etr in etrs:
        etr_id = etr["id"]
        base_x = etr["coords"]["x"]
        base_y = etr["coords"]["y"]
        color = etr_colors[color_idx % len(etr_colors)]
        color_idx += 1
        fake_prism_data[tramo_id][etr_id] = []
        for _ in range(etr["prisms_total"]):
            fake_prism_data[tramo_id][etr_id].append({
                "x": base_x + random.uniform(-10, 10), # Posición relativa al ETR
                "y": base_y + random.uniform(-10, 10), # Posición relativa al ETR
                "color": color
            })


# --- Estado de la Aplicación ---

class State(rx.State):
    """El estado de la aplicación."""

    # Lista de tramos disponibles
    tramos: list[str] = list(fake_etr_data.keys())
    # Tramo seleccionado actualmente
    selected_tramo: str = tramos[0]

    # Contenedores de todos los datos (simulando carga desde una fuente externa)
    _all_etr_data: dict = fake_etr_data
    _all_prism_data: dict = fake_prism_data

    # --- Variables Computadas (KPIs y datos reactivos) ---

    @rx.var
    def etrs(self) -> list[dict]:
        """Obtiene las ETRs para el tramo seleccionado."""
        return self._all_etr_data.get(self.selected_tramo, [])
    
    @rx.var
    def prisms_by_etr(self) -> dict[str, list[dict]]:
        """Obtiene los prismas (agrupados por ETR) para el tramo seleccionado."""
        return self._all_prism_data.get(self.selected_tramo, {})
    
    @rx.var
    def flat_prisms(self) -> list[dict]:
        """Obtiene una lista plana de todos los prismas del tramo para el mapa."""
        all_prisms = []
        for etr_id, prism_list in self.prisms_by_etr.items():
            all_prisms.extend(prism_list)
        return all_prisms
    
    @rx.var
    def total_etrs(self) -> int:
        """Calcula el total de ETRs en el tramo seleccionado."""
        return len(self.etrs)
    
    @rx.var
    def total_prisms(self) -> int:
        """Calcula el total de prismas en el tramo seleccionado."""
        return sum(etr["prisms_total"] for etr in self.etrs)
    
    @rx.var
    def avg_prisms_per_etr(self) -> float:
        """Calcula el promedio de prismas por ETR en el tramo seleccionado."""
        if not self.etrs:
            return 0.0
        return self.total_prisms / self.total_etrs
    
    @rx.var
    def total_references(self) -> int:
        """Calcula el total de referencias en el tramo seleccionado."""
        return sum(etr["refs_total"] for etr in self.etrs)
    
    @rx.var
    def avg_references_per_etr(self) -> float:
        """Calcula el promedio de referencias por ETR en el tramo seleccionado."""
        if not self.etrs:
            return 0.0
        return self.total_references / self.total_etrs

    # --- Eventos ---

    @rx.event
    def set_selected_tramo(self, value: str) -> None:
        self.selected_tramo = value

# --- Componentes Auxiliares de la UI ---

def kpi_card(title: str, value: rx.Var | str) -> rx.Component:
    """Componente para una tarjeta de indicador (KPI)."""
    return rx.card(
        rx.vstack(
            rx.text(title, size="2", color_scheme="gray"),
            rx.heading(value, size="7"),
            spacing="1",
        ),
        as_child=True,
    )


# --- Página Principal ---

def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            # Fila 1: Título y Selector de Tramo
            rx.flex(
                rx.heading("Dashboard ETR Checker - L9 - Barcelona", size="8"),
                rx.spacer(),
                rx.select(
                    State.tramos,
                    value=State.selected_tramo,
                    on_change=State.set_selected_tramo,
                    size="3",
                ),
                rx.color_mode.button(),
                spacing="4",
                align="center",
                width="100%",
            )
        )
    )


app = rx.App()
app.add_page(index)
