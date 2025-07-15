# composite-actions

GitHub Actionsで使用するComposite Actionsのコレクション

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

Claude Codeを使用してセットアップが必要かどうかを判定するアクションです。イベントテキストを分析して、コード修正やテスト実行などの作業が必要かどうかを自動判定します。

#### 使用方法

```yaml
- name: Check Claude setup needed
  uses: SonicGarden/composite-actions/check-claude-setup-needed@main
  with:
    claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
    event_text: ${{ steps.extract-event-text.outputs.text }}
```

#### 入力パラメータ

- `claude_code_oauth_token` (必須): Claude Code OAuth トークン
- `event_text` (必須): 分析対象のイベントテキスト

#### 出力パラメータ

- `needs_setup`: セットアップが必要かどうか（true/false）

#### 判定条件

以下のいずれかを含む場合に「セットアップが必要」と判定されます：
- コードの修正・追加
- テストの実行
- データベース操作
- ビルドの実行
- 依存関係のインストール

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

### generate-claude-token-key

ユーザー名からClaude tokenのシークレットキー名を生成するアクションです。GitHub Actionsでユーザー固有のClaude tokenを参照する際に使用します。

#### 対応イベント

- `issue_comment` - イシューコメント（comment.user.login）
- `pull_request_review_comment` - プルリクエストレビューコメント（comment.user.login）
- `pull_request_review` - プルリクエストレビュー（review.user.login）
- `issues` - イシュー（issue.user.login）
- `pull_request` - プルリクエスト（pull_request.user.login）

#### 使用方法

```yaml
- name: Generate Claude token key
  id: generate-token-key
  uses: SonicGarden/composite-actions/generate-claude-token-key@main
  with:
    username: ${{ github.actor }}
```

または、usernameを省略してイベントから自動取得：

```yaml
- name: Generate Claude token key
  id: generate-token-key
  uses: SonicGarden/composite-actions/generate-claude-token-key@main
```

#### 入力パラメータ

- `username` (省略可): 対象のユーザー名（省略時はイベントから自動取得）

#### 出力パラメータ

- `token_key`: Claude tokenのシークレットキー名（例: `JOHN_CLAUDE_CODE_OAUTH_TOKEN`）
