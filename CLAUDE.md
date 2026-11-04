# Сайт ARVIOM Engineering — правила роботи

- Сайт статичний. Сторінки `index.html`, `products.html`, `catalog.html`, `s-*.html`, `solutions.html`, `sol-*.html`, `vprovadzhennia.html`, `case-*.html`, `zakhyst.html`, `news.html` генеруються: після змін у `content/`, `build/*_tpl.html`, `data.js` запускати `python3 build/build.py` і комітити результат разом із джерелами.
- Мова сайту — українська. Шрифт — тільки Inter Tight. Стиль — за зразком milesight.com.
- Гілка `main` автоматично потрапляє на сервер (cron раз на хвилину, `/opt/iot-stack/eng-pull.sh`). Не пушити неперевірене: спершу відкрити сторінки локально.
- Матеріали Milesight (фото, кейси) — з позначкою «Джерело: Milesight».
- Кейси Milesight: імпорт `build/import_cases.py <dir>` (вихід конвеєра /root/gd/cases/casepipe.py). Картинка для плашки — превью зі списку milesight.com (`build/ms_cards.py`, викликається автоматично), не фото зі сторінки кейсу. Абстрактні фони без змісту не показувати, прозорі PNG — на білому.
- Сторінка кейсу генерується `build/gen_cases_v2.py` (стиль milesight.com/success-stories/iot-non-invasive-electricity-monitoring-solution-in-europe у нашому фірмовому стилі); старий `case_page` у gen_cases.py не використовується.
- Новини: `content/news.json` (date, tag, title, image, link). Головна показує 4 останні, `news.html` — усі.
- Форма на головній (#contact) шле POST JSON на n8n-вебхук https://n8n.arviom.com.ua/webhook/eng-lead (workflow «ENG site — заявка з форми», id 1VSgERxGGnzjptdi) → Telegram Максиму. Поле website — honeypot.
- SEO/favicon: `build/seo.py` (останній крок build) додає в усі сторінки robots, description, canonical, favicon, Open Graph. Налаштування і перевизначення для окремих сторінок — `content/site.json` (url, noindex, pages). При переїзді на бойовий домен: змінити `url`, поставити `noindex: false`, зібрати.
