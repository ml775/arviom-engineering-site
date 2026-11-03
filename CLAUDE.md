# Сайт ARVIOM Engineering — правила роботи

- Сайт статичний. Сторінки `index.html`, `products.html`, `catalog.html`, `s-*.html`, `solutions.html`, `sol-*.html` генеруються: після змін у `content/`, `build/*_tpl.html`, `data.js` запускати `python3 build/build.py` і комітити результат разом із джерелами.
- Мова сайту — українська. Шрифт — тільки Inter Tight. Стиль — за зразком milesight.com.
- Гілка `main` автоматично потрапляє на сервер (cron раз на хвилину, `/opt/iot-stack/eng-pull.sh`). Не пушити неперевірене: спершу відкрити сторінки локально.
- Матеріали Milesight (фото, кейси) — з позначкою «Джерело: Milesight».
- Кейси Milesight: імпорт `build/import_cases.py <dir>` (вихід конвеєра /root/gd/cases/casepipe.py). Картинка для плашки — превью зі списку milesight.com (`build/ms_cards.py`, викликається автоматично), не фото зі сторінки кейсу. Абстрактні фони без змісту не показувати, прозорі PNG — на білому.
- Сторінка кейсу генерується `build/gen_cases_v2.py` (стиль milesight.com/success-stories/iot-non-invasive-electricity-monitoring-solution-in-europe у нашому фірмовому стилі); старий `case_page` у gen_cases.py не використовується.
