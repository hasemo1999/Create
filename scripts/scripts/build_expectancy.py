"""
build_expectancy.py
─ 取引履歴 CSV を読み込み、期待値を計算して docs/expectancy.md を上書きする
CSV 例:
 Time,Symbol,Type,Lots,Profit
 2025-07-01,USDJPY,buy,0.01,12.5
 2025-07-01,USDJPY,sell,0.01,-8.3
"""

import pandas as pd
from pathlib import Path

# 1️⃣ 取引履歴 CSV を読み込む（MTの「履歴をエクスポート」→ history.csv など）
HISTORY_CSV = Path("data/history.csv")      # ← 場所は好きに変えてOK
if not HISTORY_CSV.exists():
    raise SystemExit(f"取引履歴 {HISTORY_CSV} が見つかりません")

df = pd.read_csv(HISTORY_CSV)

# 2️⃣ 勝ち負け別に平均値を計算
wins  = df[df["Profit"] > 0]
loss  = df[df["Profit"] < 0]

win_rate      = len(wins) / len(df) if len(df) else 0
avg_profit    = wins["Profit"].mean()  if not wins.empty else 0
avg_loss_abs  = loss["Profit"].abs().mean() if not loss.empty else 0

expectancy = win_rate * avg_profit - (1 - win_rate) * avg_loss_abs

# 3️⃣ Markdown に書き出し
out = Path("docs/expectancy.md")
out.parent.mkdir(exist_ok=True)

with out.open("w", encoding="utf-8") as f:
    f.write("# 今月の期待値レポート\n\n")
    f.write(f"- 総トレード数: **{len(df)}**\n")
    f.write(f"- 勝率: **{win_rate*100:.2f}%**\n")
    f.write(f"- 平均利益 (勝ち): **{avg_profit:.2f}**\n")
    f.write(f"- 平均損失 (負け): **{avg_loss_abs:.2f}**\n")
    f.write(f"- **期待値**: **{expectancy:.2f} pips**\n")
print(f"✅ 期待値レポートを {out} に保存しました")
