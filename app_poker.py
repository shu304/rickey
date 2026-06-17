from flask import Flask, request, redirect, url_for, render_template_string, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret"

DB = "survey.db"

# DB作成
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age TEXT,
        gender TEXT,
        experience TEXT,
        frequency TEXT,
        perception TEXT,
        perception_other TEXT,
        abroad TEXT,
        ir_use TEXT,
        ir_support TEXT,
        participate TEXT,
        reasons TEXT,
        comment TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# 🎴 アンケート画面
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = (
            request.form.get("age"),
            request.form.get("gender"),
            request.form.get("experience"),
            request.form.get("frequency"),
            request.form.get("perception"),
            request.form.get("perception_other"),
            request.form.get("abroad"),
            request.form.get("ir_use"),
            request.form.get("ir_support"),
            request.form.get("participate"),
            ",".join(request.form.getlist("reasons")),
            request.form.get("comment")
        )

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("""
        INSERT INTO answers (
            age, gender, experience, frequency, perception,
            perception_other, abroad, ir_use, ir_support,
            participate, reasons, comment
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, data)
        conn.commit()
        conn.close()

        return "<h2>回答ありがとうございました！</h2>"

    return render_template_string("""
    <html>
    <head>
    <style>
    body { background:#0b3d2e; color:white; font-family:sans-serif; }
    .card { background:#145a32; padding:20px; margin:20px; border-radius:10px; }
    h2 { color:#f1c40f; }
    </style>
    </head>
    <body>
    <h1>♠ ポーカーアンケート ♥</h1>
    <form method="POST">

    <div class="card">
    Q1 年齢<br>
    <select name="age">
        <option>18〜20</option><option>21〜25</option>
        <option>26〜30</option><option>31以上</option>
    </select>
    </div>

    <div class="card">
    Q2 性別<br>
    <select name="gender">
        <option>男性</option><option>女性</option>
        <option>その他</option><option>回答しない</option>
    </select>
    </div>

    <div class="card">
    Q3 ポーカー歴<br>
    <select name="experience">
        <option>半年未満</option><option>1年未満</option>
        <option>1〜3年</option><option>3年以上</option>
    </select>
    </div>

    <div class="card">
    Q4 月の来店頻度<br>
    <select name="frequency">
        <option>月1回未満</option><option>月1〜3回</option>
        <option>週1程度</option><option>週2以上</option>
    </select>
    </div>

    <div class="card">
    Q5 ポーカーの印象<br>
    <select name="perception">
        <option>ギャンブル</option>
        <option>スポーツ・競技</option>
        <option>頭脳ゲーム</option>
        <option>娯楽</option>
        <option>その他</option>
    </select><br>
    その他: <input name="perception_other">
    </div>

    <div class="card">
    Q6 海外経験<br>
    <select name="abroad">
        <option>ある</option><option>ない</option>
    </select>
    </div>

    <div class="card">
    Q7 IR利用意向<br>
    <select name="ir_use">
        <option>非常に利用したい</option>
        <option>利用したい</option>
        <option>どちらともいえない</option>
        <option>あまり利用したくない</option>
        <option>利用したくない</option>
    </select>
    </div>

    <div class="card">
    Q8 IR導入賛成<br>
    <select name="ir_support">
        <option>強くそう思う</option>
        <option>そう思う</option>
        <option>どちらともいえない</option>
        <option>そう思わない</option>
        <option>全くそう思わない</option>
    </select>
    </div>

    <div class="card">
    Q9 参加したい？<br>
    <select name="participate">
        <option>はい</option><option>いいえ</option><option>わからない</option>
    </select>
    </div>

    <div class="card">
    Q10 理由（複数）<br>
    <input type="checkbox" name="reasons" value="ポーカー人口増加">人口増加<br>
    <input type="checkbox" name="reasons" value="観光資源になる">観光<br>
    <input type="checkbox" name="reasons" value="国際大会開催">大会<br>
    <input type="checkbox" name="reasons" value="日本人選手育成">育成<br>
    <input type="checkbox" name="reasons" value="エンタメ向上">エンタメ<br>
    <input type="checkbox" name="reasons" value="その他">その他
    </div>

    <div class="card">
    Q11 自由記述<br>
    <textarea name="comment"></textarea>
    </div>

    <button type="submit">送信</button>
    </form>
    </body>
    </html>
    """)

# 🔐 管理画面ログイン
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == "20021006":
            session["login"] = True
            return redirect("/admin")
        else:
            return "パスワード違う"

    return """
    <form method="POST">
    パスワード: <input type="password" name="password">
    <button>ログイン</button>
    </form>
    """

# 📊 管理画面
@app.route("/admin")
def admin():
    if not session.get("login"):
        return redirect("/login")

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    rows = c.execute("SELECT * FROM answers").fetchall()
    conn.close()

    return f"<h2>回答一覧 {len(rows)}件</h2>" + "<br>".join([str(r) for r in rows])


# Render用
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)