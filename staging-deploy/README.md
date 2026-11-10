# staging-deploy

指定ブランチ（デフォルト `release-candidate`）から staging 等のブランチ（デフォルト `staging`）への自動デプロイ PR を作成・更新し、CI 通過後に自動マージさせる composite action です。既存の PR があれば新規作成せず本文を最新のコミット情報で更新します。

## 使用方法

```yaml
name: Staging Deploy

on:
  push:
    branches:
      - release-candidate

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions: {}

jobs:
  create-staging-pr:
    runs-on: ubuntu-slim
    # [skip deploy] がコミットメッセージに含まれていればスキップ
    if: contains(github.event.head_commit.message, '[skip deploy]') == false
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: SonicGarden/composite-actions/staging-deploy@main
        with:
          source_branch: release-candidate  # 省略可
          target_branch: staging            # 省略可
          enable_auto_merge: 'true'         # 省略可
```

注意事項：

- `on.push.branches` は `source_branch` と一致させてください
- `actions/checkout` を前置する必要はありません（gh CLI のみ使用します）
- `enable_auto_merge` は文字列の `'true'` / `'false'` で渡します

## 入力パラメータ

- `source_branch`: デプロイ元のブランチ名（デフォルト: `release-candidate`）
- `target_branch`: デプロイ先のブランチ名（デフォルト: `staging`）
- `enable_auto_merge`: CI通過後にPRを自動マージするか（デフォルト: `'true'`）。`'false'` にするとPRの作成・更新のみ行い、自動マージは設定しません

## 出力パラメータ

なし

## 必要な権限

- `contents: write`
- `pull-requests: write`

## 自動マージに必要な GitHub 設定

> **Note:** 以下の設定は `enable_auto_merge: 'true'`（デフォルト）で自動マージを利用する場合に必要です。`'false'` の場合は不要です。

PR が自動的にマージされるようにするには、リポジトリで以下の設定が必要です。

1. **ブランチ保護ルールの設定:**
   - リポジトリの Settings > Branches に移動
   - staging ブランチのブランチ保護ルールを追加
   - 「Require status checks to pass before merging」をチェック
   - 必要なCIチェック（例：テスト、linter など）を選択

2. **自動マージ機能の有効化:**
   - リポジトリの Settings > General に移動
   - 「Allow auto-merge」をチェック

これらの設定により、CIが全て通過した後に自動的にPRがマージされます。

## SonicGarden/workflows の staging_deploy.yml からの移行

主な変更点：

- `uses:` を job レベルから step レベルに移します
- `runs_on` は廃止しました。呼び出し側 job の `runs-on` で指定してください
- `[skip deploy]` の判定（job の `if:`）、`concurrency`、`permissions` は呼び出し側に書きます
- notify-deployment ジョブは廃止しました（ジョブの失敗で判別できるため）
- `enable_auto_merge` は boolean ではなく文字列（`'true'` / `'false'`）で渡します
