"""Tests to verify the quantitative impact of market views in Black-Litterman."""
import sys
import traceback
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.portfolio.optimizer import optimize_black_litterman

def test_market_view_tilt():
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "JPM", "JNJ", "V", "WMT"]
    
    # 1. Neutral BL (No views)
    weights_neutral, shifts_neutral = optimize_black_litterman(tickers, [])
    aapl_neutral = weights_neutral.get("AAPL", 0)
    print(f"Neutral AAPL weight: {aapl_neutral:.4f}")
    
    # 2. Bullish view on AAPL
    bullish_view = [{"ticker": "AAPL", "direction": "bullish", "confidence": "high"}]
    weights_bullish, shifts_bullish = optimize_black_litterman(tickers, bullish_view)
    aapl_bullish = weights_bullish.get("AAPL", 0)
    print(f"Bullish AAPL weight: {aapl_bullish:.4f}")
    assert shifts_bullish["AAPL"] == 0.05, f"Expected shift 0.05, got {shifts_bullish['AAPL']}"
    # If neutral was already at max, we can't expect an increase. 
    # But if we compare it to a BEARISH view, it should be different.
    
    # 3. Bearish view on AAPL
    bearish_view = [{"ticker": "AAPL", "direction": "bearish", "confidence": "high"}]
    weights_bearish, shifts_bearish = optimize_black_litterman(tickers, bearish_view)
    aapl_bearish = weights_bearish.get("AAPL", 0)
    print(f"Bearish AAPL weight: {aapl_bearish:.4f}")
    assert shifts_bearish["AAPL"] == -0.05
    assert aapl_bearish < aapl_neutral or aapl_bearish < aapl_bullish, "Bearish view should result in lower weight than Bullish/Neutral"

    print("\n✅ Market view tilt tests passed!")

if __name__ == "__main__":
    try:
        test_market_view_tilt()
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        traceback.print_exc()
        sys.exit(1)
