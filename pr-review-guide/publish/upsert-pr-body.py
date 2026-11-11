# PR 本文へレビューガイドのブロックを marker 方式で upsert する。
# 入力: stdin に `gh api repos/{owner}/{repo}/pulls/N` の JSON。
# 出力: 環境変数 OUT_FILE のパスへ新しい本文を書き出す(呼び出し側が gh pr edit --body-file へ渡す)。
# NOTE: 信頼できない値・モデル出力は環境変数でのみ受け取る(${{ }} をソースへ差し込む経路が無い)。
import json, os, re, sys

START = "<!-- start pr-review-guide -->"
END = "<!-- end pr-review-guide -->"
# NOTE: 非貪欲マッチで、marker 対が複数あっても最初の1組だけを対象にする
PATTERN = re.compile(re.escape(START) + r"[\s\S]*?" + re.escape(END))

# NOTE: head SHA を載せるのは、レビュアーが「このガイドは最新の push に対応して
#       いるか」を判断する唯一の手段だから。保持期間を明記するのは、期限切れの
#       リンクを踏んだ人が「壊れている」と誤解しないため。
block = "\n".join([
    START,
    "## レビューガイド",
    "",
    f"初見のレビュアー向けの解説ページ: [review-guide.html]({os.environ['ARTIFACT_URL']})",
    "",
    f"- 対象 head SHA: `{os.environ['HEAD_SHA']}`",
    f"- 生成した実行: [Actions run]({os.environ['RUN_URL']})",
    f"- artifact の保持期間: {os.environ['RETENTION_DAYS']} 日(閲覧には GitHub ログインが必要)",
    "",
    "head SHA が現在の head と異なる場合、このガイドは古い。`/guide` とコメントすると再生成する。",
    END,
])

# NOTE: 本文が未設定の PR では body が JSON の null になる("" ではない)
body = json.load(sys.stdin).get("body") or ""

if PATTERN.search(body):
    # NOTE: 置換文字列を lambda で渡す。文字列で渡すと re が \1 や \g<1> を
    #       後方参照として解釈し、URL や本文中のバックスラッシュで壊れる
    new = PATTERN.sub(lambda _m: block, body, count=1)
else:
    new = f"{body}\n\n{block}" if body else block

# NOTE: 参照実装(changed-lines-number-action の report.ts)は最後に trim() するが
#       採用しない。trim() は marker の外側(本文冒頭・末尾の空白)を書き換えるため、
#       「作者の文章をバイト単位で保持する」という要件と直接矛盾する。
# NOTE: newline="" で改行変換を無効化する。GitHub の本文は CRLF を含むことがあり、
#       既定の universal newlines だと LF へ潰れて「本文全体が変更された」差分になる。
with open(os.environ["OUT_FILE"], "w", encoding="utf-8", newline="") as fh:
    fh.write(new)
