# Сайт ARVIOM Engineering — правила роботи

- Сайт статичний. Сторінки `index.html`, `products.html`, `catalog.html` генеруються: після змін у `content/`, `build/*_tpl.html`, `catalog_tpl.html`, `data.js` запускати `python3 build/build.py` і комітити результат разом із джерелами.
- Мова сайту — українська. Шрифт — тільки Inter Tight. Стиль — за зразком milesight.com.
- Гілка `main` автоматично потрапляє на сервер (cron раз на хвилину, `/opt/iot-stack/eng-pull.sh`). Не пушити неперевірене: спершу відкрити сторінки локально.
- Матеріали Milesight (фото, кейси) — з позначкою «Джерело: Milesight».
