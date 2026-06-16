from flask import Flask, request, render_template_string
import sqlite3
import pandas as pd

app = Flask(__name__)

# ======================
# DB初期化
# ======================
def init_db():
    conn = sqlite3.connect("poker.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age TEXT,
        gender TEXT,
        experience TEXT,
        visit TEXT,
        image TEXT,
        overseas TEXT,
        ir_use TEXT,
        ir_support TEXT,
        join_intent TEXT,
        reason TEXT,
        comment TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ======================
# 回答ページ
# ======================
FORM_HTML = """
<h2>ポーカーアンケート</h2>
<form method="POST">

年齢:
<select name="age">
<option>18〜20</option>
<option>21〜25</option>
<option>26〜30</option>
<option>31以上</option>
</select><br><br>

性別:
<select name="gender">
<option>男性</option>
<option>女性</option>
<option>その他</option>
<option>回答しない</option>
</select><br><br>

ポーカー歴:
<select name="experience">
<option>半年未満</option>
<option>1年未満</option>
<option>1〜3年</option>
<option>3年以上</option>
</select><br><br>

来店頻度:
<select name="visit">
<option>月1回未満</option>
<option>月1〜3回</option>
<option>週1程度</option>
<option>週2以上</option>
</select><br><br>

IR利用意向:
<select name="ir_use">
<option>非常に利用したい</option>
<option>利用したい</option>
<option>どちらともいえない</option>
<option>あまり利用したくない</option>
<option>利用したくない</option>
</select><br><br>

導入賛成度:
<select name="ir_support">
<option>強くそう思う</option>
<option>そう思う</option>
<option>どちらともいえない</option>
<option>そう思わない</option>
<option>全くそう思わない</option>
</select><br><br>

自由記述:<br>
<textarea name="comment"></textarea><br><br>

<button type="submit">送信</button>
</form>

<a href="/admin">管理画面</a>
"""

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        data = request.form

        conn = sqlite3.connect("poker.db")
        c = conn.cursor()

        c.execute("""
        INSERT INTO responses (
            age, gender, experience, visit,
            image, overseas, ir_use, ir_support,
            join_intent, reason, comment
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("age"),
            data.get("gender"),
            data.get("experience"),
            data.get("visit"),
            "", "",  # 今回省略（必要なら追加OK）
            data.get("ir_use"),
            data.get("ir_support"),
            "", "",
            data.get("comment")
        ))

        conn.commit()
        conn.close()

        return "送信完了！"

    return render_template_string(FORM_HTML)

# ======================
# 管理画面（一覧＋分析）
# ======================
@app.route("/admin")
def admin():
    conn = sqlite3.connect("poker.db")
    df = pd.read_sql_query("SELECT * FROM responses", conn)

    total = len(df)

    # 男女別
    gender = df["gender"].value_counts()

    # 年齢別
    age = df["age"].value_counts()

    # 支持率
    support = df["ir_support"].value_counts()

    html = f"""
<h2>管理画面</h2>

<h3>回答数: {total}</h3>

<h3>男女別</h3>
{gender.to_string()}

<h3>年齢別</h3>
{age.to_string()}

<h3>導入賛成度</h3>
{support.to_string()}

<hr>
<h3>全回答</h3>
{df.to_html()}

<a href="/">戻る</a>
"""

    return html


if __name__ == "__main__":
    app.run(debug=True)