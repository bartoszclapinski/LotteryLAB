from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import date, datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, desc
from pathlib import Path

from src.database.session import SessionLocal
from src.database.models import Draw
from src.repositories.draws import DrawRepository
from src.analysis.frequency import calculate_frequency, count_draws, get_hot_cold_numbers
from src.analysis.randomness import analyze_number_randomness
from src.analysis.patterns import analyze_patterns
from src.analysis.visualizations import (
    create_correlation_heatmap_data,
    analyze_time_series_trends,
    create_time_series_chart_data
)
from src.services.export import create_full_report
from src.utils.logger import get_logger
from src.utils.i18n import detect_language, get_all_texts, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE
import random

BASE_DIR = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
LOG_DIR = BASE_DIR / ".logs"

logger = get_logger("api", log_file=str(LOG_DIR / "api.log"))


def get_lang_from_request(request: Request) -> str:
    """Extract language from request (query param or cookie)."""
    # Query param has priority
    query_lang = request.query_params.get("lang")
    cookie_lang = request.cookies.get("lang")
    accept_lang = request.headers.get("accept-language")
    return detect_language(cookie_lang, query_lang, accept_lang)


def get_template_context(request: Request, **kwargs) -> dict:
    """Build template context with i18n texts."""
    lang = get_lang_from_request(request)
    texts = get_all_texts(lang)
    return {
        "request": request,
        "lang": lang,
        "supported_languages": SUPPORTED_LANGUAGES,
        **texts,
        **kwargs
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events for the application."""
    # Startup: automatic update from MBNet
    logger.info("🚀 Starting Lottery Lab...")
    try:
        from src.data_acquisition.scheduler import update_from_mbnet
        result = update_from_mbnet()
        inserted = result.get("inserted", 0)
        skipped = result.get("skipped", 0)
        if inserted > 0:
            logger.info(f"✅ Auto-update: {inserted} new draws imported, {skipped} skipped")
            print(f"🎲 Auto-update: {inserted} new draws imported")
        else:
            logger.info(f"ℹ️ Auto-update: No new draws (database up to date)")
            print("🎲 Auto-update: Database already up to date")
    except Exception as e:
        logger.warning(f"⚠️ Auto-update failed: {e}")
        print(f"⚠️ Auto-update failed: {e} (continuing without update)")
    
    yield  # Application runs here
    
    # Shutdown
    logger.info("👋 Shutting down Lottery Lab...")


app = FastAPI(title="Lottery Lab", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000", "http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "version": "0.1.0"}


@app.get("/api/v1/analysis/frequency")
def get_frequency(
    game_type: str = "lotto",
    window_days: Optional[int] = 365,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    game_provider: Optional[str] = None,
):
    with SessionLocal() as session:
        freq = calculate_frequency(
            session=session,
            game_type=game_type,
            date_from=date_from,
            date_to=date_to,
            window_days=window_days,
            game_provider=game_provider,
        )
        num_draws = count_draws(
            session=session,
            game_type=game_type,
            date_from=date_from,
            date_to=date_to,
            window_days=window_days,
            game_provider=game_provider,
        )
    expected_each = num_draws * (6/49) if num_draws else 0.0
    deltas = {k: freq[k] - expected_each for k in freq}
    pct_deltas = {k: ((freq[k] - expected_each) / expected_each * 100.0) if expected_each else 0.0 for k in freq}
    hot_cold = get_hot_cold_numbers(freq, expected_each)
    return {
        "game_type": game_type,
        "window_days": window_days,
        "date_from": str(date_from) if date_from else None,
        "date_to": str(date_to) if date_to else None,
        "game_provider": game_provider,
        "num_draws": num_draws,
        "frequency": freq,
        "expected_each": expected_each,
        "delta": deltas,
        "pct_delta": pct_deltas,
        "hot_numbers": hot_cold["hot"],
        "cold_numbers": hot_cold["cold"],
    }


@app.get("/api/v1/draws")
def list_draws(
    game_type: Optional[str] = None,
    game_provider: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    limit: int = 100,
    offset: int = 0,
):
    with SessionLocal() as session:
        repo = DrawRepository(session)
        items = repo.list(
            game_type=game_type,
            game_provider=game_provider,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset,
        )
        total = repo.count(
            game_type=game_type,
            game_provider=game_provider,
            date_from=date_from,
            date_to=date_to,
        )
        return {"items": items, "total": total}


@app.get("/set-language")
async def set_language(request: Request, lang: str = DEFAULT_LANGUAGE):
    """Set user's preferred language via cookie."""
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
    
    # Redirect back to referer or home
    referer = request.headers.get("referer", "/")
    response = RedirectResponse(url=referer, status_code=303)
    response.set_cookie(
        key="lang",
        value=lang,
        max_age=365 * 24 * 60 * 60,  # 1 year
        httponly=True,
        samesite="lax"
    )
    return response


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    ctx = get_template_context(request, title="Lottery Lab", game_type="lotto")
    return templates.TemplateResponse("index.html", ctx)


@app.get("/partials/frequency", response_class=HTMLResponse)
async def frequency_partial(request: Request, game_type: str = "lotto", window_days: int = 365):
    with SessionLocal() as session:
        freq = calculate_frequency(session, game_type=game_type, window_days=window_days)
        num_draws = count_draws(session, game_type=game_type, window_days=window_days)
    expected_each = num_draws * (6/49) if num_draws else 0.0
    hot_cold = get_hot_cold_numbers(freq, expected_each)
    ctx = get_template_context(
        request,
        frequency=freq,
        game_type=game_type,
        window_days=window_days,
        num_draws=num_draws,
        expected_each=expected_each,
        hot_numbers=hot_cold["hot"],
        cold_numbers=hot_cold["cold"]
    )
    return templates.TemplateResponse("partials/frequency.html", ctx)


@app.get("/partials/recent-draws", response_class=HTMLResponse)
async def recent_draws_partial(request: Request):
    with SessionLocal() as session:
        repo = DrawRepository(session)
        rows = repo.latest(20)
    ctx = get_template_context(request, items=rows)
    return templates.TemplateResponse("partials/recent_draws.html", ctx)


@app.get("/partials/generator", response_class=HTMLResponse)
async def generator_partial(request: Request, game_type: str = "lotto"):
    with SessionLocal() as session:
        freq = calculate_frequency(session, game_type=game_type, window_days=365)
        num_draws = count_draws(session, game_type=game_type, window_days=365)
    expected_each = num_draws * (6/49) if num_draws else 0.0
    hot_cold = get_hot_cold_numbers(freq, expected_each)

    # Generate a set favoring hot numbers
    hot_nums = hot_cold["hot"]
    cold_nums = hot_cold["cold"]
    neutral_nums = [n for n in range(1, 50) if n not in hot_nums and n not in cold_nums]

    # Weight: 40% hot, 40% neutral, 20% cold (to avoid extreme cold numbers)
    weights = ([0.4] * len(hot_nums) +
               [0.4] * len(neutral_nums) +
               [0.2] * len(cold_nums))
    all_nums = hot_nums + neutral_nums + cold_nums

    # Generate 6 unique numbers
    generated = set()
    while len(generated) < 6:
        num = random.choices(all_nums, weights=weights, k=1)[0]
        generated.add(num)

    generated_sorted = sorted(list(generated))

    ctx = get_template_context(
        request,
        game_type=game_type,
        generated_numbers=generated_sorted,
        hot_numbers=hot_nums,
        cold_numbers=cold_nums
    )
    return templates.TemplateResponse("partials/generator.html", ctx)


@app.get("/partials/randomness", response_class=HTMLResponse)
async def randomness_partial(request: Request, game_type: str = "lotto", window_days: int = 365):
    """Get HTML partial for randomness analysis display."""
    with SessionLocal() as session:
        result = analyze_number_randomness(
            session=session,
            game_type=game_type,
            window_days=window_days,
        )

    # Remove keys that conflict with template context
    result.pop("game_type", None)
    result.pop("analysis_period", None)  # Contains window_days
    
    ctx = get_template_context(
        request,
        game_type=game_type,
        window_days=window_days,
        **result
    )
    return templates.TemplateResponse("partials/randomness.html", ctx)


@app.get("/partials/patterns", response_class=HTMLResponse)
async def patterns_partial(request: Request, game_type: str = "lotto", window_days: int = 365):
    """Get HTML partial for pattern analysis display."""
    with SessionLocal() as session:
        result = analyze_patterns(
            session=session,
            game_type=game_type,
            window_days=window_days,
        )

    # Remove keys that conflict with template context
    result.pop("game_type", None)
    
    ctx = get_template_context(
        request,
        game_type=game_type,
        window_days=window_days,
        **result
    )
    return templates.TemplateResponse("partials/patterns.html", ctx)


@app.get("/partials/correlation", response_class=HTMLResponse)
async def correlation_partial(request: Request, game_type: str = "lotto", window_days: int = 365):
    """Get HTML partial for correlation heatmap display."""
    with SessionLocal() as session:
        result = create_correlation_heatmap_data(
            session=session,
            game_type=game_type,
            window_days=window_days,
        )

    # Remove keys that conflict with template context
    result.pop("game_type", None)
    
    ctx = get_template_context(
        request,
        game_type=game_type,
        window_days=window_days,
        **result
    )
    return templates.TemplateResponse("partials/correlation.html", ctx)


@app.get("/api/v1/analysis/patterns")
def get_pattern_analysis(
    request: Request,
    game_type: str = "lotto",
    window_days: int = 365
):
    """Get comprehensive pattern analysis for lottery draws."""
    with SessionLocal() as session:
        result = analyze_patterns(
            session=session,
            game_type=game_type,
            window_days=window_days,
        )

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result


@app.get("/api/v1/analysis/correlation")
def get_correlation_analysis(
    game_type: str = "lotto",
    window_days: int = 365
):
    """Get correlation analysis for number relationships."""
    with SessionLocal() as session:
        result = create_correlation_heatmap_data(
            session=session,
            game_type=game_type,
            window_days=window_days,
        )

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result


@app.get("/api/v1/analysis/randomness")
def get_randomness_analysis(
    game_type: str = "lotto",
    window_days: Optional[int] = 365,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    game_provider: Optional[str] = None,
):
    """Get comprehensive randomness analysis for lottery draws."""
    with SessionLocal() as session:
        result = analyze_number_randomness(
            session=session,
            game_type=game_type,
            date_from=date_from,
            date_to=date_to,
            window_days=window_days,
            game_provider=game_provider,
        )
    return result


@app.get("/api/v1/analysis/trends")
def get_trends_analysis(
    game_type: str = "lotto",
    period: str = "month",
    num_periods: int = 12
):
    """Get time series trend analysis for lottery numbers."""
    with SessionLocal() as session:
        result = analyze_time_series_trends(
            session=session,
            game_type=game_type,
            period=period,
            num_periods=num_periods,
        )
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result


@app.get("/api/v1/analysis/trends/chart")
def get_trends_chart_data(
    game_type: str = "lotto",
    period: str = "month",
    num_periods: int = 12,
    numbers: Optional[str] = None
):
    """Get chart-ready time series data for selected numbers."""
    # Parse numbers from comma-separated string
    number_list = None
    if numbers:
        try:
            number_list = [int(n.strip()) for n in numbers.split(',') if n.strip()]
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid numbers format")
    
    with SessionLocal() as session:
        result = create_time_series_chart_data(
            session=session,
            game_type=game_type,
            numbers=number_list,
            period=period,
            num_periods=num_periods,
        )
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result


@app.get("/partials/trends", response_class=HTMLResponse)
async def trends_partial(
    request: Request,
    game_type: str = "lotto",
    period: str = "month",
    num_periods: int = 12
):
    """Get HTML partial for time series trend analysis display."""
    with SessionLocal() as session:
        result = analyze_time_series_trends(
            session=session,
            game_type=game_type,
            period=period,
            num_periods=num_periods,
        )
        
        chart_data = create_time_series_chart_data(
            session=session,
            game_type=game_type,
            period=period,
            num_periods=num_periods,
        )

    # Remove keys that conflict with template context
    result.pop("game_type", None)
    chart_data.pop("game_type", None)
    
    ctx = get_template_context(
        request,
        game_type=game_type,
        period=period,
        num_periods=num_periods,
        chart_data=chart_data,
        **result
    )
    return templates.TemplateResponse("partials/trends.html", ctx)


@app.get("/api/v1/export/report")
async def export_report(
    request: Request,
    format: str = "pdf",
    game_type: str = "lotto",
    window_days: int = 365,
    include_frequency: bool = True,
    include_randomness: bool = True,
    include_patterns: bool = True,
    include_draws: bool = True
):
    """
    Export comprehensive analysis report as PDF or Excel.
    
    Args:
        format: Export format ('pdf' or 'excel')
        game_type: Type of lottery game
        window_days: Analysis window in days
        include_frequency: Include frequency analysis
        include_randomness: Include randomness tests
        include_patterns: Include pattern analysis
        include_draws: Include recent draws (Excel only)
    """
    if format not in ["pdf", "excel"]:
        raise HTTPException(status_code=400, detail="Format must be 'pdf' or 'excel'")
    
    lang = get_lang_from_request(request)
    
    frequency_data = None
    randomness_data = None
    patterns_data = None
    draws_data = None
    
    with SessionLocal() as session:
        if include_frequency:
            freq = calculate_frequency(session, game_type=game_type, window_days=window_days)
            num_draws = count_draws(session, game_type=game_type, window_days=window_days)
            expected_each = num_draws * (6/49) if num_draws else 0.0
            hot_cold = get_hot_cold_numbers(freq, expected_each)
            frequency_data = {
                "game_type": game_type,
                "window_days": window_days,
                "num_draws": num_draws,
                "frequency": freq,
                "expected_each": expected_each,
                "hot_numbers": hot_cold["hot"],
                "cold_numbers": hot_cold["cold"],
            }
        
        if include_randomness:
            randomness_data = analyze_number_randomness(
                session=session,
                game_type=game_type,
                window_days=window_days,
            )
        
        if include_patterns:
            patterns_data = analyze_patterns(
                session=session,
                game_type=game_type,
                window_days=window_days,
            )
        
        if include_draws and format == "excel":
            repo = DrawRepository(session)
            draws_data = repo.latest(100)
    
    # Generate report
    buffer = create_full_report(
        frequency_data=frequency_data,
        randomness_data=randomness_data,
        patterns_data=patterns_data,
        draws_data=draws_data,
        format=format,
        language=lang,
        game_type=game_type,
        window_days=window_days
    )
    
    # Set filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    if format == "pdf":
        filename = f"lottery_report_{game_type}_{timestamp}.pdf"
        media_type = "application/pdf"
    else:
        filename = f"lottery_report_{game_type}_{timestamp}.xlsx"
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    return StreamingResponse(
        buffer,
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
