# REPORT_2 イテレーション報告書

## 概要
静的PWAのデプロイアビリティを整備。主要ホスティングへの一貫した
デプロイ経路、自動チェックゲート、バージョン管理を確立した。

## 成果
- **tools/bump_version.py**: sw.js VERSION の機械的インクリメント（--set 可）
- **tools/check_deploy.py**: デプロイ前ゲート — 必須ファイル、manifest妥当性、
  icon PNG検証、SWプリキャッシュ実在、ルート絶対パス検出。stdlib のみ
- **Makefile**: serve/icons/bump/check/dist/clean。
  `make dist` は check 通過後に公開ファイルのみを dist/ へ集約
- **.github/workflows/deploy.yml**: main push → `make dist` →
  upload-pages-artifact → deploy-pages。公開物はアプリのみで開発物を露出しない
- **_headers**: Netlify/CF Pages 用。sw.js・index・manifest は no-cache、
  icons は1日、セキュリティヘッダ付与
- **manifest "id"**: "./" を追加しインストール識別子を安定化（警告解消）
- **README**: GitHub Pages / Netlify・CF Pages / 汎用手順とリリース手順を記載

## 検証結果
- check_deploy: 全項目pass・警告ゼロ
- make dist: 9ファイル（app一式 + _headers）生成、dist配信で全て200
- deploy.yml: YAML妥当（jobs=[deploy]）
- bump_version: rfi-v1→v2→--set復元 まで動作確認

## デプロイ結果
- **公開URL**: https://ririumu.github.io/poker_6max_rfi_range_grid/ （稼働確認済み・全リソース200）
- リポジトリ: public 化（private は Pages 非対応プランのため）
- CI: push 由来の初回 run は Pages 未設定で failure → 設定後の dispatch run で success
- 以後 main への push で自動デプロイ

## 残課題・運用メモ
- ~~GitHub Pages側の設定~~ → APIで有効化済み（build_type=workflow）
- アプリ変更時は `make bump` を忘れずに（CIでも差分検知はしていない）
- iOSスプラッシュ画像・レンジ編集機能は将来イテレーション候補
- 独自ドメイン/cname 設定は未対応（必要なら `cname` を Pages APIで追加）
