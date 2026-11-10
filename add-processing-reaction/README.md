# add-processing-reaction

GitHubイベント（イシュー、プルリクエスト、コメントなど）に応じて処理中のリアクション（👀）を自動的に追加するアクションです。

## 対応イベント

- `issue_comment` - イシューコメント
- `pull_request_review_comment` - プルリクエストレビューコメント
- `issues` - イシュー
- `pull_request_review` - プルリクエストレビュー

## 使用方法

```yaml
- name: Add processing reaction
  uses: SonicGarden/composite-actions/add-processing-reaction@main
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

## 必要な権限

- `contents: read`
- `issues: write`
- `pull-requests: write`
