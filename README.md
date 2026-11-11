# composite-actions

GitHub Actionsで使用するComposite Actionsのコレクション

## Available Actions

- [add-processing-reaction](add-processing-reaction/README.md) - GitHubイベントに処理中のリアクションを追加
- [check-claude-setup-needed](check-claude-setup-needed/README.md) - Claude Codeを使用してセットアップが必要かどうかを判定
- [claude-code](claude-code/README.md) - Claude CodeをGitHub Actionsで実行し、自動的にコード作成・修正を行う
- [claude-dependabot-review](claude-dependabot-review/README.md) - Dependabot更新PRをCI緑でも危うい観点でClaudeレビュー
- [claude-review](claude-review/README.md) - Claude CodeによるPRの自動コードレビュー（インラインコメント・suggestion）
- [claude-review-cli](claude-review-cli/README.md) - @aki77/claude-code-review CLI で PR を自動コードレビュー
- [extract-event-text](extract-event-text/README.md) - GitHubイベントタイプに応じてテキストを抽出
- [get-user-secret-key](get-user-secret-key/README.md) - ユーザー名を取得し、Secretキーを動的に検索
- [heroku-deploy-notify](heroku-deploy-notify/README.md) - Heroku デプロイの完了/失敗を検知して PR にコメント
- [license-finder](license-finder/README.md) - ライセンスチェックと承認済みライセンスの管理
- [pr-review-guide](pr-review-guide/README.md) - PR ごとの初見レビュアー向け解説ページを Claude で生成し PR 本文へ追記（generate / publish）
- [staging-deploy](staging-deploy/README.md) - staging 等への自動デプロイ PR を作成・更新し自動マージを設定
- [update-ruby-version](update-ruby-version/README.md) - .ruby-version を最新の安定版 Ruby に更新する PR を作成してマージ（check / merge）
