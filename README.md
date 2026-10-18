# LocalTube

Eine kleine, responsive und datensparsame Weboberfläche für persönliche Medien-Workflows.

## GitHub Pages aktivieren

1. Öffne **Settings → Pages** in diesem Repository.
2. Wähle unter **Build and deployment** die Quelle **Deploy from a branch**.
3. Wähle den Branch `main` und den Ordner `/(root)`, danach **Save**.
4. Warte, bis GitHub Pages die Website veröffentlicht hat.

## Was diese Version bereits kann

- Responsive Darstellung für Desktop, Tablet und Smartphone
- Eingabe und einfache Prüfung einer URL
- MP3/MP4- sowie Einzelvideo/Playlist-Auswahl in der Oberfläche
- Einfügen eines Links aus der Zwischenablage, sofern der Browser es erlaubt
- Kein eingebautes Analyse- oder Werbetracking
- Keine Übertragung eingegebener Links an einen zusätzlichen Download-Anbieter durch diese Oberfläche

## Wichtige Einschränkung

**Diese GitHub-Pages-Version lädt noch keine Videos oder Audiodateien herunter.** GitHub Pages hostet statische Dateien und führt keinen lokalen Python-Dienst aus. Der Download-Button bestätigt derzeit nur die gewählten Optionen. Es gibt absichtlich keine Umgehung technischer Schutzmaßnahmen.

Wenn eine lokale Verarbeitung ergänzt wird, muss dafür ein separat installierter Dienst auf dem eigenen Gerät laufen. Dieser sollte standardmäßig nur an localhost gebunden sein, einen zufälligen Zugriffstoken verlangen, nur erwartete Anfragen annehmen und nicht direkt aus dem öffentlichen Internet erreichbar sein. Eine Website auf GitHub Pages kann nicht ohne Weiteres sicher auf einen solchen Dienst zugreifen: Browser-Mixed-Content-, CORS- und Private-Network-Regeln müssen korrekt berücksichtigt werden. Für Nutzung von unterwegs ist zusätzlich eine sichere private Netzwerkverbindung erforderlich; keinen unauthentifizierten Port ins Internet weiterleiten.

## Rechtmäßige Nutzung

Verwende das Werkzeug nur für Inhalte, die du selbst erstellt hast, für die du die erforderlichen Rechte/Erlaubnis hast oder die du nach geltendem Recht herunterladen darfst. Privater Gebrauch allein garantiert nicht, dass jede Kopie zulässig ist. Beachte die Bedingungen des jeweiligen Dienstes und umgehe keine technischen Schutzmaßnahmen.

## Datenschutz

Die Oberfläche speichert URLs nicht dauerhaft und sendet sie nicht an einen Download-Service. GitHub Pages selbst wird weiterhin von GitHub gehostet, und der Browser ruft für den Seitenaufruf Dateien von GitHub ab. Die Stylesheet-Datei lädt außerdem optionale Schriftarten von Google Fonts. Falls auch diese Drittanbieter-Anfrage vermieden werden soll, entferne den `@import` in `style.css`; die Seite verwendet danach Systemschriften.
