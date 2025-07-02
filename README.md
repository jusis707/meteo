# meteo
</br>LATVIJAS VIDES, ĢEOLOĢIJAS UN METEOROLOĢIJAS CENTRS (videscentrs.lvgmc.lv) datu parsers, ar docker konteinera stdout izvadi un html datnes izveidi ./output mapē.
</br>(modificējama, esošās, Saldus, atrašanās vieta, pēc nosaukuma - https://videscentrs.lvgmc.lv/karte)  
</br>Uzstādīšana:
</br>git clone https://github.com/jusis707/meteo
</br> cd meteo
</br>Pēc izvēles, zemāk, divi veidi:
</br>1.
</br>docker build -t weather-scraper .
</br>docker run --rm weather-scraper
</br>skatamies output terminālī
</br>papildus, izveidojas 'html' datne, mapē: ./output
</br>2.
</br>docker-compose up --build
</br>vēlāk var:
</br>docker-compose up -d
</br>docker-compose logs -t -f
</br>skatamies output
</br>papildus, izveidojas 'html' datne, mapē: ./output
</br>Mapē 'versija-ar-meteogrammu', papildus, pievienota meteogrammas attēls.
</br>
</br>
</br>
