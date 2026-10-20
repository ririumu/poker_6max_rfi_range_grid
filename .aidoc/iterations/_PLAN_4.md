# Iteration 4 計画: Netlify デプロイマニュアル作成

## ゴール
Netlify へのデプロイ手順を `docs/` に独立マニュアルとして整備する。

## 作業アイテム（直列チェックリスト）
- [x] 1. イテレーション初期化（USERINPUT追記・_PLAN_4）+ `docs/DEPLOY_NETLIFY.md` 作成
- [x] 2. README にマニュアルへのリンク追加・OVERVIEW/AUDIT_4/REPORT_4 更新 + push

## マニュアルに含める内容
- 前提条件（アカウント・認証トークンの入手方法）
- 方法A: `make deploy-netlify`（REST API・CLI不要・本プロジェクト標準）
- 方法B: netlify CLI 経由
- 方法C: GitHub 連携（netlify.toml 利用・自動デプロイ）
- 方法D: Netlify Drop（手動ドラッグ&ドロップ）
- デプロイ後検証手順（リソース・_headers・PWA）
- 運用（サイトID/state.json・再デプロイ・bump運用・独自ドメイン）
- トラブルシューティング
