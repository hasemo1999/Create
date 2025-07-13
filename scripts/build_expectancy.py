from pathlib import Path
import datetime as dt
import pandas as pd

HISTORY_CSV = Path("data/history.csv")
EXPECT_MD   = Path("docs/expectancy.md")
SUMMARY_MD  = Path("docs/100倍まとめ.md")

def calc_expectancy(df: pd.DataFrame) -> float:
    """
    Expected Value = (勝率 × 平均勝ち) － (負け率 × 平均負け)
    """
    wins   = df[df["Profit"] > 0]["Profit"]
    losses = df[df["Profit"] < 0]["Profit"].abs()
    win_rate = len(wins) / len(df)
    expect = win_rate * wins.mean() - (1 - win_rate) * losses.mean()
    return expect, win_rate

def main() -> None:
    if not HISTORY_CSV.exists():
        raise SystemExit(f"取引履歴 {HISTORY_CSV} が見つかりません")

    df = pd.read_csv(HISTORY_CSV)
    expect, win_rate = calc_expectancy(df)

    # 期待値レポートを Markdown で作成
    report = f"""\
# 期待値レポート {dt.date.today():%Y-%m-%d}

| 指標 | 数値 |
|------|------|
| 勝率 | **{win_rate:.1%}** |
| 期待値 | **{expect:+.2f} pips** |
"""

    EXPECT_MD.write_text(report, encoding="utf-8")
    print("✅ docs/expectancy.md を更新しました")

    # --- 100倍まとめ.md の末尾に今月のダッシュボードを追記 ---
    with SUMMARY_MD.open("a", encoding="utf-8") as f:
        f.write("\n\n## 今月の期待値ダッシュボード\n")
        f.write(report)

if __name__ == "__main__":
    main()
