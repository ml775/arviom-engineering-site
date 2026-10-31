# Сайт ARVIOM Engineering

Статичний сайт: HTML-сторінки + дані. Збирається скриптом, без CMS.

## Як змінити вміст
- **Кейси, розробки, команда, логотипи** — `content/home.json`, потім `python3 build/build.py`.
- **Каталог IoT (сторінка «Продукти»)** — `content/catalog/*.json`, назви українською — `build/uk.py`.
- **Серія EM300 (каталог з порівнянням)** — `data.js` (дані), `catalog_tpl.html` (вигляд).
- **Тексти й вигляд сторінок** — `build/index_tpl.html`, `build/products_tpl.html`, `partner.html`.

Після зміни: `python3 build/build.py` → згенеруються `index.html`, `products.html`, `catalog.html`.

## Фото
- `img/` — рендери й скриншоти, `img/ms/` — матеріали з milesight.com, `img/cat/` — фото каталогу Milesight.

## Історія й відкат
Кожна зміна — коміт у git. Відкотити: `git log`, потім `git revert <коміт>`.
