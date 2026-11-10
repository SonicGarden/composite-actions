# claude-code

Claude CodeをGitHub Actionsで実行するアクションです。GitHubのイシューやプルリクエストのコメントから自動的にコード作成・修正を行います。プロジェクト固有のセットアップが必要な場合は自動的に検出し、環境構築を行った上でClaude Codeを実行します。

## 使用方法

```yaml
- name: Run Claude Code
  uses: SonicGarden/composite-actions/claude-code@main
  with:
    claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

カスタム設定を追加する場合：

```yaml
- name: Run Claude Code with custom settings
  uses: SonicGarden/composite-actions/claude-code@main
  with:
    claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
    additional_claude_args: "--model claude-3-opus-20240229"
    additional_system_prompt: |
      プロジェクト固有の追加指示をここに記載
```

## 入力パラメータ

- `claude_code_oauth_token` (必須): Claude Code OAuth トークン
- `additional_claude_args` (省略可): Claude Codeへの追加引数（モデル指定、ツール設定など）
- `additional_system_prompt` (省略可): 追加のシステムプロンプト（デフォルトでは日本語出力を指定）

## 出力パラメータ

- `execution_file`: Claude実行ファイルのパス

## 機能

- **自動セットアップ検出**: `-setup`フラグやコード修正が必要な場合を自動判定
- **プロジェクト固有セットアップ**: `.github/actions/project-setup`が存在する場合、自動的に実行
- **ベースブランチ指定**: コメントに`--base=branch_name`を含めることで、特定のブランチを基準に作業
- **モデル切り替え**: コメントに`-opus`を含めることで、Claude Opus モデルを使用
- **日本語対応**: デフォルトですべての出力が日本語に設定
- **MCP統合**: deepwikiとcontext7のMCPサーバーが利用可能
- **処理中リアクション**: 自動的に処理開始時に👀リアクションを追加

## 対応イベント

- イシューコメント
- プルリクエストコメント
- イシューの作成
- プルリクエストレビュー

## 必要な権限

- `contents: write`
- `issues: write`
- `pull-requests: write`
- `actions: read`
