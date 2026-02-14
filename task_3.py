import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

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

price_change_date = pd.to_datetime("2021-01-15")
df["period"] = df["date"].apply(
    lambda x: "Before Price Increase" if x < price_change_date else "After Price Increase"
)

# -------------------- DASH APP --------------------

app = Dash(__name__)

app.layout = html.Div(
    className="main-container",
    children=[
        html.H1("🌸 Pink Morsel Sales Dashboard", className="title"),

        html.Div(
            className="filter-card",
            children=[
                html.H3("Filter by Region", className="filter-title"),

                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": " All", "value": "all"},
                        {"label": " North", "value": "north"},
                        {"label": " East", "value": "east"},
                        {"label": " South", "value": "south"},
                        {"label": " West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    className="radio-group"
                )
            ]
        ),

        html.Div(
            className="chart-card",
            children=[
                dcc.Graph(id="sales-line-chart")
            ]
        ),

        html.Div(
            className="chart-card",
            children=[
                dcc.Graph(
                    figure=px.bar(
                        df.groupby("period")["sales"].sum().reset_index(),
                        x="period",
                        y="sales",
                        color="period",
                        title="Total Sales Before vs After Price Increase",
                        color_discrete_sequence=["#EC4899", "#F472B6"]
                    )
                )
            ]
        ),
    ]
)


# -------------------- CALLBACK FOR INTERACTIVE LINE CHART --------------------

@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value")
)
def update_line_chart(selected_region):

    filtered_df = df if selected_region == "all" else df[df["region"].str.lower() == selected_region]
    daily_sales = filtered_df.groupby("date")["sales"].sum().reset_index()

    fig = px.line(
        daily_sales,
        x="date",
        y="sales",
        markers=True,
        color_discrete_sequence=["#DB2777"],
        title=f"Daily Sales Trend — {selected_region.upper()} Region"
    )

    fig.update_layout(
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(size=14),
        title_font=dict(size=22, color="#BE185D"),
        xaxis_title="Date",
        yaxis_title="Sales",
    )

    return fig


# -------------------- RUN APP --------------------

if __name__ == "__main__":
    app.run(debug=True)
