# Сайт ARVIOM Engineering

Статичний сайт: HTML-сторінки + дані. Збирається скриптом, без CMS.

## Як змінити вміст
- **Кейси, розробки, команда, логотипи** — `content/home.json`, потім `python3 build/build.py`.
- **Каталог IoT (сторінка «Продукти»)** — `content/catalog/*.json`, назви українською — `build/uk.py`.
- **Сторінки серій** (`s-*.html`, `catalog.html` = EM300): склад — `content/catalog/sensor_series.json` та `iot_catalog.json`, характеристики — `content/catalog/specs.json` (витягнуті з даташитів скриптом `build/specs.py`), вигляд — `build/series_tpl.html`, налаштування серій — `build/gen_series.py`. Серія EM300 — дані в `data.js`.
- **Рішення** (`solutions.html`, `sol-*.html`) — тексти в `content/solutions.json`, вигляд — `build/solutions_tpl.html`.
- **Тексти й вигляд сторінок** — `build/index_tpl.html`, `build/products_tpl.html`, `partner.html`.

Після зміни: `python3 build/build.py` → згенеруються `index.html`, `products.html`, `catalog.html`, `s-*.html`.

## Фото
- `img/` — рендери й скриншоти, `img/ms/` — матеріали з milesight.com, `img/cat/` — фото каталогу Milesight.

## Історія й відкат
Кожна зміна — коміт у git. Відкотити: `git log`, потім `git revert <коміт>`.
