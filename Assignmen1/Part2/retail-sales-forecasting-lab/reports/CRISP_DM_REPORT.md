# Retail Sales Forecasting Lab — CRISP-DM Report

## Business understanding

Store teams need a simple view of expected demand so they can plan inventory, staffing, promotions, and maintenance. The project forecasts weekly sales for a selected store and highlights the highest and lowest expected future weeks.

## Data understanding

The project uses the Kaggle Walmart Store Sales Forecasting schema: Store, Date, Weekly_Sales, Holiday_Flag, Temperature, Fuel_Price, CPI, and Unemployment. The included fallback is synthetic and exists only to make the demonstration reproducible without a download.

## Data preparation

Dates and sales are parsed, invalid records are removed, and duplicate store-weeks are dropped. Features include week-of-year, month, trend index, annual sine/cosine terms, lag-1 and lag-4 sales, rolling four-week mean, and holiday flag.

## Modeling

The model is Ridge regression because it is transparent and fast for a student project. It is compared with a seasonal-naive baseline that uses the value from four weeks earlier. For future recursion, each forecast becomes an input to the next step.

## Evaluation

The last 20% of usable observations are held out chronologically. MAE is easy to interpret as average dollar error; RMSE gives additional weight to large misses. A random split is avoided because it would allow future information into training.

## Business insights

High forecast weeks are candidates for extra inventory, labor, and campaign capacity. Low forecast weeks are candidates for targeted offers, maintenance, and leaner replenishment. Holiday flags and seasonal peaks should be checked with store managers before operational decisions.

## Limitations and next steps

The simple model does not capture promotions, stockouts, price changes, product-level demand, or hierarchical store relationships. Add richer exogenous features, rolling-origin backtesting, prediction intervals, and production monitoring before using forecasts for high-stakes replenishment.

