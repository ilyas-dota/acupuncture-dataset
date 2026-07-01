# 🏯 Acupuncture Dataset

**Open-source база знаний по акупунктуре — Мастер Тун, ТКМ, WAA, Три Иглы Цзиня.**

📊 **10 332 чанка** из **162 книг**, структурированных для AI-агентов и MCP серверов.

## Структура

```
data/
  chunks/          — чанки текста
    tung/  (1348)  — Мастер Тун
    tcm/   (4773)  — ТКМ
    waa/    (42)   — WAA
    jin/   (840)   — Три Иглы Цзиня
    ear/    (20)   — Аурикулотерапия
    manual/(524)   — Мануальная терапия
    psyche/(119)   — Психоэмоциональные
    general/(2603) — Общие материалы
  tung-points.json  — 212 точек Туна
  tcm-points.json   — 346 точек ТКМ
  dao-ma.json       — 11 Dao Ma комбинаций
  waa-protocols.json— 22 протокола WAA
```

## Формат чанка

```json
{
  "source": "Robert_Chu_Master_Tung's_Acupuncture.pdf",
  "title": "22.05 Ling Gu — локация и показания",
  "text": "Описание точки на русском или английском...",
  "category": "tung"
}
```

## MCP сервер

В папке `server/` — MCP сервер для Claude/GPT:

```bash
pip install mcp requests
python server/server.py
```

## Лицензия

MIT
