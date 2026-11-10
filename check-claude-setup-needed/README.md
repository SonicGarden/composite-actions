# check-claude-setup-needed

Claude Codeを使用してセットアップが必要かどうかを判定するアクションです。イベントテキストを分析して、コード修正やテスト実行などの作業が必要かどうかを自動判定します。event_textパラメータが未指定の場合は、GitHubイベントから自動的にテキストを抽出します。

## 使用方法

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

## 入力パラメータ

- `claude_code_oauth_token` (必須): Claude Code OAuth トークン
- `event_text` (任意): 分析対象のイベントテキスト（未指定の場合は自動で抽出）

## 出力パラメータ

- `needs_setup`: セットアップが必要かどうか（true/false）

## 判定条件

以下のいずれかを含む場合に「セットアップが必要」と判定されます：
- コードの修正・追加
- テストの実行
- データベース操作
- ビルドの実行
- 依存関係のインストール
