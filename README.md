# meteo
LATVIJAS VIDES, ĢEOLOĢIJAS UN METEOROLOĢIJAS CENTRS (videscentrs.lvgmc.lv) parsers, ar dokcer stdout izvadi un html izveidi
<p>
 Startējas divos veidos:
</p>
</br>
1.
nano scraper.py
docker build -t weather-scraper .
docker run --rm weather-scraper

2.
docker-compose up --build

vēlāk var:
docker-compose up -d
docker-compose logs -t -f
