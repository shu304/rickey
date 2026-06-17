from flask import Flask, request, redirect, render_template_string, session
import sqlite3
import os
import json

app = Flask(__name__)
app.secret_key = "secret"

DB = "survey.db"

# DB
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
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

# 🎴 アンケート
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = (
            request.form.get("name"),
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
        c.execute("INSERT INTO answers VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?)", data)
        conn.commit()
        conn.close()

        return "<h2>回答ありがとうございました！</h2><a href='/'>戻る</a>"

    return render_template_string("""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    body { background:#0b3d2e; color:white; text-align:center; font-family:sans-serif;}
    .card { background:#145a32; padding:15px; margin:10px; border-radius:10px;}
    input,select,textarea { width:90%; padding:10px; margin-top:10px;}
    button { width:90%; padding:15px; margin:20px; background:gold;}
    .checkbox-group {
    text-align:left;
    line-height:2;
    font-size:14px;
}

.checkbox-group label {
    display:flex;
    align-items:center;
    gap:10px;
    white-space:nowrap;   /* ← 改行させない */
}

.checkbox-group input {
    transform: scale(1.2); /* ← 押しやすくする */
}
    </style>
    </head>
    <body>

    <h2>ポーカーアンケート <span onclick="location.href='/login'">🂡</span></h2>

    <form method="POST">

    <div class="card">Q1 年齢<select name="age">
    <option>18〜20</option><option>21〜25</option><option>26〜30</option><option>31以上</option>
    </select></div>

    <div class="card">Q2 性別<select name="gender">
    <option>男性</option><option>女性</option><option>その他</option></select></div>

    <div class="card">Q3 ポーカー経験<select name="experience">
    <option>半年未満</option><option>1年未満</option><option>1〜3年</option><option>3年以上</option>
    </select></div>

    <div class="card">Q4 来店頻度<select name="frequency">
    <option>月1未満</option><option>月1〜3</option><option>週1</option><option>週2以上</option>
    </select></div>

    <div class="card">Q5 ポーカーへの印象<select name="perception">
    <option>ギャンブル</option><option>スポーツ</option><option>頭脳ゲーム</option><option>娯楽</option>
    </select>
    <input name="perception_other" placeholder="その他"></div>

    <div class="card">Q6 海外カジノでポーカー経験<select name="abroad">
    <option>ある</option><option>ない</option></select></div>

    <div class="card">Q7 IRカジノが開業したら<select name="ir_use">
    <option>したい</option><option>普通</option><option>したくない</option></select></div>

    <div class="card">Q8 IRにポーカーを導入するべきか<select name="ir_support">
    <option>賛成</option><option>普通</option><option>反対</option></select></div>

    <div class="card">Q9 もし導入されたら参加したいですか<select name="participate">
    <option>はい</option><option>いいえ</option></select></div>

    <div class="card" id="q10">
    Q10 導入してほしい理由
    <div class="checkbox-group">
    <label><input type="checkbox" name="reasons" value="ポーカー人口増加">ポーカー人口増加</label>
    <label><input type="checkbox" name="reasons" value="観光資源になる">観光資源になる</label>
    <label><input type="checkbox" name="reasons" value="国際大会開催">国際大会開催</label>
    <label><input type="checkbox" name="reasons" value="日本人選手育成">日本人選手育成</label>
    <label><input type="checkbox" name="reasons" value="エンタメ向上">エンタメ向上</label>
    </div>
    </div>

    <div class="card">Q11 コメント<textarea name="comment"></textarea></div>

    <button>送信</button>

    </form>
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
        return "NG"

    return """
    <div style="text-align:center;margin-top:100px;">
    <h2>ログイン</h2>
    <form method="POST">
    <input type="password" name="password">
    <br><br>
    <button>ログイン</button>
    </form>
    <br>
    <a href="/">← 解答画面に戻る</a>
    </div>
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

    return render_template_string(f"""
    <h2>管理画面</h2>
    <a href="/">← 解答画面に戻る</a>

    <table border=1 style="width:100%;font-size:12px;">
    <tr>
    <th>ID</th><th>年齢</th><th>性別</th><th>コメント</th>
    </tr>

    {''.join([f"""
    <tr>
    <td>{r[0]}</td>
    <td>{r[1]}</td>
    <td><a href='/user/{r[0]}'>{r[2]}</a></td>
    <td>{r[3]}</td>
    <td>{r[13]}</td>
    </tr>
    """ for r in rows])}
    </table>
    """)

# 👤 個別詳細
@app.route("/user/<int:id>")
def user(id):
    if not session.get("login"):
        return redirect("/login")

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    r = c.execute("SELECT * FROM answers WHERE id=?", (id,)).fetchone()
    conn.close()

    return f"""
    <p>年齢: {r[2]}</p>
    <p>性別: {r[3]}</p>
    <p>経験: {r[4]}</p>
    <p>頻度: {r[5]}</p>
    <p>印象: {r[6]}</p>
    <p>海外: {r[8]}</p>
    <p>IR利用: {r[9]}</p>
    <p>IR賛成: {r[10]}</p>
    <p>参加: {r[11]}</p>
    <p>理由: {r[12]}</p>
    <p>コメント: {r[13]}</p>

    <br>
    <a href="/admin">← 一覧に戻る</a>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)