# Iteration 2 計画: デプロイアビリティ整備

## ゴール
静的PWAを任意のホスティングへ一貫してデプロイできる体制を作る。
対象: GitHub Pages(Actions) / Netlify / Cloudflare Pages / 任意静的ホスト。

## 現状の課題
- デプロイ手段が未定義（手動コピーのみ）
- `sw.js` の `VERSION` が手動更新で事故りやすい
- デプロイ前の妥当性チェックがない
- リポジトリには非公開ファイル(.aidoc/, tools/, AGENTS.md)があり、
  全体をそのまま公開すると開発物が露出する
- manifest に `"id"` がない（インストール識別子の安定性）
- sw.js が長時間キャッシュされると更新が届かない運用リスク

## 作業アイテム（直列チェックリスト）
- [ ] 1. イテレーション初期化（USERINPUT追記・_PLAN_2・本コミット）
- [ ] 2. リリースツール `tools/bump_version.py` + `tools/check_deploy.py`
- [ ] 3. `Makefile`（serve/icons/bump/check/dist/clean）＋ dist パッケージング
- [ ] 4. `.github/workflows/deploy.yml`（GitHub Pages へ dist 相当のみ公開）+ `_headers`
- [ ] 5. manifest `"id"` 追加 + 検証（check/dist/serve/curl）
- [ ] 6. README/OVERVIEW/AUDIT/REPORT 更新、プランチェック完了

## 設計方針
- 公開物は `dist/` 相当の app files のみ（index/manifest/sw/icons/_headers）
- check_deploy.py がデプロイ前ゲート（Makefile・CI両方で使用）
- bump_version.py で `rfi-vN` を機械的にインクリメント
- _headers: sw.js/index/manifest は no-cache、icons は immutable
- GH Actions: push to main → パッケージ → upload-pages-artifact → deploy-pages
