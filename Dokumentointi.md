Dokumentointi:

Grafiikat priorisointi järjestys:
1. Pelihahmo
2. Alustat (perusalusta, yhden pompun kestävä, liikkuva,    "ansa-aslusta")
3. Tausta
4. "Musta-aukko" tmv. eli ilmassa paikallaan oleva kohta josta hahmo kuolee, ei voi tuhota-
5. Hirviöt
6. Pelihahmon aseen panos

Vaatimus ideoita

UI Vaatimuksia
- Peli
- Menu, Pelissä voi päästä menuun painamalla yhtä nappia.
- Molemmat hiiri ja näppäimistö toimivat, eli ukkelilla voi liikkua nuolinäppäimillä ja 
- Kauppa, josta voi ostaa pelissä kerätyllä rahalla esim kehitysominaisuuksia, liikkuu nopeampaa jne. 
- Selkeät siirtymiset

Logiikka vaatimuksia
- Peli vaikeutuu mitä korkeammalle mennään, esiintyy esimerkiksi enemmän hirviöitä ja erilaisia alustoja, taikka alustoja on harvemmin ja vähemmän. Kuitenkin siten, että peli on mahdollinen. (Eli alustat eivät ole liian kaukana toisistaan, sekä hirviön alla on alusta joka ei mene rikki jotta taisteluun voi käyttää aikaa)

- Pelissä generoituu korkeus huomioiden satunnaisesti erilaisia alustoja, hirviöitä ja pelihahmoa auttavia väliaikaisia boosteja 

- Rahaa spawnaa ikkunaan, sitä voi kerätä ja oman rahan näkee ylänurkasta että paljonko sitä on.

- Pelihahmo hyppii automaattisesti (kun tulee maakontakti, tapahtuu välittömästi uusi hyppy)

- Pelireunat tulee määrittää, ettei pelihahmo häviä peli-ikkunasta. Pelireunan voi kuitenkin ylittää, jolloin hahmo ilmestyy toiselle puolelle peli-ikkunaa

Alustat:
    - Normaali alusta
    - Rikki menevä alusta (kestää 1 hypyn)
    - Ansa-alusta (ei kestä yhtään hyppyä)
    - Liikkuva alusta

Boostit:
    - Superhyppy (osuessa pelaaja hyppää paljon korkeammalle)
    - Hyppykengät (osuessa pelaaja saa käyttöönsä kengät, joilla voi hyppyiä korkemmalle esim. 10 kertaa)
    - Rakettireppu (Pelaaja lentää kovaa vauhtia tietyn ajan ylöspäin)
    - Sateenvarjo (pelaajan tippuu hitaammin tietyn ajan)

Hirviöt:
    - Paikallaan olevia hirviöitä
    - Sivusuunnassa liikkuvia hirviöitä
    - Muutama eri hirviö (esim pieni, leveä, korkea)
    - Kestää yhden tai useamman osuman (vaikeutuu korkeuden kasvaessa)

Toiminnallisia vaatimuksia:

- Suoritettaessa peliohjelma, peli käynnistyy päävalikkoon. Päävalikossa on 2 nappia "Aloita peli" ja "Asetukset".

- Pelin voi aloittaa "Aloita peli" painikkeesta, jonka jälkeen siirrytään pelisceneen.

- Hahmoa voi pelissä liikuttaa vasemmalle ja oikealle näppäimillä (a & d / nuolivasen & nuoli oikea)

- Hahmo ampuu välilyönti näppäimellä. Panokset lentävät hahmosta suoraan ylöspäin

- Mikäli panos osuu hirviöön, hirviö kuolee ja häviää peliruudusta. Pelissä voi ilmaantua hirviöitä, jotka vaativat useampia osumia.

- Peli pitää voida laittaa tauolle oikeassa yläreunassa olevasta "Pause" napista. Taukovalikossa on kolme nappia, yhdellä voi jatkaa peliä, toisella avata asetusmenun ja kolmannella palata pelin päävalikkoon.

- Voi avata asetusmenun taukovalikon tai päävalikon kautta nappia painamalla. Asetusmenussa voit säätää seuraavia asetuksia:
    - Äänen voimakkuus (liukukytkin 1-10)
    - Musiikin voimakkuus (liukukytkin 1-10) 

Ei toiminnallisia vaatimuksia:

- Peli toimii samalla lailla eri laitteilla (esim. hidas ja nopea tietokone)

- Peli on kieleltään englanniksi

- Pelissä saavutetut ennätykset tallennetaan tietokantaan. Tietokantaan tallennetaan top 5 ennätystä, mikäli pelissä saavuttaa suuremman arvon kuin jo olemassa oleva top5, uusi ennätys ylikirjoitetaan oikeaan kohtaan. 

- Tietokantaa ei pidä päästä muuttamaan itse. Kun peli on ohi, peli tarkastaa onko saavutettu maksimikorkeus suurempi kuin tietokannassa olevat ennätykset, mikäli on, pelaaja voi antaa nimimerkin ja tieto ylikirjoitetaan tietokantaan HTTP POST pyynnöllä.