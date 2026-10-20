# AUDIT_3 作業ログ

## 調査
- `netlify` CLI 未インストール、NETLIFY_AUTH_TOKEN 環境変数なし
- `~/Library/Preferences/netlify/config.json` に netlify-cli 認証トークン残存を発見
  （liliumbookair@gmail.com / nfc_ トークン / userId 64bc...）
  → CLI インストール不要の REST API 直接デプロイ方針に決定

## 作業経過（branch -> commit -> merge）
1. `iter3/01-init`: _PLAN_3 + USERINPUT追記 [191d3bd]
2. `iter3/02-netlify-toml`: netlify.toml（command=make dist, publish=dist）[7f8c16a]
3. `iter3/03-netlify-deploy`: 実デプロイ + スクリプト化 [7067ca7]
   - `GET /user` でトークン検証 → ok
   - `POST /sites {"name":"rfi-range-grid"}` → サイト作成成功
     site_id=2311da9f-..., url=https://rfi-range-grid.netlify.app
   - `make dist` → zip → `POST /sites/{id}/deploys` (application/zip)
   - state polling: 1回目で ready
   - 検証: 全リソース200、_headers適用実測
     - sw.js: cache-control: no-cache ✓（更新発見の要）
     - index: no-cache、icons: public max-age=86400
     - セキュリティ: nosniff / referrer-policy / x-frame-options DENY
   - tools/deploy_netlify.py 作成（冪等・state.json再利用・zip in-memory）
   - `make deploy-netlify` で2回目デプロイ → ready（冪等性実証）
   - .netlify/state.json に siteId 保存（gitignore済み）

## 判断メモ
- zip deploy 方式を採用した理由: ファイルダイジェスト方式より単純で、
  _headers も zip 内で自動処理される
- netlify.toml は git 連携時の保険（今回の zip deploy では未使用だが害なし）
- state.json は gitignore: ローカル状態でありコミット対象外とした
  （netlify-cli はコミット可だが、本リポジトリでは機械生成物は除外方針）
- トークンは shell 変数経由で引き回し、平文を出力・コミットせず
