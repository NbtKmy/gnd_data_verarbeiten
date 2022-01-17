# GND-Daten Verarbeiten

Wie Lobid (https://lobid.org/gnd/api) zeigt, kann man die GND-Daten über den API-Schnittstelle holen und verarbeiten. 

Hier in diesem Repo zeige ich meinen Versuch - zuerst hole ich die GND-Daten durch Bulk-Download. Dannach habe ich mit Python die beliebige Information aus der GND-Datei geholt und daraus eine CSV-Tabelle erstellt.

## Requirements
- Python vers. 3
- Pandas

## Schritt 1 - Bulk-Download

Zuerst sollte man überlegen, welche Datei man von der GND abzapfen möchte.
Ich wollte bsplw. die Personen-Daten aus der GND haben, die in den 1850er geboren sind und derer Todesjahre unbekannt sind.
Nach dem eigenen Bedarf soll man die Query formulieren:

```
https://lobid.org/gnd/search?q=dateOfBirth:185* NOT dateOfDeath:*&filter=type:DifferentiatedPerson&format=json
```
Diese Query gibt 8606 Treffer zurück (Stand: 17.01.2022).
Die Menge finde ich okay. 
Aufgrund dessen habe ich Bulk-Download über meiner Terminal ausgeführt:

```
curl --header "Accept-Encoding: gzip" 'https://lobid.org/gnd/search?q=dateOfBirth:185*%20NOT%20dateOfDeath:*&filter=type:DifferentiatedPerson&format=jsonl' -o 'gnd_geb185x.txt.gz'
```

Nach der Ausführung findet man die Bulk-Datei in GZIP-Format.

## Schritt 2 - Datenverarbeiten

Wenn man die GZIP-Datei gekriegt hat, kann man sie danach leicht mit Python verarbeiten. 
Als Beispiel habe ich hier eine Python-Code geschrieben.
Für die Ausführung dieser Code braucht man Python version 3 und Pandas. 

```
python gnd_botsunen.py -i gnd_geb185x -o test
```

oder

```
python3 gnd_botsunen.py -i gnd_geb185x -o test
```
Daraus entstand die 'test.csv'-Datei in diesem Repo.

