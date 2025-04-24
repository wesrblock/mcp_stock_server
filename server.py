# server.py
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
import yfinance as yf

app = FastAPI(
    title="Quote Server",
    version="1.1",
    description="Exposes an MCP-style tool that returns live stock prices."
)

# ────────────────────────── 1.  Stock-price endpoint ──────────────────────────
@app.get("/v1/getquote")
async def get_quote(tickers: list[str] = Query(..., description="One or more stock symbols")):
    """
    /v1/getquote?tickers=AAPL&tickers=MSFT
    /v1/getquote?tickers=AAPL,MSFT,GOOG
    """
    # Accept both repeated keys and comma-separated list
    if len(tickers) == 1 and "," in tickers[0]:
        tickers = [t.strip() for t in tickers[0].split(",") if t.strip()]

    if not tickers:
        raise HTTPException(status_code=400, detail="No tickers supplied.")

    prices: dict[str, float | None] = {}
    for symbol in tickers:
        try:
            prices[symbol.upper()] = yf.Ticker(symbol).fast_info.get("lastPrice")
        except Exception:
            prices[symbol.upper()] = None

    return JSONResponse({"data": prices})

# ────────────────────────── 2.  Tool-description endpoint ─────────────────────
@app.get("/v1/tool")
async def tool_description():
    """
    Returns only the description string expected by an MCP client.
    """
    return JSONResponse(
        {
            "description": "Return current stock price(s) for the provided ticker symbols."
        }
    )

# Run locally:
# uvicorn server:app --host 0.0.0.0 --port 8000 --reload
