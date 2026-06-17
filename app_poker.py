from flask import Flask, request, redirect, render_template_string, session
import sqlite3
import os
import json

app = Flask(__name__)
app.secret_key = "secret"

DB = "survey.db"

# DB初期化
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

# 🎴 アンケート
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
        c.execute("INSERT INTO answers VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?)", data)
        conn.commit()
        conn.close()

        return "<h2>回答ありがとうございました！</h2>"

    return render_template_string("""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    body { background:#0b3d2e; color:white; font-family:sans-serif; text-align:center;}
    .card { background:#145a32; padding:15px; margin:10px; border-radius:10px;}
    select, textarea, input { width:90%; padding:12px; margin-top:10px; font-size:16px; border-radius:8px;}
    button { width:90%; padding:15px; margin:20px; background:gold; border:none; border-radius:10px; font-size:18px;}
    .checkbox-group { text-align:left; line-height:2; font-size:15px;}
    </style>
    </head>
    <body>

    <h2>♠ ポーカーアンケート ♥ <span onclick="location.href='/login'">🂡</span></h2>

    <form method="POST">

    <div class="card">Q1 年齢<select name="age">
    <option>18〜20</option><option>21〜25</option><option>26〜30</option><option>31以上</option>
    </select></div>

    <div class="card">Q2 性別<select name="gender">
    <option>男性</option><option>女性</option><option>その他</option><option>回答しない</option>
    </select></div>

    <div class="card">Q3 ポーカー経験<select name="experience">
    <option>半年未満</option><option>1年未満</option><option>1〜3年</option><option>3年以上</option>
    </select></div>

    <div class="card">Q4 来店頻度<select name="frequency">
    <option>月1未満</option><option>月1〜3</option><option>週1</option><option>週2以上</option>
    </select></div>

    <div class="card">Q5 ポーカーへの印象<select name="perception">
    <option>ギャンブル</option><option>スポーツ</option><option>頭脳ゲーム</option><option>娯楽</option><option>その他</option>
    </select>
    <input name="perception_other" placeholder="その他"></div>

    <div class="card">Q6 海外カジノでポーカー経験<select name="abroad">
    <option>ある</option><option>ない</option></select></div>

    <div class="card">Q7 IRカジノが開業したら<select name="ir_use">
    <option>非常に利用したい</option><option>利用したい</option>
    <option>どちらとも思わない</option><option>したくない</option>
    </select></div>

    <div class="card">Q8 IRにポーカーを導入するべきか<select name="ir_support">
    <option>強く賛成</option><option>賛成</option><option>普通</option><option>反対</option>
    </select></div>

    <div class="card">Q9 もし導入されたら参加したいですか<select name="participate" id="q9" onchange="toggleQ10()">
    <option>はい</option><option>いいえ</option><option>わからない</option>
    </select></div>

    <div class="card" id="q10">
    Q10 導入してほしい理由
    <div class="checkbox-group">
    <label><input type="checkbox" name="reasons" value="ポーカー人口増加"> ポーカー人口増加</label><br>
    <label><input type="checkbox" name="reasons" value="観光資源になる"> 観光資源になる</label><br>
    <label><input type="checkbox" name="reasons" value="国際大会開催"> 国際大会開催</label><br>
    <label><input type="checkbox" name="reasons" value="日本人選手育成"> 日本人選手育成</label><br>
    <label><input type="checkbox" name="reasons" value="エンタメ向上"> エンタメ向上</label>
    </div>
    </div>

    <div class="card">Q11 コメント<textarea name="comment"></textarea></div>

    <button>送信</button>

    </form>

    <script>
    function toggleQ10(){
        let v = document.getElementById("q9").value;
        document.getElementById("q10").style.display = (v === "いいえ") ? "none" : "block";
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
        return "NG"

    return """
    <body style="background:#0b3d2e;font-family:sans-serif;">
    <div style="max-width:400px;margin:100px auto;background:white;padding:30px;border-radius:15px;text-align:center;">
    <h2>管理ログイン</h2>
    <form method="POST">
    <input type="password" name="password" placeholder="パスワード"
    style="width:100%;padding:15px;font-size:18px;border-radius:10px;border:1px solid #ccc;">
    <br><br>
    <button style="width:100%;padding:15px;background:#145a32;color:white;border:none;border-radius:10px;">ログイン</button>
    </form>
    </div>
    </body>
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

    data_json = json.dumps(rows)

    return render_template_string(f"""
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>

    <body style="font-family:sans-serif;text-align:center;">

    <h2>管理画面</h2>

    <button onclick="toggle(1)">年齢</button>
    <button onclick="toggle(2)">性別</button>
    <button onclick="toggle(3)">経験</button>
    <button onclick="toggle(4)">頻度</button>
    <button onclick="toggle(10)">参加</button>
    <button onclick="toggle(11)">理由</button>

    <canvas id="chart"></canvas>

    <h3>回答一覧</h3>
    <table border="1" style="width:100%;font-size:12px;">
    <tr>
    <th>ID</th><th>年齢</th><th>性別</th><th>経験</th><th>頻度</th><th>参加</th><th>削除</th>
    </tr>
    {''.join([f"""
    <tr>
    <td>{r[0]}</td>
    <td>{r[1]}</td>
    <td>{r[2]}</td>
    <td>{r[3]}</td>
    <td>{r[4]}</td>
    <td>{r[10]}</td>
    <td><button onclick="deleteOne({r[0]})" style="background:red;color:white;">削除</button></td>
    </tr>
    """ for r in rows])}
    </table>

    <script>
    const data = {data_json};
    let current = null;
    let chart = null;

    function toggle(index){{
        if(current === index){{
            if(chart) chart.destroy();
            current = null;
            return;
        }}

        current = index;
        if(chart) chart.destroy();

        const count = {{}};

        data.forEach(d => {{
            let val = d[index];
            if(index == 11){{
                if(val) val.split(',').forEach(v => count[v]=(count[v]||0)+1);
            }} else {{
                count[val] = (count[val]||0)+1;
            }}
        }});

        chart = new Chart(document.getElementById('chart'), {{
            type:'pie',
            data:{{
                labels:Object.keys(count),
                datasets:[{{data:Object.values(count)}}]
            }}
        }});
    }}

    function deleteOne(id){{
        if(confirm("このデータ削除する？")){{
            fetch('/delete/' + id).then(()=>location.reload());
        }}
    }}
    </script>

    </body>
    </html>
    """)

# 🗑️ 個別削除
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM answers WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)