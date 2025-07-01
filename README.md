# meteo
</br>LATVIJAS VIDES, ĢEOLOĢIJAS UN METEOROLOĢIJAS CENTRS (videscentrs.lvgmc.lv) datu parsers, ar docker konteinera stdout izvadi un html datnes izveidi ./output mapē.
</br>(modificējama, esošās, Saldus, atrašanās vieta, pēc nosaukuma - https://videscentrs.lvgmc.lv/karte)  
</br>Startējas divos veidos:
</br>1.
</br>docker build -t weather-scraper .
</br>docker run --rm weather-scraper
</br>2.
</br>docker-compose up --build
</br>vēlāk var:
</br>docker-compose up -d
</br>docker-compose logs -t -f
