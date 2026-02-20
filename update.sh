#!/bin/bash
# ─────────────────────────────────────────────────────────────
# Nikos Cafe — Daily Data Update Script
# Run after adding new sales/inventory data to your Excel files
# Usage: ./update.sh
# ─────────────────────────────────────────────────────────────

set -e  # stop on any error

echo ""
echo "🥙 Nikos Cafe — Data Update"
echo "─────────────────────────────"

echo "📂 Copying latest Excel files into data/ ..."

cp "/Users/mayurpatil/Downloads/NIKOS_2026/Sales_data/Combined_reports/combined_sales_data.xlsx" \
   "$(dirname "$0")/data/combined_sales_data.xlsx"

cp "/Users/mayurpatil/Downloads/NIKOS_2026/order_data/COMBINED_Master_Analysis.xlsx" \
   "$(dirname "$0")/data/COMBINED_Master_Analysis.xlsx"

echo "✅ Files copied."
echo ""
echo "📤 Pushing to GitHub..."

cd "$(dirname "$0")"
git add data/
git diff --cached --quiet && echo "⚠️  No data changes to commit — files unchanged." && exit 0
git commit -m "data: update $(date '+%Y-%m-%d')"
git push

echo ""
echo "✅ Done! Streamlit Cloud will redeploy in ~60 seconds."
echo "🔗 Reload the app URL to see fresh data."
echo ""
