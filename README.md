# 🏯 Acupuncture Dataset

**Open-source structured knowledge base for acupuncture: Master Tung, TCM, WAA, Jin's Three Needles.**

## 📊 Stats

| Metric | Value |
|--------|-------|
| 📚 Books | 162 |
| 📄 Chunks | 9 903 |
| 📝 Points | 590+ |
| 📦 Size | 51 MB |
| 🌍 Languages | Russian, English, Portuguese |

## Structure

```
data/
  chunks/          — text chunks from books
    tung/  (1348)  — Master Tung
    tcm/   (4773)  — TCM
    waa/    (42)   — Wrist-Ankle
    jin/   (840)   — Jin's Three Needles
    ear/    (20)   — Auriculotherapy
    manual/(524)   — Manual therapy
    psyche/(119)   — Psycho-emotional
    general/(2603) — General materials
  tung-points.json  — 212 Master Tung points
  tcm-points.json   — 346 TCM points
  dao-ma.json       — 11 Dao Ma combinations
  waa-protocols.json— 22 WAA protocols
```

## Chunk Format

```json
{
  "source": "Robert_Chu_Master_Tung's_Acupuncture.pdf",
  "title": "22.05 Ling Gu — location and indications",
  "text": "Point description (Russian or English)...",
  "category": "tung"
}
```

## MCP Server

```bash
pip install mcp requests
python server/server.py
```

## Books included

| Category | Books | Key titles |
|----------|-------|------------|
| 🏯 **Master Tung** | 50 | Master TUNG Tech, TUNG BOOK 2, Robert Chu, Nelson Beloto, Brad Wisnant |
| 🏛 **TCM** | 16 | Maciocia, Falev, Maciocia, Schnorrenberger |
| 🌿 **WAA** | 6 | WAA Atlas, WAA Book, Heart of WAA |
| 🪡 **Jin's Needles** | 9 | Jin's Three Needles protocols |
| 👂 **Auriculotherapy** | 7 | Pesikov, Hijama atlas |
| 💆 **Manual therapy** | 7 | Myofascial pain, manual medicine |
| 🧠 **Psycho-emotional** | 1 | Emotions in TCM |
| 📦 **General** | 66 | Li Yun pain management, 6 Elements, Cosmetic acupuncture |

## License

MIT — free to use, study, and modify.
