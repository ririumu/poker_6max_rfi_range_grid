# AUDIT_1 作業ログ

## 調査
- `~/Downloads/poker_6max_rfi_range_grid.html` を解析
  - 2580行中、先頭〜2533行は Claude.ai 保存ページのデザイントークンCSS（不要）
  - 実体は 2533-2580行: ポジションボタン + 統計 + 13×13 グリッド + レンジ記法パーサ
  - 依存していたCSS変数(--surface-1等)は破棄し自前テーマに置換
- 環境: python3.14 / node v26 / sips 利用可能、gitユーザー設定済み(ririumu)

## 作業経過（branch -> commit -> merge）
1. `main` 初回コミット: AGENTS.md, .gitignore, .aidoc 一式 [5c66544]
2. `iter1/02-index-html`: index.html 再構成 → merge [aa48bab]
   - 単一ファイル化、フェルト緑ダークテーマ
   - 軸ラベル・凡例・セル詳細・キーボード操作・localStorage・SW更新トースト追加
   - 原作の P/N データ・パーサ ex()・cb() を保持
3. `iter1/03-manifest-icons`: manifest + アイコン生成 → merge [fda76a1]
   - tools/make_icons.py: 標準ライブラリのみで PNG 出力（2xレンダ→ダウンサンプルAA）
   - アイコンはBTNレンジの13×13グリッドモチーフ（見た目確認済み）
   - favicon.svg も同一モチーフで生成
   - ※ __pycache__ が誤って混入 → 次ブランチで除去・gitignore化
4. `iter1/04-service-worker`: sw.js → merge [2d81c1b]
   - ES5スタイルのPromise記述（広いブラウザ互換）
   - プリキャッシュ + キャッシュファースト + ナビゲーションフォールバック
   - message "skipWaiting" → 更新トースト連携
5. `iter1/05-verify`: 検証 → merge [9877c84]
   - manifest JSON妥当性OK、sw.js/inline script 構文OK
   - レンジ計算: UTG 17.9% / HJ 21.3% / CO 27.9% / BTN 43.9% / SB 35.1% — 妥当
   - http.serverで全9リソース 200 確認
   - getElementById参照・iconパス整合性OK
   - 修正: .ax.row の aspect-ratio による行ラベル縦ずれを解消
6. `iter1/06-docs`: README / OVERVIEW / AUDIT / REPORT（本ブランチ）

## 判断メモ
- SW は「更新トースト→ユーザー承認→skipWaiting→controllerchange reload」方式。
  初回インストール時は controller 非存在のため自動リロードなし（ループ回避）。
- アイコンはフォント不要・テーマ性重視で「アプリそのままのグリッド」を採用。
- apple-touch-icon は非透過・全面描画の180px PNG。
- start_url/scope は "./" 相対指定 → GitHub Pages等サブパス配信に対応。
