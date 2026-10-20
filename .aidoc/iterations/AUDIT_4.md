# AUDIT_4 作業ログ

## 作業経過（branch -> commit -> merge）
1. `iter4/01-docs-manual`: `docs/DEPLOY_NETLIFY.md` 新規作成
   - 構成: 前提条件/認証2系統 → デプロイ4方法 → 検証 → 運用 → トラブルシュート
   - 内容は iter3 の実績（REST API zip deploy・実サイト情報・_headers実測値）に基づく
   - README にマニュアルへのリンク＋ファイル構成へ追記
   - 併せて deploy_netlify.py の configstore パスを Linux 対応で拡張
     （~/.config/netlify/config.json, ~/.config/configstore/netlify-cli.json）
   - 改修後に `make deploy-netlify` 実実行 → ready（3回目・冪等再確認）

## 判断メモ
- マニュアルは docs/ 配下に配置（.aidoc/ は開発記録、docs/ は利用者向け）
- デプロイ方法を4系統記載したが「方法A: make deploy-netlify」を標準と明記
- 実測値（URL・サイト名・デプロイ回数・ヘッダ実値）を含めて即参照可能に
