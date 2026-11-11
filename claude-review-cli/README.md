# claude-review-cli

`@aki77/claude-code-review` CLI を `npx` で実行して PR の自動コードレビューを行うアクションです。GitHub MCP ツールを直接呼び出す `claude-review` とは異なり、CLI が gh CLI 経由で diff を取得してレビューし、コメントを投稿します。`pull_request` による自動実行に加え、PR への `/review` コメントでも再実行できます。

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
  # NOTE: PR更新時のレビューと/reviewコメントは同じgroupで同時実行を防ぐ (例: workflow--pr-123)
  # NOTE: 単なるコメントでもアクション自体は発動してしまうので、/review以外のコメントは個別groupで無関係なキャンセルを防ぐ (例: workflow--comment-456)
  group: |
    ${{
      github.event_name == 'pull_request' && format('{0}--pr-{1}', github.workflow, github.event.pull_request.number) ||
      startsWith(github.event.comment.body, '/review') && format('{0}--pr-{1}', github.workflow, github.event.issue.number) ||
      format('{0}--comment-{1}', github.workflow, github.event.comment.id)
    }}
  cancel-in-progress: true

jobs:
  claude-review:
    # PR への `/review` コメント（OWNER / MEMBER / COLLABORATOR のみ）、または
    # pull_request で Dependabot・draft・`[skip review]`・レビュー済みラベル付きのものを除く
    if: >
      (github.event_name == 'issue_comment' &&
        github.event.issue.pull_request &&
        startsWith(github.event.comment.body, '/review') &&
        contains(fromJSON('["OWNER","MEMBER","COLLABORATOR"]'), github.event.comment.author_association)) ||
      (github.event_name == 'pull_request' &&
        github.actor != 'dependabot[bot]' &&
        !github.event.pull_request.draft &&
        !contains(github.event.pull_request.title, '[skip review]') &&
        !contains(join(github.event.pull_request.labels.*.name, ','), 'reviewed-by-claude'))
    runs-on: ubuntu-24.04-arm
    timeout-minutes: 30
    permissions:
      contents: read
      pull-requests: write
      issues: write
      checks: read
    steps:
      - name: Run Claude Code Review
        uses: SonicGarden/composite-actions/claude-review-cli@main
        with:
          # 以下どちらかが必須
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

注意事項：

- アクション内で checkout するため、呼び出し側で `actions/checkout` を前置しないでください
- checkout は PR の head SHA を `persist-credentials: false` で行い、トークンを `.git/config` に残しません（`issue_comment` はシークレットが使える信頼コンテキストで動くため）
- PR のコードと `CLAUDE.md`・`.claude/review.yaml` は CLI に読まれます。また CLI は PR の作業ツリーで `npx` を実行するため、`.npmrc` なども PR 側のものが使われます。`/review` を起動できる人は呼び出し側の `if:` で制限し、fork からの PR では中身を確認してから `/review` してください（上記例では `author_association` が OWNER / MEMBER / COLLABORATOR の場合のみ）
- リポジトリ固有の除外条件（特定ブランチ間の PR を除外するなど）が必要な場合は、呼び出し側 job の `if:` に条件を追加してください
- runner（`runs-on`）・タイムアウト（`timeout-minutes`）・権限（`permissions`）・`concurrency` は呼び出し側の job / ワークフローで指定します
- 呼び出し側で `gh actions-lock` を実行すると、アクション本体と内部で使用している actions を `actions.lock` で固定できます

## 入力パラメータ

- `claude_code_oauth_token` (どちらか必須): Claude Code OAuth トークン（推奨）
- `anthropic_api_key` (どちらか必須): Anthropic API キー（`claude_code_oauth_token` がない場合のフォールバック）

## 必要な権限

- `contents: read`
- `pull-requests: write`
- `issues: write`
- `checks: read`

## 機能

- `@aki77/claude-code-review` CLI による自動レビュー（インラインコメント）
- PR コメントで `/review` と投稿すると再レビューを実行
- `reviewed-by-claude` ラベルを自動作成・付与し、二重レビューを防止
- 既存の Claude bot コメントを自動削除して重複を防止
- ドラフト PR、`[skip review]` を含むタイトル、Dependabot 起点の PR は自動的にスキップ（Dependabot 更新 PR は `claude-dependabot-review` を利用）

## SonicGarden/workflows の claude-review-cli.yml からの移行

主な変更点：

- `uses:` を job レベルから step レベルに移します
- `runs_on` は廃止しました。呼び出し側 job の `runs-on` で指定してください
- `secrets:` は `with:` に変わります。`claude_oauth_token` は `claude_code_oauth_token` に改名しました。`anthropic_api_key` も `with:` で渡します
- job の `if:`（Dependabot・draft・`[skip review]`・`reviewed-by-claude` ラベルの除外、`/review` コメントの判定）、`timeout-minutes`、`permissions`、`concurrency` は呼び出し側に書きます
- `/review` コメントで起動できる人を OWNER / MEMBER / COLLABORATOR に限定し、コメント本文の先頭が `/review` のときだけ起動するようにしました（旧版は誰の、本文のどこにあっても起動）
- `claude_code_oauth_token` を指定した場合は `anthropic_api_key` を渡さなくなりました（旧版は OAuth トークンの有無にかかわらず API キーが渡されていました）
- checkout は PR の head SHA を `persist-credentials: false` で行います。ベースブランチの明示的な fetch は不要になったため廃止しました
