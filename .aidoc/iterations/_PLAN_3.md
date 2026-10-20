# Iteration 3 計画: Netlify への実デプロイ

## ゴール
Netlify に dist 相当を実デプロイし、公開URLを取得・検証する。

## 調査結果
- `netlify` CLI: 未インストール
- 認証: `~/Library/Preferences/netlify/config.json` に CLI 用トークン残存
  （userId 64bc... / liliumbookair@gmail.com / nfc_ トークン）→ REST API で利用可能
- アプローチ: CLI インストール不要の Netlify REST API（zip deploy）で実行

## 作業アイテム（直列チェックリスト）
- [ ] 1. イテレーション初期化（USERINPUT追記・_PLAN_3）
- [ ] 2. `netlify.toml` 追加（git連携デプロイにも対応できるよう command/publish 定義）
- [ ] 3. APIデプロイ実施: トークン検証 → サイト作成 → `make dist` → zip deploy
- [ ] 4. 公開検証: 全リソース200・`_headers` 適用（Cache-Control実測）・manifest内容
- [ ] 5. docs更新（README Netlify節に実URL・AUDIT_3・REPORT_3・OVERVIEW）＋ push

## 設計方針
- サイト名候補: `rfi-range-grid`（衝突時は代替名）
- zip deploy: `POST /api/v1/sites/{id}/deploys` に dist をzipして送信
- `_headers` は zip 内に同梱済み → Netlify が自動適用
- トークンはシェル変数経由で読み出し、会話・ログに平文出力しない
