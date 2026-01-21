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
- Kasvava haaste, eli peli vaikeutuu mitä korkeammalle mennään, esiintyy esimerkiksi enemmän hirviöitä ja rikkoutuvia alustoja taikka alustoja on harvemmin ja vähemmän.
- Korkeus
- Rahaa spawnaa ikkunaan, sitä voi kerätä ja oman rahan näkee ylänurkasta että paljonko sitä on.
- Reilu peli / ei mahdoton
- Hyppiminen selkeää
- Ulkoreunat

Toiminnallisia vaatimuksia:

- Suoritettaessa peliohjelma, peli käynnistyy päävalikkoon. Päävalikossa on 2 nappia "Aloita peli" ja "Asetukset".

- Pelin voi aloittaa "Aloita peli" painikkeesta, jonka jälkeen siirrytään pelisceneen.

- Hahmoa voi pelissä liikuttaa vasemmalle ja oikealle näppäimillä (a & d / nuolivasen & nuoli oikea)

- Pelihahmo hyppii automaattisesti jatkuvasti (kun tulee maakontakti, tapahtuu välittömästi uusi hyppy)

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


