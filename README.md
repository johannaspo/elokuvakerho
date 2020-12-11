# elokuvakerho

Huitsin Nevadan yliopiston elokuvakerhon perinteikkääseen toimintaan kuuluu keskeisesti kerhon kirjastosta löytyvien elokuvien lainaus ja arvostelu. Elokuvakerho on nyt siirtynyt digiaikaan, joten sille on perustettu omat nettisivut. Uuden sivuston toiminnallisuudet on listattu tässä.

Kirjauduttuaan sivustolle jäsenet voivat:
-	selata kerhon elokuvakokoelmaa
-	lukea jokaisen elokuvan omalta sivulta elokuvan nimen, genren, julkaisuvuoden, kuvauksen, lainaustilanteen sekä mahdolliset arvostelut
-	kirjoittaa arvosteluja elokuville
-	lainata elokuvia (elokuvan voi hakea kerhohuoneesta lainausilmoitusta seuraavana päivänä)

Lisäksi sivuston ylläpitäjät voivat:
-	lisätä jäseniä kerhoon
-	lisätä elokuvia kokoelmaan
-	tarkastella mitkä elokuvat ovat lainassa ja kenellä
-	merkata lainatun elokuvan palautetuksi

## Lopullinen palautus ##

Sovellusta pääsee edelleen testaamaan adminina (tunnus ja salasana admin) tai tavallisena jäsenenä (tunnus ja salasana jasen) osoitteessa https://elokuvakerho.herokuapp.com/. 

Tavallinen jäsen voi selata elokuvavalikoimaa, katsella elokuvan tietoja, lukea ja kirjoittaa arvosteluja (myös pelkön tähtiarvosanan antaminen on mahdollista) sekä lainata elokuvia. Lisäksi on mahdollista katsella toisten jäsenten sivuja, joilta löytyy nyt myös linkit kyseisen jäsenen kirjoittamiin arvosteluihin. Tavallinen jäsen voi löytää toisen jäsenen sivun vain elokuva-arvosteluista, joissa on linkki arvostelijan sivulle. Admin-käyttäjät näkevät admin-sivuilta jäsenlistauksen kokonaisuudessaan.

Admin-käyttäjät voivat admin-sivujen kautta myös lisätä kerhoon uusia jäseniä, lisätä uusia elokuvia kokoelmaan ja tarkastella, mitkä elokuvat ovat lainassa sekä merkata niitä palautetuiksi. Tässä versiossa on muokattu elokuvan lisäämistä niin, että genret löytyvät valmiiksi lomakkeen genre-valikosta. Genreille on myös nyt oma taulunsa tietokannassa. Sovellusta on mahdollista jatkokehittää niin, että elokuville voisi halutessaan lisätä useamman genren.