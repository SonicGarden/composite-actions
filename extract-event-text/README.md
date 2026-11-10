# extract-event-text

GitHubイベントタイプに応じてテキストを抽出するアクションです。さまざまなイベントタイプから適切なテキストを自動的に抽出します。

## 対応イベント

- `issue_comment` - イシューコメント（comment.body）
- `pull_request_review_comment` - プルリクエストレビューコメント（comment.body）
- `pull_request_review` - プルリクエストレビュー（review.body）
- `issues` - イシュー（issue.bodyまたはissue.title）

## 使用方法

```yaml
- name: Extract event text
  id: extract-event-text
  uses: SonicGarden/composite-actions/extract-event-text@main
```

## 入力パラメータ

なし（GitHub contextから自動的に取得）

## 出力パラメータ

- `text`: 抽出されたイベントテキスト（JSONエスケープ済み）
