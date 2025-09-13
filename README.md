# composite-actions

GitHub Actionsで使用するComposite Actionsのコレクション

## Available Actions

- [add-processing-reaction](#add-processing-reaction) - GitHubイベントに処理中のリアクションを追加
- [check-claude-setup-needed](#check-claude-setup-needed) - Claude Codeを使用してセットアップが必要かどうかを判定
- [claude-code](#claude-code) - Claude CodeをGitHub Actionsで実行し、自動的にコード作成・修正を行う
- [extract-event-text](#extract-event-text) - GitHubイベントタイプに応じてテキストを抽出
- [get-user-secret-key](#get-user-secret-key) - ユーザー名を取得し、Secretキーを動的に検索
- [license-finder](#license-finder) - ライセンスチェックと承認済みライセンスの管理

## Actions

### add-processing-reaction

GitHubイベント（イシュー、プルリクエスト、コメントなど）に応じて処理中のリアクション（👀）を自動的に追加するアクションです。

#### 対応イベント

- `issue_comment` - イシューコメント
- `pull_request_review_comment` - プルリクエストレビューコメント
- `issues` - イシュー
- `pull_request_review` - プルリクエストレビュー

#### 使用方法

```yaml
- name: Add processing reaction
  uses: SonicGarden/composite-actions/add-processing-reaction@main
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

#### 必要な権限

- `contents: read`
- `issues: write`
- `pull-requests: write`

### check-claude-setup-needed

Claude Codeを使用してセットアップが必要かどうかを判定するアクションです。イベントテキストを分析して、コード修正やテスト実行などの作業が必要かどうかを自動判定します。event_textパラメータが未指定の場合は、GitHubイベントから自動的にテキストを抽出します。

#### 使用方法

```yaml
# event_textを明示的に指定する場合
- name: Check Claude setup needed
  uses: SonicGarden/composite-actions/check-claude-setup-needed@main
  with:
    claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
    event_text: ${{ steps.extract-event-text.outputs.text }}

# event_textを自動抽出する場合（簡単な使用方法）
- name: Check Claude setup needed
  uses: SonicGarden/composite-actions/check-claude-setup-needed@main
  with:
    claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

#### 入力パラメータ

- `claude_code_oauth_token` (必須): Claude Code OAuth トークン
- `event_text` (任意): 分析対象のイベントテキスト（未指定の場合は自動で抽出）

#### 出力パラメータ

- `needs_setup`: セットアップが必要かどうか（true/false）

#### 判定条件

以下のいずれかを含む場合に「セットアップが必要」と判定されます：
- コードの修正・追加
- テストの実行
- データベース操作
- ビルドの実行
- 依存関係のインストール

### claude-code

Claude CodeをGitHub Actionsで実行するアクションです。GitHubのイシューやプルリクエストのコメントから自動的にコード作成・修正を行います。プロジェクト固有のセットアップが必要な場合は自動的に検出し、環境構築を行った上でClaude Codeを実行します。

#### 使用方法

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

#### 入力パラメータ

- `claude_code_oauth_token` (必須): Claude Code OAuth トークン
- `additional_claude_args` (省略可): Claude Codeへの追加引数（モデル指定、ツール設定など）
- `additional_system_prompt` (省略可): 追加のシステムプロンプト（デフォルトでは日本語出力を指定）

#### 出力パラメータ

- `execution_file`: Claude実行ファイルのパス

#### 機能

- **自動セットアップ検出**: `-setup`フラグやコード修正が必要な場合を自動判定
- **プロジェクト固有セットアップ**: `.github/actions/project-setup`が存在する場合、自動的に実行
- **ベースブランチ指定**: コメントに`--base=branch_name`を含めることで、特定のブランチを基準に作業
- **モデル切り替え**: コメントに`-opus`を含めることで、Claude Opus モデルを使用
- **日本語対応**: デフォルトですべての出力が日本語に設定
- **MCP統合**: deepwikiとcontext7のMCPサーバーが利用可能
- **処理中リアクション**: 自動的に処理開始時に👀リアクションを追加

#### 対応イベント

- イシューコメント
- プルリクエストコメント
- イシューの作成
- プルリクエストレビュー

#### 必要な権限

- `contents: write`
- `issues: write`
- `pull-requests: write`
- `actions: read`

### extract-event-text

GitHubイベントタイプに応じてテキストを抽出するアクションです。さまざまなイベントタイプから適切なテキストを自動的に抽出します。

#### 対応イベント

- `issue_comment` - イシューコメント（comment.body）
- `pull_request_review_comment` - プルリクエストレビューコメント（comment.body）
- `pull_request_review` - プルリクエストレビュー（review.body）
- `issues` - イシュー（issue.bodyまたはissue.title）

#### 使用方法

```yaml
- name: Extract event text
  id: extract-event-text
  uses: SonicGarden/composite-actions/extract-event-text@main
```

#### 入力パラメータ

なし（GitHub contextから自動的に取得）

#### 出力パラメータ

- `text`: 抽出されたイベントテキスト（JSONエスケープ済み）

### get-user-secret-key

ユーザー名を取得し、指定されたキーリストから前方一致でSecretキーを検索するアクションです。GitHub Actionsでユーザー固有のSecretキーを動的に取得する際に使用します。

#### 使用方法

```yaml
- name: Get user secret key
  id: get-secret-key
  uses: SonicGarden/composite-actions/get-user-secret-key@main
  with:
    username: ${{ github.actor }}
    available_keys: "JOHN_CLAUDE_CODE_OAUTH_TOKEN,JANE_CLAUDE_CODE_OAUTH_TOKEN,ADMIN_CLAUDE_CODE_OAUTH_TOKEN"
```

または、usernameを省略してgithub.actorから自動取得：

```yaml
- name: Get user secret key
  id: get-secret-key
  uses: SonicGarden/composite-actions/get-user-secret-key@main
  with:
    available_keys: "JOHN_CLAUDE_CODE_OAUTH_TOKEN,JANE_CLAUDE_CODE_OAUTH_TOKEN,ADMIN_CLAUDE_CODE_OAUTH_TOKEN"
```

#### 入力パラメータ

- `username` (省略可): 対象のユーザー名（省略時はgithub.actorから自動取得）
- `available_keys` (必須): カンマ区切りの有効なSecretキーリスト

#### 出力パラメータ

- `exists`: キーが存在するかどうか（true/false）
- `secret_key`: 見つかったSecretキー
- `username`: 使用されたユーザー名

### license-finder

プロジェクトの依存関係のライセンスをチェックし、承認されていないライセンスを検出するアクションです。商用利用可能な安全なライセンスがデフォルトで設定されており、レポートをGitHub Actions Summaryに出力します。

#### 使用方法

```yaml
# 基本的な使用方法
- name: Check licenses
  uses: SonicGarden/composite-actions/license-finder@main

# 追加のライセンスを許可する場合
- name: Check licenses with additional permitted licenses
  uses: SonicGarden/composite-actions/license-finder@main
  with:
    additional-licenses: "Custom-License-1.0,Internal-License"

# 特定の依存関係を無視する場合
- name: Check licenses with ignored dependencies
  uses: SonicGarden/composite-actions/license-finder@main
  with:
    ignored-dependencies: "problematic-gem,legacy-package"

# 追加ライセンスと無視する依存関係の両方を指定する場合
- name: Check licenses with custom configuration
  uses: SonicGarden/composite-actions/license-finder@main
  with:
    additional-licenses: "Custom-License-1.0"
    ignored-dependencies: "internal-tool,dev-only-package"
```

#### 入力パラメータ

- `additional-licenses` (省略可): 追加で許可するライセンス（カンマ区切り）
- `ignored-dependencies` (省略可): ライセンスチェックから除外する依存関係（カンマ区切り）

#### デフォルトで許可されているライセンス

商用利用可能な主要なオープンソースライセンス（MIT、Apache-2.0、BSDファミリーなど）がデフォルトで許可されています。Ruby、Pythonなどの言語固有のライセンスや、フォント用ライセンス（OFL-1.1）も含まれています。

#### 機能

- 未承認ライセンスの検出
- GitHub Actions Summaryへのマークダウン形式でのレポート出力
- 追加ライセンスの動的な許可設定
- 特定の依存関係をライセンスチェックから除外
