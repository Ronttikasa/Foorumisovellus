# Foorumisovellus

Sovellus on keskustelualue, joka koostuu huoneista joissa on viesteistä koostuvia keskusteluketjuja. Käyttäjät ovat joko peruskäyttäjiä tai ylläpitäjiä.

## Välipalautus 3

Toteutetut ominaisuudet:
- Käyttäjä näkee etusivulla listan huoneista
- Käyttäjä voi aloittaa uuden keskusteluketjun tai kirjoittaa viestin olemassaolevaan ketjuun
- Käyttäjä voi lukea muiden viestejä ja kirjoittaa uusia viestejä
- Käyttäjä voi poistaa itse kirjoittamansa viestin
- Ylläpitäjä voi luoda uusia huoneita
- Ylläpitäjä voi luoda vain ylläpitäjille näkyvän huoneen

Sovellus on testattavissa [Herokussa](https://glc-foorumi.herokuapp.com/).

Sovellukseen voi luoda uuden peruskäyttäjän testausta varten, ylläpitäjätoimintoja voi testata tunnuksilla `testiadmin`/`admin321`

Tiedossa olevat puutteet:
- Sovelluksen backend ei vielä tarkista käyttäjän oikeutta katsella tiettyä huonetta/ketjua

## Backlog

Suunnitellut keskeiset toiminnot:
- [x] Käyttäjä voi luoda uuden tunnuksen sekä kirjautua sisään ja ulos.
- [x] Käyttäjä näkee etusivulla listan huoneista
- [ ] Käyttäjä näkee etusivulla kunkin huoneen viimeisimmän viestin ajankohdan.
- [x] Käyttäjä voi luoda uuden viestiketjun valitsemaansa huoneeseen.
- [x] Käyttäjä voi kirjoittaa uuden viestin viestiketjuun.
- [ ] Käyttäjä voi muokata kirjoittamaansa viestiä. 
- [x] Käyttäjä voi poistaa ~~luomansa ketjun tai~~ kirjoittamansa viestin.
- [ ] Käyttäjä voi etsiä kaikki viestit jotka sisältävät tietyn sanan, tai jotka on kirjoittanut tietty käyttäjä.
- [ ] Käyttäjä voi lähettää yksityisviestin toiselle käyttäjälle.
- [x] Ylläpitäjä voi lisätä huoneita.
- [ ] Ylläpitäjä voi poistaa huoneita.
- [ ] Ylläpitäjä voi bännätä käyttäjän.
- [ ] Ylläpitäjä voi luoda salaisen huoneen ja määrittää keillä on pääsy salaiseen huoneeseen.
- [ ] Ylläpitäjä voi muokata ja poistaa kenen tahansa luomia ketjuja ja viestejä.
