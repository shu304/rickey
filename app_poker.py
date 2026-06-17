from flask import Flask, request, redirect, render_template_string, session
import sqlite3
import os
from collections import Counter

app = Flask(__name__)
app.secret_key = "secret"

DB = "survey.db"

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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        reasons = ",".join(request.form.getlist("reasons"))
        other = request.form.get("reasons_other")

        if other:
            reasons += "," + other

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
            reasons,
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

/* チェックボックス整列 */
.checkbox-group label {
    display: grid;
    grid-template-columns: 30px 1fr;
    align-items: center;
    width: 100%;
}
.checkbox-group span {
    text-align: center;
}
</style>

<script>
function toggleQ10() {
    const q8 = document.querySelector("select[name='ir_support']").value;
    const q10 = document.getElementById("q10");

    if (q8 === "反対") {
        q10.style.display = "none";
    } else {
        q10.style.display = "block";
    }
}
</script>

</head>
<body>

<h2>ポーカーアンケート <span onclick="location.href='/login'">🂡</span></h2>

<form method="POST">

<div class="card">名前<input name="name" required></div>

<div class="card">年齢<select name="age">
<option>18〜20</option><option>21〜25</option><option>26〜30</option><option>31以上</option>
</select></div>

<div class="card">性別<select name="gender">
<option>男性</option><option>女性</option><option>その他</option></select></div>

<div class="card">経験<select name="experience">
<option>半年未満</option><option>1年未満</option><option>1〜3年</option><option>3年以上</option>
</select></div>

<div class="card">来店頻度<select name="frequency">
<option>月1未満</option><option>月1〜3</option><option>週1</option><option>週2以上</option>
</select></div>

<div class="card">ポーカーの印象<select name="perception">
<option>ギャンブル</option><option>スポーツ</option><option>頭脳ゲーム</option><option>娯楽</option>
</select>
<input name="perception_other" placeholder="その他"></div>

<div class="card">海外カジノでのポーカー経験<select name="abroad">
<option>ある</option><option>ない</option></select></div>

<div class="card">IRカジノが起業したら利用<select name="ir_use">
<option>したい</option><option>どちらとも思わない</option><option>したくない</option></select></div>

<div class="card">IRへポーカー導入への賛否（Q8）
<select name="ir_support" onchange="toggleQ10()">
<option>賛成</option><option>どちらとも思わない</option><option>反対</option>
</select>
</div>

<div class="card">もし導入されたら参加したいか<select name="participate">
<option>はい</option><option>いいえ</option></select></div>

<!-- Q10 -->
<div class="card" id="q10">
導入してほしい理由

<div class="checkbox-group">

<label>
<input type="checkbox" name="reasons" value="ポーカー人口増加">
<span>ポーカー人口増加</span>
</label>

<label>
<input type="checkbox" name="reasons" value="観光資源になる">
<span>観光資源になる</span>
</label>

<label>
<input type="checkbox" name="reasons" value="国際大会開催">
<span>国際大会開催</span>
</label>

<label>
<input type="checkbox" name="reasons" value="日本人選手育成">
<span>日本人選手育成</span>
</label>

<label>
<input type="checkbox" name="reasons" value="エンタメ向上">
<span>エンタメ向上</span>
</label>

</div>

<br>
その他：
<input type="text" name="reasons_other" placeholder="自由入力">

</div>

<div class="card">自由にコメント<textarea name="comment"></textarea></div>

<button>送信</button>

</form>

</body>
</html>
    """)

# ======================
# 🔐 ログイン
# ======================
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == "20021006":
            session["login"] = True
            return redirect("/admin")
        return "NG"

    return """
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    body {
        background:#0b3d2e;
        color:white;
        text-align:center;
        font-family:sans-serif;
    }
    input,button {
        width:80%;
        padding:15px;
        margin-top:15px;
        font-size:16px;
    }
    button {
        background:gold;
    }
    </style>
    </head>
    <body>

    <h2>ログイン</h2>

    <form method="POST">
    <input type="password" name="password" placeholder="パスワード">
    <br>
    <button>ログイン</button>
    </form>

    <br>
    <a href="/" style="color:white;">← 解答画面に戻る</a>

    </body>
    </html>
    """


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
    <br><br>
    <a href="/charts">📊 円グラフを見る</a>

    <table border=1 style="width:100%;font-size:12px;">
    <tr>
    <th>ID</th><th>名前</th><th>年齢</th><th>性別</th><th>コメント</th>
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


# ======================
# 📊 円グラフ（11項目）
# ======================
@app.route("/charts")
def charts():
    if not session.get("login"):
        return redirect("/login")

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    rows = c.execute("SELECT * FROM answers").fetchall()
    conn.close()

    def make_chart(data, title):
        count = Counter(data)
        total = sum(count.values())

        labels = list(count.keys())
        values = list(count.values())

        return f"""
        <h3>{title}</h3>
        <p>合計: {total}</p>
        <ul>
        {''.join([f"<li>{k}: {v}</li>" for k,v in count.items()])}
        </ul>

        <canvas id="{title}"></canvas>

        <script>
        new Chart(document.getElementById("{title}"), {{
            type: 'pie',
            data: {{
                labels: {labels},
                datasets: [{{
                    data: {values}
                }}]
            }}
        }});
        </script>
        """

    age = [r[2] for r in rows]
    gender = [r[3] for r in rows]
    exp = [r[4] for r in rows]
    freq = [r[5] for r in rows]
    perception = [r[6] for r in rows]
    abroad = [r[8] for r in rows]
    ir_use = [r[9] for r in rows]
    ir_support = [r[10] for r in rows]
    participate = [r[11] for r in rows]

    # 理由（分解）
    reasons_list = []
    for r in rows:
        if r[12]:
            reasons_list += r[12].split(",")

    comments = ["あり" if r[13] else "なし" for r in rows]

    return f"""
    <html>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <h2>円グラフ分析（全11項目）</h2>

    {make_chart(age,"年齢")}
    {make_chart(gender,"性別")}
    {make_chart(exp,"経験")}
    {make_chart(freq,"頻度")}
    {make_chart(perception,"印象")}
    {make_chart(abroad,"海外経験")}
    {make_chart(ir_use,"IR利用")}
    {make_chart(ir_support,"IR賛否")}
    {make_chart(participate,"参加")}
    {make_chart(reasons_list,"理由")}
    {make_chart(comments,"コメント有無")}

    <br><br>
    <a href="/admin">← 一覧に戻る</a>
    </html>
    """


@app.route("/user/<int:id>")
def user(id):
    if not session.get("login"):
        return redirect("/login")

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    r = c.execute("SELECT * FROM answers WHERE id=?", (id,)).fetchone()
    conn.close()

    return f"""
    <h2>詳細</h2>
    <p>年齢: {r[2]}</p>
    <p>性別: {r[3]}</p>
    <p>経験: {r[4]}</p>
    <p>頻度: {r[5]}</p>
    <p>コメント: {r[13]}</p>

    <a href="/admin">← 戻る</a>
    """


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)