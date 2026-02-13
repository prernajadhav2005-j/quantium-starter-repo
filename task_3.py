import pandas as pd
from dash import Dash, dcc, html
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

df["period"] = df["date"].apply(lambda x: "Before Price Increase" if x < price_change_date else "After Price Increase")


daily_sales = df.groupby("date")["sales"].sum().reset_index()



app = Dash(__name__)

fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Daily Sales of Pink Morsels (Before vs After Price Increase)",
    markers=True,
)

app.layout = html.Div([
    html.H1("Pink Morsel Sales Dashboard", style={"textAlign": "center"}),

    dcc.Graph(figure=fig),

    html.H3("Sales Before vs After Price Increase", style={"marginTop": "40px"}),

    dcc.Graph(
        figure=px.bar(
            df.groupby("period")["sales"].sum().reset_index(),
            x="period",
            y="sales",
            title="Comparison of Total Sales",
            color="period"
        )
    )
])


if __name__ == "__main__":
    app.run(debug=True)
