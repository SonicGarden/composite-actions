# get-user-secret-key

ユーザー名を取得し、指定されたキーリストから前方一致でSecretキーを検索するアクションです。GitHub Actionsでユーザー固有のSecretキーを動的に取得する際に使用します。

## 使用方法

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

## 入力パラメータ

- `username` (省略可): 対象のユーザー名（省略時はgithub.actorから自動取得）
- `available_keys` (必須): カンマ区切りの有効なSecretキーリスト

## 出力パラメータ

- `exists`: キーが存在するかどうか（true/false）
- `secret_key`: 見つかったSecretキー
- `username`: 使用されたユーザー名
