PY ?= python3
PORT ?= 8000

APP_FILES := index.html manifest.webmanifest sw.js
ICON_FILES := $(wildcard icons/*.png icons/*.svg)

.PHONY: serve icons bump check dist clean

## ローカルプレビュー (PORT=8000 で変更可)
serve:
	$(PY) -m http.server $(PORT)

## アイコン再生成
icons:
	$(PY) tools/make_icons.py

## sw.js のキャッシュ VERSION をインクリメント（リリース前に必須）
bump:
	$(PY) tools/bump_version.py

## デプロイ前チェック
check:
	$(PY) tools/check_deploy.py

## 公開用ファイルを dist/ に集約（dist/ をそのまま静的ホストへアップロード可能）
dist: check
	rm -rf dist
	mkdir -p dist/icons
	cp $(APP_FILES) dist/
	cp $(ICON_FILES) dist/icons/
	@if [ -f _headers ]; then cp _headers dist/; fi
	@echo "dist/ ready ($$(find dist -type f | wc -l | tr -d ' ') files)"

clean:
	rm -rf dist
