const express = require("express");
const { Pool } = require("pg");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

// Supabase接続
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

// データ取得
app.get("/api/answers", async (req, res) => {
  const result = await pool.query("SELECT * FROM answers");
  res.json(result.rows);
});

// データ追加
app.post("/api/answers", async (req, res) => {
  const { name, answer } = req.body;
  await pool.query(
    "INSERT INTO answers (name, answer) VALUES ($1, $2)",
    [name, answer]
  );
  res.json({ status: "ok" });
});

app.listen(3000, () => console.log("Server running on 3000"));