# REPORT_3 イテレーション報告書

## 概要
Netlify への実デプロイを REST API で実行し、公開・検証・再現性確保まで完了。

## 成果
- **公開URL**: https://rfi-range-grid.netlify.app （稼働中・全リソース200）
- サイト: `rfi-range-grid`（アカウント liliumbookair@gmail.com 配下に作成）
- `_headers` 適用実測:
  - `sw.js`: `cache-control: no-cache`（更新発見の要）✓
  - `/`: no-cache、icons: `public, max-age=86400` ✓
  - `x-content-type-options: nosniff` / `referrer-policy` / `x-frame-options: DENY` ✓
- `netlify.toml`: git 連携デプロイ用設定（command=make dist, publish=dist）
- `tools/deploy_netlify.py`: CLI 不要の冪等デプロイスクリプト
  （トークン自動解決・サイト再利用・in-memory zip・ready ポーリング）
- `make deploy-netlify`: check→dist→deploy の一発コマンド（2回実行済み・冪等）

## 検証結果
- デプロイ1回目（curl直叩き）: state=ready
- デプロイ2回目（make deploy-netlify経由）: ready — 再現性確認
- タイトル/manifest/各リソース実測で本物の配信を確認

## 運用メモ
- 2系統の公開URLが並存:
  - GitHub Pages: https://ririumu.github.io/poker_6max_rfi_range_grid/（pushで自動）
  - Netlify: https://rfi-range-grid.netlify.app（`make deploy-netlify` で手動 or git連携で自動化可能）
- Netlify側を自動化したい場合は Netlify UI でリポジトリ連携するだけ（netlify.toml済み）
- トークンはローカル configstore 由来。CI化する場合は NETLIFY_AUTH_TOKEN シークレット化
