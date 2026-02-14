import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# ---------- LOAD & CLEAN DATA ----------
files = [
    "data/daily_sales_data_0.csv",
    "data/daily_sales_data_1.csv",
    "data/daily_sales_data_2.csv"
]

df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

df["product"] = df["product"].str.strip().str.lower()
df = df[df["product"] == "pink morsel"]

df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)
df["sales"] = df["quantity"] * df["price"]
df["date"] = pd.to_datetime(df["date"])

# Ensure region exists (some datasets lack region)
if "region" not in df.columns:
    df["region"] = "all"

# ---------- DASH APP ----------
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Pink Morsel Sales Dashboard", id="main-header", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Region:"),
        dcc.RadioItems(
            id="radio-group",
            className="radio-group",
            options=[
                {"label": "North", "value": "north"},
                {"label": "South", "value": "south"},
                {"label": "East", "value": "east"},
                {"label": "West", "value": "west"},
                {"label": "All Regions", "value": "all"},
            ],
            value="all",
            inline=True
        )
    ], style={"marginBottom": "20px"}),

    dcc.Graph(id="sales-line-chart")
])

# ---------- CALLBACK ----------
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("radio-group", "value")
)
def update_line_chart(region):
    filtered = df if region == "all" else df[df["region"] == region]

    fig = px.line(
        filtered,
        x="date",
        y="sales",
        title=f"Pink Morsel Sales Over Time — Region: {region.capitalize()}",
        markers=True
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)
