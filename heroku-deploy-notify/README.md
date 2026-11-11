# heroku-deploy-notify

Heroku-GitHub 自動デプロイ対象ブランチへの push を契機に、Heroku Platform API をポーリングしてリリースの完了/失敗を検知し、そのマージコミットに紐づく PR にデプロイ結果をコメントする composite action です。デプロイ本体には介入しない外形監視です（Rails / release phase / Procfile は変更しません）。

## 使用方法

ブランチごとに job を分け、`heroku_app_name` / `env_name` を渡します。`push` トリガーと `concurrency` は呼び出し側で定義します。

```yaml
name: Deploy Notify

on:
  push:
    branches: [staging, main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions: {}

jobs:
  notify-production:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-slim
    timeout-minutes: 15
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: SonicGarden/composite-actions/heroku-deploy-notify@main
        with:
          heroku_app_name: my-app
          env_name: production
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}

  notify-staging:
    if: github.ref == 'refs/heads/staging'
    runs-on: ubuntu-slim
    timeout-minutes: 15
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: SonicGarden/composite-actions/heroku-deploy-notify@main
        with:
          heroku_app_name: my-app-staging
          env_name: staging
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
```

注意事項：

- `actions/checkout` を前置する必要はありません（gh / curl のみ使用します）
- `poll_interval_seconds × poll_max_attempts` に起動などの時間を足した値が `timeout-minutes` 内に収まるようにしてください（ubuntu-slim は 15 分で打ち切られます）
- `notify_on_*` / `include_release_log` は文字列の `'true'` / `'false'` で渡します
- `heroku_app_name` / `env_name` / `heroku_api_key` は必須です。composite action では必須入力が強制されないため、空の場合は最初のステップでエラー終了します

## 入力パラメータ

- `heroku_app_name`: Heroku アプリ名（必須）
- `env_name`: PR コメントに表示する環境名（必須、例: `production` / `staging`）
- `heroku_api_key`: read-protected スコープの Heroku API トークン（必須。read スコープだと releases の取得が 403 になります）
- `poll_interval_seconds`: ポーリング間隔（秒）（デフォルト: `'15'`）
- `poll_max_attempts`: 最大試行回数（デフォルト: `'48'`）。`poll_interval_seconds × この値` が監視時間です。ランナーの 15 分上限内に収めてください
- `release_fetch_count`: 取得する最新 release 件数（デフォルト: `'20'`）
- `notify_on_success`: 成功通知の ON/OFF（デフォルト: `'true'`）
- `notify_on_failure`: 失敗通知の ON/OFF（デフォルト: `'true'`）
- `notify_on_timeout`: release を検知できずタイムアウトした場合の通知 ON/OFF（デフォルト: `'true'`）
- `include_release_log`: PR コメントに Heroku release phase ログ（折りたたみ）を添付する ON/OFF（デフォルト: `'true'`）

## 出力パラメータ

なし

## 必要な権限

- `contents: read`
- `pull-requests: write`（マージされた PR へのコメントに必要）

## 前提

- 対象リポジトリで Heroku-GitHub の自動デプロイが有効であること
- Heroku release の `description` が `Deploy <短縮SHA>` 形式であること（コミット SHA 先頭 7 文字で照合します）

## 機能

- Heroku release を最大 `poll_max_attempts` 回ポーリングして完了/失敗を検知
- マージコミットに紐づく PR にデプロイ結果（成功/失敗/タイムアウト）をコメント
- PR コメントは `push` イベント時のみ（手動実行などでは誤爆防止でスキップ）

## SonicGarden/workflows の heroku_deploy_notify.yml からの移行

主な変更点：

- `uses:` を job レベルから step レベルに移します
- `runs-on` / `timeout-minutes` / `permissions` は呼び出し側 job に書いてください
- `secrets:` の `heroku_api_key` は `with:` の `heroku_api_key` で渡します
- ON/OFF の input は元から文字列だったため、書き方は変わりません（`'true'` / `'false'`）
