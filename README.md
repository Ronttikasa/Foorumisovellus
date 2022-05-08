# Foorumisovellus

Sovellus on keskustelualue, joka koostuu huoneista joissa on viesteistä koostuvia keskusteluketjuja. Käyttäjät ovat joko peruskäyttäjiä tai ylläpitäjiä.

Sovellus on testattavissa [Herokussa](https://glc-foorumi.herokuapp.com/).

Sovellukseen voi luoda uuden peruskäyttäjän testausta varten, ylläpitäjätoimintoja voi testata tunnuksilla `testiadmin`/`admin321`

## Loppupalautus

Uudet ominaisuudet:
- Ylläpitäjä voi poistaa keskusteluketjun
- Ylläpitäjä voi poistaa kenen tahansa kirjoittaman viestin
- Tyylitelty ulkoasu

## Sovelluksen toteutetut ominaisuudet

- Käyttäjä voi luoda uuden tunnuksen
- Käyttäjä voi kirjautua sisään ja ulos.
- Käyttäjä voi lukea muiden viestejä ja kirjoittaa uusia viestejä
- Käyttäjä näkee etusivulla listan huoneista
- Käyttäjä voi aloittaa uuden keskusteluketjun tai kirjoittaa viestin olemassaolevaan ketjuun
- Käyttäjä voi poistaa itse kirjoittamansa viestin
- Ylläpitäjä voi luoda uusia huoneita
- Ylläpitäjä voi luoda vain ylläpitäjille näkyvän huoneen
- Ylläpitäjä voi poistaa keskusteluketjun
- Ylläpitäjä voi poistaa kenen tahansa kirjoittaman viestin

## Sovelluksen käyttöönotto kehitysympäristössä

- Asenna PostgreSQL ja luo uusi tietokanta
- Kloonaa repositorio ja luo hakemistoon virtuaaliympäristö komennolla `python3 -m venv venv`
- Käynnistä virtuaaliympäristö `source venv/bin/activate`
- Asenna riippuvuudet komennolla `pip install -r requirements.txt`
- Luo juurihakemistoon tiedosto *.env* ja kopioi sinne tiedoston [*.env.template*](https://github.com/Ronttikasa/foorumisovellus/blob/main/.env.template) sisältö. Aseta .env-tiedostossa muuttujaan DATABASE_URL käyttämäsi tietokannan osoite ja muuttujaan SECRET_KEY oma salainen avaimesi.

Salaisen avaimen luominen onnistuu esim. Python-tulkissa komennoilla
``` python
import secrets
secrets.token_hex(16)
```
- Alusta tietokanta komennolla `psql DATABASE_NAME < schema.sql`
- Käynnistä sovellus komennolla `flask run`


## Jatkokehitysideoita

- Käyttäjä näkee etusivulla tietoja kustakin alueesta, esim viestien yhteismäärä, viimeisimmän viestin ajankohta
- Käyttäjä voi muokata omaa viestiään
- Käyttäjä voi etsiä kaikki viestit jotka sisältävät tietyn sanan, tai jotka on kirjoittanut tietty käyttäjä.
- Käyttäjä voi lähettää yksityisviestin toiselle käyttäjälle
- Ylläpitäjä voi poistaa huoneita
- Ylläpitäjä voi muokata kenen tahansa kirjoittamaa viestiä
- Ylläpitäjä voi bännätä käyttäjän
- Ylläpitäjä voi määritellä käyttäjäryhmiä ja esim. luoda tietylle ryhmälle näkyvän huoneen
