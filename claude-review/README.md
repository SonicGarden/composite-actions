# claude-review

Claude Code を使用して PR の自動コードレビューを行うアクションです。変更内容を日本語でレビューし、インラインコメント（GitHub の suggestion 付き）とまとめコメントを投稿します。`pull_request` による自動実行に加え、PR への `/review` コメントでも手動起動できます。

## 使用方法

トリガー（`on: pull_request` / `issue_comment`）と発火条件、runner・タイムアウト・権限・concurrency は呼び出し側のワークフローで定義します。

```yaml
name: Claude Code Review
on:
  pull_request:
    types: [opened, synchronize, ready_for_review]
  issue_comment:
    types: [created]
concurrency:
  # 同一 PR の再実行で多重レビューを防ぐ。
  # `/review` 以外のコメント（claude[bot] 自身のコメントを含む）は run ごとに別グループにして、
  # 実行中のレビューをキャンセルしないようにする
  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.event.issue.number }}-${{ (github.event_name == 'pull_request' || startsWith(github.event.comment.body, '/review')) && 'review' || github.run_id }}
  cancel-in-progress: true
jobs:
  claude-review:
    # pull_request で draft でない、または PR への `/review` コメント（OWNER / MEMBER / COLLABORATOR のみ）
    if: >
      (github.event_name == 'pull_request' && github.event.pull_request.draft == false) ||
      (github.event_name == 'issue_comment' &&
        github.event.issue.pull_request &&
        startsWith(github.event.comment.body, '/review') &&
        contains(fromJSON('["OWNER","MEMBER","COLLABORATOR"]'), github.event.comment.author_association))
    runs-on: ubuntu-24.04-arm
    timeout-minutes: 30
    permissions:
      contents: read
      pull-requests: write
      issues: write
      id-token: write
    steps:
      - name: Run Claude Code Review
        uses: SonicGarden/composite-actions/claude-review@main
        with:
          guideline_files: |
            doc/agent/code-review.md
            doc/agent/code-review-rails.md
          minimum_changed_lines: '10'
          # 以下どちらかが必須
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

注意事項：

- アクション内で checkout するため、呼び出し側で `actions/checkout` を前置しないでください
- `issue_comment` では PR HEAD（`refs/pull/<N>/head`）を checkout します。`issue_comment` はシークレットが使える信頼コンテキストで動くため、アクション内で次の防御をしています
  - checkout は `persist-credentials: false` で行い、トークンを `.git/config` に残さない
  - Claude Code の設定（`.claude/`・`.mcp.json`）は PR のベースブランチの内容で上書きする（ベースに無ければ削除する）
  - ガイドラインファイルは PR 側ではなくベースブランチから読む
- それでも PR のコード（`CLAUDE.md` などを含む）は Claude に読まれます。`/review` を起動できる人は呼び出し側の `if:` で制限し、fork からの PR では中身を確認してから `/review` してください（上記例では `author_association` が OWNER / MEMBER / COLLABORATOR の場合のみ）
- runner（`runs-on`）・タイムアウト（`timeout-minutes`）・権限（`permissions`）・`concurrency` は呼び出し側の job / ワークフローで指定します
- 呼び出し側で `gh actions-lock` を実行すると、アクション本体と内部で使用している actions を `actions.lock` で固定できます
- 旧 `SonicGarden/workflows` の再利用可能ワークフロー版からの変更点として、`claude_code_oauth_token` を指定した場合は `anthropic_api_key` を渡さなくなりました（旧版は OAuth トークンの有無にかかわらず API キーが渡されていました）

## 入力パラメータ

- `guideline_files` (必須): コードレビューのガイドラインファイルのパス一覧（改行区切り）
- `model` (省略可): 使用する Claude モデル（デフォルト: `sonnet`。空文字を明示指定するとアクション側のデフォルトになる）
- `minimum_changed_lines` (省略可): 前回レビューからの最小変更行数（デフォルト: `'0'`、`'0'` の場合は常に実行。文字列で渡す）
- `claude_code_oauth_token` (どちらか必須): Claude Code OAuth トークン（推奨）
- `anthropic_api_key` (どちらか必須): Anthropic API キー（`claude_code_oauth_token` がない場合のフォールバック）

## 必要な権限

- `contents: read`
- `pull-requests: write`
- `issues: write`
- `id-token: write`

## 機能

- PR の変更内容を日本語で自動レビュー
- インラインコメントによる具体的な改善提案（suggestion 機能で変更を適用可能）
- コード品質、セキュリティ、パフォーマンスなど多角的な観点からのレビュー
- 既存の Claude bot コメントを自動削除して重複を防止
- PR への `/review` コメントによる手動起動（`issue_comment` では PR HEAD を checkout）
- `minimum_changed_lines` 以下の変更量（前回レビュー以降）ではレビューをスキップ
- コミットメッセージに `[skip review]` を含む場合はスキップ（`pull_request` のみ）
