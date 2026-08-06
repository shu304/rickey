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

  // 初回データ取得
  useEffect(() => {
    fetch(URL)
      .then(res => res.json())
      .then(data => setAnswers(data));
  }, []);

  // チェックボックス
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

  // ✅ 送信（これだけ残す）
  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      ...form,
      reasons: [...form.reasons, form.reasons_other].join(",")
    };

    await fetch(URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    alert("送信成功！");

    // 再取得
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
      textAlign: "center"
    }}>

      <h2>ポーカーアンケート</h2>

      <form onSubmit={handleSubmit}>

        <div>
          年齢
          <select value={form.age} onChange={e => setForm({ ...form, age: e.target.value })}>
            <option>18〜20</option>
            <option>21〜25</option>
            <option>26〜30</option>
            <option>31以上</option>
          </select>
        </div>

        <div>
          性別
          <select value={form.gender} onChange={e => setForm({ ...form, gender: e.target.value })}>
            <option>男性</option>
            <option>女性</option>
            <option>その他</option>
          </select>
        </div>

        <div>
          経験
          <select value={form.experience} onChange={e => setForm({ ...form, experience: e.target.value })}>
            <option>半年未満</option>
            <option>1年未満</option>
            <option>1〜3年</option>
            <option>3年以上</option>
          </select>
        </div>

        <div>
          来店頻度
          <select value={form.frequency} onChange={e => setForm({ ...form, frequency: e.target.value })}>
            <option>月1未満</option>
            <option>月1〜3</option>
            <option>週1</option>
            <option>週2以上</option>
          </select>
        </div>

        <div>
          ポーカーの印象
          <select value={form.perception} onChange={e => setForm({ ...form, perception: e.target.value })}>
            <option>ギャンブル</option>
            <option>スポーツ</option>
            <option>頭脳ゲーム</option>
            <option>娯楽</option>
          </select>
        </div>

        <button type="submit">送信</button>

      </form>

      <h2>回答一覧</h2>

      {answers.map((a, i) => (
        <div key={i}>
          <p>年齢: {a[1]}</p>
          <p>性別: {a[2]}</p>
        </div>
      ))}

    </div>
  );
}

export default App;