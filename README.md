# FlavorFunk-Bestellsystem
Eine Anwendung im Rahmen unserer Projektarbeit
Diese Anwendung dient als Bestell-/Bezahlsystem für das Restaurant "Golden Seagull"



**Starten der Anwendung**
->  Öffne das Windows Powershell Terminal (oder Terminal deiner Wahl) aus dem Ordner heraus, in dem du diese Dateien gespeichert hast.
->  Führe im Terminal folgende Codezeile aus: streamlit run flavorfunk.py.
    (stelle sicher, dass du dich in der richtigen Umgebung, in der Streamlit installiert ist, befindest)
->  Bestätige mit der Enter-Taste, um zur Streamlit Anwendung weitergeleitet zu werden



**Benutzung der Anwendung**
Zuerst sieht man die Speisekarte, auf dieser sieht man die ganzen Speisen und Getränke, die das Restaurant "Golden Seagull" führt.
Links ist eine Sidebar, in der sich ein Dropdown Menü befindet, womit man durch die Seiten navigieren kann:

*Speisekarte anzeigen*          Anzeige der Speisekarte Golden Seagull

*Neue Bestellung erstellen*     Hier kann man Artikel zu einem Tisch bestellen. Zuerst wählt man den Tisch aus dem Dropdown Menü aus.
                                Dann wählt man Artikel und Menge aus (die Menge kann über '- / +' verringert/erhöht werden, oder auch direkt eingetragen).
                                Es ist auch möglich Zusatzinfos hinzuzufügen, um beispielsweise besondere Kundenwünsche anzugeben, oder genauere Infos zu einem Artikel zu geben 
                                (bsp.: bei Softdrinks als Zusatzinfo: Cola/Fanta/Sprite etc.)

*Bestellungen anzeigen*         Hier kann man die Bestellungen an den Tischen einsehen. Zu sehen sind die nötigsten Infos für Servicekraft/ Koch/ Barkeeper.
                                Hier kann die Servicekraft auch einzelne Artikel, stornieren. Der Status wird bei Neuauswahl des Tisches aktualisiert.

*Bestellung bezahlen*           Hier kann man die Bestellungen bezahlen. Dazu wählt man erst einen Tisch mit offenen Bestellungen. Daraufhin werden alle bestellten Artikel dort
                                aufgelistet und deren Gesamtsumme berechnet. Kurzgesagt - eine Rechnung wird erstellt. Daraufhin kann man entscheiden welche Bezahlmethode man anwenden möchte, und ob man
                                Trinkgeld geben will. Nach Bestätigung, wird die bezahlte Summe (inclusive Trinkgeld) angezeigt, und die Artikel wechseln ihren Status auf 'bezahlt'



**Anmerkung**
Beachte, dass diese Version noch eine Beta-Version ist, bei der noch weitere Funktionen angepasst und optimiert werden.
Geplante Anpassungen für zukünftige Patches sind:

->  Automatische Aktualisierung der Bestellliste nach einer Stornierung
->  Hinterlegung der Rechnungen nach einer Bezahlung. Dabei sollten die Rechnungen in einer Datei abgelegt werden und jederzeit aufrufbar sein.
->  Die Bestellliste eines Tisches, soll nach Bezahlung und Hinterlegung der Rechnung, zurückgesetzt werden. Dies soll zur besseren Übersicht dienen.


**Nachwort**
Wir bedanken uns, für dein Vertrauen in unsere Arbeit und hoffen, dass diese dir gefällt.
Mit freundlichen Grüßen
Euer Dev-Team
Miguel Kliem (miguelkliem91), Maik Schweizer (schweizer90) und Malcom Abimbola (MegatronxX93)
