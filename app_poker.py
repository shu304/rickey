from flask import Flask, request, redirect, render_template_string, session
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    body { background:#0b3d2e; color:white; font-family:sans-serif; }
    .card { background:#145a32; padding:20px; margin:15px; border-radius:10px; }
    button { width:90%; padding:12px; margin:20px; background:gold; border:none; border-radius:10px;}
    </style>
    </head>
    <body>

    <h1>♠ ポーカーアンケート ♥ <span onclick="location.href='/login'" style="cursor:pointer;">🂡</span></h1>

    <form method="POST">

    <div class="card">Q1 年齢
    <select name="age">
    <option>18〜20</option><option>21〜25</option>
    <option>26〜30</option><option>31以上</option>
    </select></div>

    <div class="card">Q2 性別
    <select name="gender">
    <option>男性</option><option>女性</option>
    <option>その他</option><option>回答しない</option>
    </select></div>

    <div class="card">Q3 ポーカー歴
    <select name="experience">
    <option>半年未満</option><option>1年未満</option>
    <option>1〜3年</option><option>3年以上</option>
    </select></div>

    <div class="card">Q4 来店頻度
    <select name="frequency">
    <option>月1回未満</option><option>月1〜3回</option>
    <option>週1程度</option><option>週2以上</option>
    </select></div>

    <div class="card">Q5 印象
    <select name="perception">
    <option>ギャンブル</option>
    <option>スポーツ・競技</option>
    <option>頭脳ゲーム</option>
    <option>娯楽</option>
    <option>その他</option>
    </select>
    <input name="perception_other" placeholder="その他入力">
    </div>

    <div class="card">Q6 海外経験
    <select name="abroad">
    <option>ある</option><option>ない</option>
    </select></div>

    <div class="card">Q7 IR利用
    <select name="ir_use">
    <option>非常に利用したい</option>
    <option>利用したい</option>
    <option>どちらともいえない</option>
    <option>あまり利用したくない</option>
    <option>利用したくない</option>
    </select></div>

    <div class="card">Q8 賛成
    <select name="ir_support">
    <option>強くそう思う</option>
    <option>そう思う</option>
    <option>どちらともいえない</option>
    <option>そう思わない</option>
    <option>全くそう思わない</option>
    </select></div>

    <div class="card">Q9 参加
    <select name="participate" id="q9" onchange="toggleQ10()">
    <option>はい</option><option>いいえ</option><option>わからない</option>
    </select></div>

    <div class="card" id="q10">
    Q10 理由<br>
    <input type="checkbox" name="reasons" value="人口増加">人口増加<br>
    <input type="checkbox" name="reasons" value="観光">観光<br>
    <input type="checkbox" name="reasons" value="大会">大会<br>
    <input type="checkbox" name="reasons" value="育成">育成<br>
    <input type="checkbox" name="reasons" value="エンタメ">エンタメ
    </div>

    <div class="card">Q11
    <textarea name="comment"></textarea>
    </div>

    <button>送信</button>

    </form>

    <script>
    function toggleQ10(){
        const val = document.getElementById("q9").value;
        document.getElementById("q10").style.display =
            (val === "いいえ") ? "none" : "block";
    }
    </script>

    </body>
    </html>
    """)

# 🔐 ログイン
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == "20021006":
            session["login"] = True
            return redirect("/admin")
        return "パスワード違う"

    return """
    <form method="POST">
    パスワード<input type="password" name="password">
    <button>ログイン</button>
    </form>
    """

# 📊 管理画面（削除付き）
@app.route("/admin", methods=["GET","POST"])
def admin():
    if not session.get("login"):
        return redirect("/login")

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # 削除処理
    if request.method == "POST":
        ids = request.form.getlist("delete_ids")
        for i in ids:
            c.execute("DELETE FROM answers WHERE id=?", (i,))
        conn.commit()

    rows = c.execute("SELECT * FROM answers").fetchall()
    conn.close()

    html = """
    <h1>📊 管理画面</h1>
    <form method="POST">
    <table border="1" style="border-collapse:collapse;width:100%">
    <tr style="background:#333;color:white;">
    <th>削除</th><th>ID</th><th>年齢</th><th>性別</th>
    <th>経験</th><th>頻度</th><th>参加</th><th>理由</th>
    </tr>
    """

    for r in rows:
        html += f"""
        <tr>
        <td><input type="checkbox" name="delete_ids" value="{r[0]}"></td>
        <td>{r[0]}</td>
        <td>{r[1]}</td>
        <td>{r[2]}</td>
        <td>{r[3]}</td>
        <td>{r[4]}</td>
        <td>{r[10]}</td>
        <td>{r[11]}</td>
        </tr>
        """

    html += """
    </table>
    <button type="submit">選択したデータを削除</button>
    </form>
    """

    return html

# Render用
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)