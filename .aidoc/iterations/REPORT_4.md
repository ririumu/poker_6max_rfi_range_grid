# REPORT_4 イテレーション報告書

## 概要
Netlify デプロイの独立マニュアル `docs/DEPLOY_NETLIFY.md` を作成し、
README からリンク。併せて deploy スクリプトを Linux 互換に拡張。

## 成果
- **docs/DEPLOY_NETLIFY.md**: 前提条件・認証2系統、デプロイ4方法
  （make deploy-netlify / netlify CLI / GitHub連携 / Netlify Drop）、
  curl による検証手順、運用（bump・state.json・独自ドメイン・ロールバック）、
  トラブルシューティング表、現状サマリ
- **README**: マニュアルへの導線リンク＋ファイル構成追記
- **tools/deploy_netlify.py**: configstore パス3候補対応（macOS/Linux）
- 検証: 改修後の `make deploy-netlify` 実実行で ready（3度目の成功）

## 残課題・運用メモ
- Netlify git連携を有効化すれば push→自動デプロイ化（UI操作が必要）
- CI環境での Netlify デプロイには NETLIFY_AUTH_TOKEN をシークレット登録
