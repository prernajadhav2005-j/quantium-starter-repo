import sys
import os

# Ensure project root is in the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from quantium_starter_repo.task_3 import app


# ---------- TEST 1: HEADER IS PRESENT ----------
def test_header_is_present(dash_duo):
    dash_duo.start_server(app)

    header = dash_duo.find_element("h1")
    assert header is not None
    assert "Pink Morsel Sales Dashboard" in header.text


# ---------- TEST 2: LINE CHART EXISTS ----------
def test_line_chart_exists(dash_duo):
    dash_duo.start_server(app)

    chart = dash_duo.find_element("#sales-line-chart")
    assert chart is not None


# ---------- TEST 3: REGION PICKER EXISTS ----------
def test_region_picker_exists(dash_duo):
    dash_duo.start_server(app)

    radio = dash_duo.find_element(".radio-group")
    assert radio is not None
