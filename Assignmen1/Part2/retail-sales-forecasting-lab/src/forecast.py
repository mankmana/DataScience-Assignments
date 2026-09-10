import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error


def features(df):
    x = df.copy().sort_values("Date").reset_index(drop=True)
    x["trend"] = np.arange(len(x))
    x["week"] = x.Date.dt.isocalendar().week.astype(int)
    x["month"] = x.Date.dt.month
    x["sin52"] = np.sin(2 * np.pi * x["week"] / 52)
    x["cos52"] = np.cos(2 * np.pi * x["week"] / 52)
    x["lag1"] = x.Weekly_Sales.shift(1)
    x["lag4"] = x.Weekly_Sales.shift(4)
    x["rolling4"] = x.Weekly_Sales.shift(1).rolling(4).mean()
    return x.dropna().reset_index(drop=True)


def fit_forecast(df, horizon=12):
    x = features(df)
    cols = ["trend", "week", "month", "sin52", "cos52", "lag1", "lag4", "rolling4", "Holiday_Flag"]
    split = max(int(len(x) * .8), len(x) - 26)
    train, test = x.iloc[:split], x.iloc[split:]
    model = Ridge(alpha=10.0).fit(train[cols], train.Weekly_Sales)
    pred = model.predict(test[cols])
    baseline = test.lag4.to_numpy()
    metrics = {"model_mae": float(mean_absolute_error(test.Weekly_Sales, pred)), "model_rmse": float(np.sqrt(mean_squared_error(test.Weekly_Sales, pred))), "baseline_mae": float(mean_absolute_error(test.Weekly_Sales, baseline)), "baseline_rmse": float(np.sqrt(mean_squared_error(test.Weekly_Sales, baseline)))}
    history = pd.DataFrame({"Date": test.Date, "Actual": test.Weekly_Sales, "Predicted": pred, "Baseline": baseline})
    last = x.iloc[-1].copy()
    future = []
    values = list(x.Weekly_Sales)
    for i in range(horizon):
        date = last.Date + pd.Timedelta(weeks=i + 1)
        week = int(date.isocalendar().week)
        holiday = int(date.month in [11, 12] and date.day > 15)
        row = {"Date": date, "trend": last.trend + i + 1, "week": week, "month": date.month, "sin52": np.sin(2 * np.pi * week / 52), "cos52": np.cos(2 * np.pi * week / 52), "lag1": values[-1], "lag4": values[-4], "rolling4": np.mean(values[-4:]), "Holiday_Flag": holiday}
        value = float(model.predict(pd.DataFrame([row])[cols])[0]); future.append({"Date": date, "Forecast": value, "Holiday_Flag": holiday}); values.append(value)
    return history, pd.DataFrame(future), metrics

