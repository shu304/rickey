import { useState, useEffect } from "react";

function App() {
  const [answers, setAnswers] = useState([]);

  const [form, setForm] = useState({
    age: "18〜20",
    gender: "男性",
    experience: "半年未満",
    frequency: "月1未満",
    perception: "ギャンブル",
    perception_other: "",
    abroad: "ある",
    ir_use: "したい",
    ir_support: "賛成",
    participate: "はい",
    reasons: [],
    reasons_other: "",
    comment: ""
  });

  const URL = "https://poker-survey.onrender.com/api/answers";

  // 初回表示でデータ取得
  useEffect(() => {
    fetch(URL)
      .then(res => res.json())
      .then(data => setAnswers(data));
  }, []);

  // チェックボックス処理
  const toggleReason = (value) => {
    setForm(prev => {
      const exists = prev.reasons.includes(value);
      return {
        ...prev,
        reasons: exists
          ? prev.reasons.filter(r => r !== value)
          : [...prev.reasons, value]
      };
    });
  };

  // 送信
  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      ...form,
      reasons: [...form.reasons, form.reasons_other].join(",")
    };

    await fetch(URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const res = await fetch(URL);
    const data = await res.json();
    setAnswers(data);
  };

  return (
    <div style={{
      background: "#0b3d2e",
      color: "white",
      minHeight: "100vh",
      padding: "30px",
      textAlign: "center",
      fontFamily: "sans-serif",
      lineHeight: "1.8em"
    }}>

      <h2>
        ポーカーアンケート{" "}
        <span
          style={{ cursor: "pointer" }}
          onClick={() => window.location.href = "https://poker-survey.onrender.com/admin"}
        >
          🂡
        </span>
      </h2>


      <form onSubmit={handleSubmit}>


        {/* 年齢 */}
        <div className="card">
          年齢
          <select value={form.age} onChange={e => setForm({ ...form, age: e.target.value })}>
            <option>18〜20</option>
            <option>21〜25</option>
            <option>26〜30</option>
            <option>31以上</option>
          </select>
        </div>

        {/* 性別 */}
        <div className="card">
          性別
          <select value={form.gender} onChange={e => setForm({ ...form, gender: e.target.value })}>
            <option>男性</option>
            <option>女性</option>
            <option>その他</option>
          </select>
        </div>

        {/* 経験 */}
        <div className="card">
          経験
          <select value={form.experience} onChange={e => setForm({ ...form, experience: e.target.value })}>
            <option>半年未満</option>
            <option>1年未満</option>
            <option>1〜3年</option>
            <option>3年以上</option>
          </select>
        </div>

        {/* 来店頻度 */}
        <div className="card">
          来店頻度
          <select value={form.frequency} onChange={e => setForm({ ...form, frequency: e.target.value })}>
            <option>月1未満</option>
            <option>月1〜3</option>
            <option>週1</option>
            <option>週2以上</option>
          </select>
        </div>

        {/* ポーカーの印象 */}
        <div className="card">
          ポーカーの印象
          <select value={form.perception} onChange={e => setForm({ ...form, perception: e.target.value })}>
            <option>ギャンブル</option>
            <option>スポーツ</option>
            <option>頭脳ゲーム</option>
            <option>娯楽</option>
          </select>

          <input
            placeholder="その他"
            value={form.perception_other}
            onChange={e => setForm({ ...form, perception_other: e.target.value })}
          />
        </div>

        {/* 海外経験 */}
        <div className="card">
          海外カジノでのポーカー経験
          <select value={form.abroad} onChange={e => setForm({ ...form, abroad: e.target.value })}>
            <option>ある</option>
            <option>ない</option>
          </select>
        </div>

        {/* IR利用 */}
        <div className="card">
          IRカジノが起業したら利用
          <select value={form.ir_use} onChange={e => setForm({ ...form, ir_use: e.target.value })}>
            <option>したい</option>
            <option>どちらとも思わない</option>
            <option>したくない</option>
          </select>
        </div>

        {/* IR賛否 */}
        <div className="card">
          IRへポーカー導入への賛否（Q8）
          <select
            value={form.ir_support}
            onChange={e => setForm({ ...form, ir_support: e.target.value })}
          >
            <option>賛成</option>
            <option>どちらとも思わない</option>
            <option>反対</option>
          </select>
        </div>

        {/* 参加意向 */}
        <div className="card">
          もし導入されたら参加したいか
          <select value={form.participate} onChange={e => setForm({ ...form, participate: e.target.value })}>
            <option>はい</option>
            <option>いいえ</option>
          </select>
        </div>
        {/* Q10：賛成のときだけ表示 */}
        {form.ir_support !== "反対" && (
          <div className="card" id="q10">
            導入してほしい理由

            <div className="checkbox-group">

              {[
                "ポーカー人口増加",
                "観光資源になる",
                "国際大会開催",
                "日本人選手育成",
                "エンタメ向上"
              ].map(reason => (
                <label key={reason}>
                  <input
                    type="checkbox"
                    checked={form.reasons.includes(reason)}
                    onChange={() => toggleReason(reason)}
                  />
                  <span>{reason}</span>
                </label>
              ))}

            </div>

            <br />
            その他：
            <input
              type="text"
              placeholder="自由入力"
              value={form.reasons_other}
              onChange={e => setForm({ ...form, reasons_other: e.target.value })}
            />
          </div>
        )}
        {/* コメント */}
        <div className="card">
          自由にコメント
          <textarea
            value={form.comment}
            onChange={e => setForm({ ...form, comment: e.target.value })}
          />
        </div>

        <button style={{ width: "90%", padding: "15px", margin: "20px", background: "gold" }}>
          送信
        </button>

      </form>

      <h2>回答一覧</h2>
      <ul>
        {answers.map(a => (
          <li key={a[0]}>
            {a[1]} / {a[2]} / {a[3]} / {a[13]}
          </li>
        ))}
      </ul>

    </div>
  );
}

<button
  onClick={() => window.location.href="https://poker-survey.onrender.com/admin"}
>
  管理画面へ
</button>

export default App;
