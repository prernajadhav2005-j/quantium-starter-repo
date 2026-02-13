import pandas as pd
df=pd.read_csv("data/daily_sales_data_0.csv")
print(df)

df = df[df["product"].str.lower() == "pink morsel"]

df["price"]=df["price"].str.replace("$","",regex=False).astype(float)
df["sales"]=df["quantity"]* df["price"]

df["date"] = pd.to_datetime(df["date"])
df=df[["sales","date","region"]]
df.to_csv("cleaned_data.csv", index=False)

dff=pd.read_csv("cleaned_data.csv")
print(dff)