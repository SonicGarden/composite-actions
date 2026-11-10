# license-finder

プロジェクトの依存関係のライセンスをチェックし、承認されていないライセンスを検出するアクションです。商用利用可能な安全なライセンスがデフォルトで設定されており、レポートをGitHub Actions Summaryに出力します。

## 使用方法

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

# license_finder のバージョンを固定する場合
- name: Check licenses with pinned license_finder
  uses: SonicGarden/composite-actions/license-finder@main
  with:
    version: "7.2.1"
```

## 入力パラメータ

- `additional-licenses` (省略可): 追加で許可するライセンス（カンマ区切り）
- `ignored-dependencies` (省略可): ライセンスチェックから除外する依存関係（カンマ区切り）
- `version` (省略可): インストールする license_finder gem のバージョン（例: `7.2.1`）。省略すると、実行時点の最新版をインストールする

## デフォルトで許可されているライセンス

商用利用可能な主要なオープンソースライセンス（MIT、Apache-2.0、BSDファミリーなど）がデフォルトで許可されています。Ruby、Pythonなどの言語固有のライセンスや、フォント用ライセンス（OFL-1.1）も含まれています。

## 機能

- 未承認ライセンスの検出
- GitHub Actions Summaryへのマークダウン形式でのレポート出力
- 追加ライセンスの動的な許可設定
- 特定の依存関係をライセンスチェックから除外
