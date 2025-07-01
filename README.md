# meteo
LATVIJAS VIDES, ĢEOLOĢIJAS UN METEOROLOĢIJAS CENTRS (videscentrs.lvgmc.lv) parsers, ar dokcer stdout izvadi un html izveidi
<p>
 Startējas divos veidos:
</p>
</br>1.
</br>nano scraper.py
</br>docker build -t weather-scraper .
</br>docker run --rm weather-scraper
</br>2.
</br>docker-compose up --build
</br>vēlāk var:
</br>docker-compose up -d
</br>docker-compose logs -t -f
