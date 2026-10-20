# Iteration 1 計画: RFIレンジグリッド PWA 化

## ゴール
`~/Downloads/poker_6max_rfi_range_grid.html`（Claudeアーティファクトの保存ページ）を
完全動作する PWA として仕上げる。広いデバイス対応（iOS Safari / Android Chrome / デスクトップ）。

## 現状分析
- 実体は末尾約50行: ポジションボタン(UTG/HJ/CO/BTN/SB) → 13×13 ハンドグリッド + オープン率/コンボ数表示
- 2500行のデザイントークンCSSは不要（`--surface-1` 等への依存のみ）
- PWA要件なし: manifest / SW / アイコン / meta類 全て欠如

## 作業アイテム（直列チェックリスト）
- [ ] 1. リポジトリ初期化（main 初回コミット: AGENTS.md + .aidoc 計画/ログ）
- [ ] 2. `index.html` クリーン再構成（自前テーマ、レスポンシブ、凡例・座標軸・セル詳細、localStorage、a11y）
- [ ] 3. `manifest.webmanifest` + アイコン生成（PNG 192/512/maskable + apple-touch-icon + SVG favicon）
- [ ] 4. `sw.js`（オフライン対応 precache + 更新通知）
- [ ] 5. ローカル検証（http.server で配信、各リソース200、SW登録、manifest妥当性）
- [ ] 6. README.md / OVERVIEW.md / AUDIT.md / REPORT.md 整備

## 設計方針
- index.html は CSS/JS インラインの単一ファイル（file:// 直開きでも動作、SWキャッシュも単純）
- テーマ: ポーカーフェルト風ダークグリーン、セル色分け=ペア/スーテッド/オフスーツ
- レンジ記法パーサ(ex)とロジックは原作を保持
- ES2017程度の素JS、色関数(color-mix等)は使わず広いブラウザ互換
- SWはキャッシュファースト、バージョン定数で更新、相対パスで GitHub Pages 等サブパスにも対応
- iOS: apple-touch-icon(180) + apple-mobile-web-app-capable + theme-color
