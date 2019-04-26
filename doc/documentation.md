---
title: SWT Skiapoden Testing Dokumentation
---

![Entwicklungs-Team beim Testen](./img/testen.jpg)

# Skiapoden
Microservice für das Wikipedia-Philosophiespiel

1. Wählen Sie einen (zufälligen) Wikipedia-Artikel aus.
2. Klicken Sie auf den ersten Link zu einem anderen Artikel.
3. Zählen Sie die «Hopfen», um den Artikel Philosophie zu erreichen.

Dieser Microservice hilft Ihnen, das Spiel automatisch zu spielen.

Die Annahmen, was der erste Link eines Artikels ist, sind:

1. Der Link befindet sich innerhalb eines Artikelabsatzes.
2. Der Link steht nicht in Klammern oder Klammern.
3. Der Link enthält keinen Anker (#).
4. Der Link verweist nicht auf eine Datei (File: ...)
5. Der Link hat die Form / wiki / ...
6. Die Verknüpfung befindet sich nicht in einer Tabelle oder Box.

Von den Links, die diese Bedingungen erfüllen, wird der erste ausgewählt.

## Anleitung
Erstellen Sie zunächst eine CSV-Datei ohne Spaltenüberschriften mit diesen Spalten:

- Wikipedia Sprache: de, en, fr usw.
- Quellartikel: Weihnachten, Kebab, Mexiko usw.
- Zielartikel: Philosophie für unseren Anwendungsfall, aber alles andere gilt auch.
- Erwartete Hops vom Quell- zum Zielartikel: 7 ist das Ziel, aber jede positive Zahl geht.

Zum Beispiel:

```
de,Tatsache,Philosophie,7
en,Cheese,Philosophy,7
fr,Langue,Philosophie,7
ru,Достопримечательность,Философия,7
de,Zürich,Philosophie,7
en,Pig,Philosophy,7
fr,Gridley_(Iowa),Philosophie,7
ru,Наука,Философия,7
de,Zwillingsparadoxon,Philosophie,7
fr,Journalisme,Philosophie,7
ru,Афины,Философия,7
de,Käse,Philosophie,7
en,Competition,Philosophy,7
fr,Agriculture_du_Tarn,Philosophie,7
ru,Университет,Философия,7
```
Zweitens wählen Sie im Online-Formular für die Testübermittlung die so erstellte Datei für den Upload aus.

Drittens entscheiden Sie sich für die Hops-Grenze, d.H. nach wie vielen Klicks zum nächsten Artikel-Link, ohne den Zielartikel zu finden, falls der Prozess für den aktuellen Testfall (nicht die gesamte Testserie) angehalten wird.

Viertens senden Sie das Formular, um die Tests zu starten.

Fünftens warten Sie, bis der erstellte Bericht zum Download bereit ist.

Der erstellte Bericht enthält die gleichen Spalten wie die hochgeladene CSV-Datei sowie die folgenden Spalten:

1. Die ermittelte Sprungzahl, wie viele Verknüpfungen tatsächlich verfolgt werden mussten, um den Zielartikel zu erreichen, oder -1 im Fehlerfall.
2. Eine Nachricht mit folgendem Hinweis:
    - `success`: erwartete Sprungzahl = ermittelte Sprungzahl
    - `failure`: erwartete Sprungzahl ≠ ermittelte Sprungzahl
    - `[error message]`: Schleife erkannt, erster Link nicht gefunden usw.

## Online Formular
Das Online Formular ist unter diesem Link zu finden: [hier geht's zum Online Formular](http://skiapoden.herokuapp.com/)

![submission form](./img/formular.png)

## API Endpoints

### `/csv`
Dieser Endpunkt akzeptiert eine CSV-Liste mit Testfällen, die die Wikipedia-Sprache, den Quell- und Zielartikel sowie die erwartete Anzahl von Hops enthält, die zum Erreichen des Zielartikels erforderlich sind:i

```
de,Bier,Philosophie,14
en,Beer,Philosophy,12
fr,Bière,Philosophie,11
ru,Пиво,Философия,7
```

Der Endpunkt wird wie folgt aufgerufen. Stellen Sie sicher, dass Sie die Option `--data-binary` verwenden, um die Zeilenumbrüche in der CSV beizubehalten:

`curl -X POST https://skiapoden.herokuapp.com/csv --data-binary @tests.csv`

Es wird eine CSV-Liste zurückgegeben, die die Anzahl der tatsächlich benötigten Sprünge angibt. Das Ergebnis des Tests wird als «Erfolg» (erwartete und tatsächliche Sprüngezahl ist gleich), «Ausfall» (sonst) oder die Fehlermeldung angezeigt, falls etwas schiefgelaufen ist:

```
de,Bier,Philosophie,14,14,success
en,Beer,Philosophy,12,18,failure
fr,Bière,Philosophie,11,11,success
ru,Пиво,Философия,7,18,failure
```

### `/hopcount`
Dieser Endpunkt akzeptiert eine JSON-Struktur von Testfällen, führt diese aus und gibt einen JSON-Bericht mit Testergebnissen zurück. Verwendungszweck:

`curl -X POST https://skiapoden.herokuapp.com/hopcount -d @hopcount.json`

Mit der Eingabe `hopcount.json` sieht das so aus:

```
[
  {
    "lang": "de",
    "source": "Medizin",
    "target": "Philosophie",
    "expected": 7
  },
  {
    "lang": "en",
    "source": "Competition",
    "target": "Philosophie",
    "expected": 7
  },
  {
    "lang": "fr",
    "source": "Pigeon",
    "target": "Philosophie",
    "expected": 7
  },
  {
    "lang": "ru",
    "source": "Достопримечательность",
    "target": "Философия",
    "expected": 7
  }
]
```

Und der Bericht kommt so zurück:

```
[
  {
    "lang": "de",
    "source": "Medizin",
    "target": "Philosophie",
    "expected": 7,
    "actual": 7,
    "result": "success"
  },
  {
    "lang": "en",
    "source": "Competition",
    "target": "Philosophie",
    "expected": 7,
    "actual": -1,
    "result": "error: unable to extract first link of https://en.wikipedia.org/wiki/Entity"
  },
  {
    "lang": "fr",
    "source": "Pigeon",
    "target": "Philosophie",
    "expected": 7,
    "actual": 6,
    "result": "failure"
  },
  {
    "lang": "ru",
    "source": "Достопримечательность",
    "target": "Философия",
    "expected": 7,
    "actual": 18,
    "result": "failure"
  }
]
```

### `/firstlink`
Dieser Endpunkt extrahiert den ersten Artikellink eines Wikipedia-Artikels.

Es akzeptiert eine JSON-Struktur, die die Wikipedia-Sprache enthält, und enthält folgenden Artikel:

```
{
    "language": "en",
    "article": "ACME"
}
```

Der Dienst kann auf dem /firstlink-Endpunkt mit der POST-Methode aufgerufe werden:

`$ curl -X POST https://skiapoden.herokuapp.com/firstlink -d '{ "language": "en", "article": "Heroku" }'`

Die Antwort wird eine JSON-Struktur sein:

```
{
    "firstLink": "https://en.wikipedia.org/wiki/Platform_as_a_service"
}
```

© 2019 by the [Skiapoden](https://github.com/skiapoden/) team, using the [firstlink](https://github.com/patrickbucher/firstlink) module and [Go](https://golang.org/).

## Coole Begriffe (Glossar)
- Microservice: Microservices sind ein Architekturmuster der Informationstechnik, bei dem komplexe Anwendungssoftware aus unabhängigen Prozessen komponiert wird, die untereinander mit sprachunabhängigen Programmierschnittstellen kommunizieren.
- API Endpoints: Endpoints are important aspects of interacting with server-side web APIs, as they specify where resources lie that can be accessed by third party software. Usually the access is via a URI to which HTTP requests are posted, and from which the response is thus expected.
- Hops: Sprünge von einem Wikipedia-Link zum nächsten.
- JSON: Die JavaScript Object Notation, kurz JSON, ist ein kompaktes Datenformat in einer einfach lesbaren Textform zum Zweck des Datenaustauschs zwischen Anwendungen.
- Skiapoden: Skiapoden, auch Skiapodes, Schattenfüßler oder Schattenfüßer sind Fabelwesen von menschlicher Gestalt, aber mit nur einem Bein. Mit diesem sollen sie blitzschnell laufen können. Ihren riesigen Fuß halten sie beim Liegen als Sonnenschutz über sich. 
