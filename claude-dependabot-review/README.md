# claude-dependabot-review

Dependabot の依存更新 PR について、CI（テスト）が緑でも見逃しがちな「ランタイム挙動の変化・deprecation」を CHANGELOG ベースで Claude に評価させ、PR へ要約コメントを 1 本残すアクションです。検出/分類は Dependabot に、「壊れたか」は CI に任せ、このアクションは「緑でも危ういもの」を拾う役に徹します。言語・フレームワークには依存しません。

## 使用方法

トリガー（`on: workflow_run`）と発火条件（CI 成功 & Dependabot 起点）、runner・タイムアウト・権限は呼び出し側のワークフローで定義し、`head_sha` を渡します。

```yaml
name: Claude Dependabot Review
on:
  workflow_run:
    workflows: ["Test"]   # CI(テスト本体)のワークフロー名に合わせる
    types: [completed]
concurrency:
  # 同一 head_branch の再実行で多重コメントを防ぐ
  group: ${{ github.workflow }}-${{ github.event.workflow_run.head_branch }}
  cancel-in-progress: true
jobs:
  dependabot-review:
    # Dependabot 起点の PR、かつ CI が成功した場合のみ
    if: >
      github.event.workflow_run.event == 'pull_request' &&
      github.event.workflow_run.conclusion == 'success' &&
      github.event.workflow_run.actor.login == 'dependabot[bot]'
    runs-on: ubuntu-24.04-arm
    timeout-minutes: 20
    permissions:
      contents: read
      pull-requests: write
      id-token: write
    steps:
      - name: Run Claude Dependabot Review
        uses: SonicGarden/composite-actions/claude-dependabot-review@main
        with:
          head_sha: ${{ github.event.workflow_run.head_sha }}
          # 以下どちらかが必須
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

注意事項：

- アクション内でベースブランチを checkout するため、呼び出し側で `actions/checkout` を前置しないでください
- runner（`runs-on`）・タイムアウト（`timeout-minutes`）・権限（`permissions`）は呼び出し側の job で指定します
- 呼び出し側で `gh actions-lock` を実行すると、アクション本体と内部で使用している actions を `actions.lock` で固定できます

## 入力パラメータ

- `head_sha` (必須): レビュー対象 PR の HEAD コミット SHA（呼び出し側で `github.event.workflow_run.head_sha` を渡す）
- `model` (省略可): 使用する Claude モデル（デフォルト: `sonnet`。空文字を明示指定するとアクション側のデフォルトになる）
- `claude_code_oauth_token` (どちらか必須): Claude Code OAuth トークン（推奨）
- `anthropic_api_key` (どちらか必須): Anthropic API キー（`claude_code_oauth_token` がない場合のフォールバック）

## 必要な権限

- `contents: read`
- `pull-requests: write`
- `id-token: write`

## 前提

- 呼び出し側の `workflows: ["Test"]` を、待ち受けたい CI ワークフローの `name` に合わせること
- Dependabot が PR 本文に Release notes / Changelog を展開していること（一次ソースとして読む）

## 機能

- CI（テスト）が緑でも見逃す「ランタイム挙動の変化・deprecation」を CHANGELOG ベースで評価
- ベースブランチ（更新適用前の現状コード）のみを checkout し、信頼コンテキストに untrusted な PR HEAD を置かない
- PR へのコメントは 1 本に集約（既存の Claude コメントを自動削除して重複を防止）
- `head_sha` に紐づく open PR が見つからない場合はスキップ
