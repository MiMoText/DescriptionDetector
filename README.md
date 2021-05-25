# DescriptionDetector
Skripte zur Identifikation von Beschreibungspassagen in Texten auf Basis eines Vokabulars.

Das Projekt am besten in einem virtuellen Environment ausführen. Mit folgendem Befehl können dann alle benötigten Pakete installiert werden:\
`pip install -r requirements.txt`\
Es wird unter Anderem das franzöische spaCy-Modell **fr_core_news_sm** heruntergeladen und verwendet. Wenn gewünscht, kann dieses durch andere/größere Modelle ersetzt werden (siehe [spacy.io/models/fr](https://spacy.io/models/fr)).

### config.py
Konfigurations-Datei, welche Konstanten für Dateipfade sowie Header der TSV-Dateien enthält. Das Ändern von Headern oder Dateiepfaden kann dazu führen, dass die einzelnen Skripte nicht erwartungsgemäß funktionieren.

### vocabulaire.py
Diese Skript erstellt aus dem Vokabular, welches als CSV-Datei vorliegt eine txt-Datei, in welcher dann je Zeile eine Vokabel zu finden ist. Das Vokabular liegt ursprünglich als Excel-Datei vor und muss von Hand mithilfe von z.B. Excel in eine CSV umgewandelt werden.

Um das Vokabular zu ändern, wird empfohlen\die txt-Datei [vocabulaire.txt](https://github.com/MiMoText/DescriptionDetector/blob/main/data/vocab/vocabulaire.txt) anzupassen. Danach sollte jedoch das Skript *vocabulaire.py* **nicht** ausgeführt werden, da die txt-Datei sonst erneut überschrieben wird.

### process.py
*process.py* verarbeitet die Roman-Texte, die als txt-Dateien ([data/plain/files/](https://github.com/MiMoText/DescriptionDetector/tree/main/data/plain/files)) vorliegen zu TSV-Dateien ([data/processed/files/](https://github.com/MiMoText/DescriptionDetector/tree/main/data/processed/files)), die analysiert werden können. Dieses Skript muss nur ausgeführt werden, falls die TSV-Dateien nicht existieren. Die Ausführung kann aufgrund von NLP etwas dauern.

Jede erstellte TSV-Datei besitzt folgende Spalten:

Header | Typ | Erläuterung
---|--- | ---
`sentence nr` | `int` | Satz Nummerierung in txt-Datei 
`sentence` | `str` | Satz
`paragraph nr` | `int` | Paragraph Nummerierung in txt-Datei (getrennt durch \n)
`sentence nr in paragraph` | `int` | Satz Nummerierung im Paragraph
`words` | `int` | Anzahl der Wörter
`matches` | `int` | Anzahl der Matches mit Vokabeliste
`sentence density` | `float` | Dichte-Score (`matches` / `words`)
`vocabulary words matched` | `2d-str-list` | Auflistung der Matches

## analyze.py
Mit *analyze.py* können die TSV-Dateien analysiert werden. Dazu kann die **main**-Methode des Skripts nach Belieben angepasst werden.

Folgende Methoden stehen zur Verfügung:

#### load_data() `return df, df_no_zeros, datframes`
lädt die TSV-Dateien.
* `df`: ein DataFrame bestehend aus allen TSV-Dateien
* `df_no_zeros`: DataFrame wie `df`, nur ohne `sentence_density==0`
* `dataframes`: Dictionary von DataFrames der einzelnen TSV-Dateien, mit dem Dateinamen (ohne Endung) als Key

#### save_data(data, filepath=None, dir=None)
Speichert ein oder mehrere DataFrames ab.\
Handelt es sich bei `data` um ein DataFrame, wird dieses unter `filepath` gespeichert.\
Ist `data` ein Python-Dictionary, werden alle DataFrames unter dem Key abgespeichert. Dann kann auch ein Ordner über den Parameter `dir` angegeben werden, wo die DataFrames gespeichert werden sollen.

#### concat_dataframes(data_dict) `return df`
Konkateniert die DataFrames des Python-Dictionaries `data_dict` und gibt das zusammengesetzte DataFrame `df` zurück. Bedeutet alle Zeilen der einzelnen DataFrames werden in einem großen DataFrame gespeichert. 

#### create_plot(header, data, filepath=None, dir=None)
Handelt es sich bei `data` um ein Python-Dictionary (mit String als Key und DataFrame als Value) wird für jedes DataFrame und dem angegeben `header` ein Plot erstellt und unter dem Key abgespeichtert. Wird dem Parameter `dir` ein Ordner übergeben, werden die Plots in diesem gespeichert.\
Dem Parameter `data` kann auch nur ein DataFrame übergeben werden, welches dann unter dem angegeben Parameter `filepath` abgespeichert wird.

#### create_boxplot(header, data, filepath=None, dir=None)
(*siehe create_plot(), jedoch wird hier ein Boxplot erstellt*)

#### density_paragraph(data)
Berechnet für das in `data` übergegebene DataFrame den Dichte-Score je Paragraph und fügt diesen dann dem DataFrame in einer weiteren Spalte hinzu. Diese Spalte erhält den Header `paragraph density`.

#### density_range(dens_range, data, restrict_same_paragraph=False)
Diese Funktion berechnet den Density-Score für Satzfolgen angegebener Größen. Die Größe der Satzfolge, für die der Density-Score berechnet werden soll, wird über den Parameter `dens_range` angegeben und muss eine ungerade Zahl sein. `data` ist das DataFrame für welches der Density-Score berechnet werden soll.\
Z.B. Bei `dens_range=3` wird nicht der Dichte-Score für jeden Satz berechnet, sondern der Dichte-Score jedes Satzes ergibt sich aus drei Sätzen, dem vorherigen, dem eigentlichen, und dem nachfolgenden Satz. Dafür werden die Anzahl der Wörter der drei Sätze summiert und durch die Summe der Matches der drei Sätze dividiert. So werden bei `dens_range=5` zwei vorherige und zwei nachfolgende in die Berechnung mit einbezogen.\
Ist der Parameter `restrict_same_paragraph` auf `True` gesetzt, betrachtet die Methode immer nur Satzfolgen eines Paragraphen und für den letzten Satz eines Paragraphen werden für `dens_range=3` nur der vorherige und der eigentliche Satz in die Berechnung mit einbezogen, da der nachfolgende Satz zu einem anderen Paragraphen gehört.\
Die berechneten Scores werden in einer weitere Spalte dem DataFrame hinzugefügt und entsprechend den Parametern benannt (siehe *config.py* bzgl. Benennung)

#### median_density_per_paragraph(data, skip_one_sentence_paragraphs=False)
Für das unter `data` angegebene DataFrame wird der Median der Dichte-Scores je Paragraph sowie deren Standardabweichung berechnet und in den Spalten `paragraph density median` und `paragraph density std` dem DataFrame hinzugefügt.

#### paragraph_dataframe(data) `return df`
Erstellt für das DataFrame im Parameter `data` ein neues DataFrame `df`, welches statt einem Satz pro Zeile nur noch einen Paragraph pro Zeile enthält.\
Folgende Spalten sind in dem DataFrame enthalten:

Header | Typ | Erläuterung
---|--- | ---
`paragraph nr` | `int` | Paragraph Nummerierung in txt-Datei (getrennt durch \n)
`sentences` | `int` | Anzahl der Sätze
`words` | `int` | Anzahl der Wörter
`matches` | `int` | Anzahl der Matches mit Vokabeliste
`paragraph density` | `float` | Dichte-Score (`matches` / `words`)
`paragraph density median` | `float` | Median der Dichte-Scores je Satz
`paragraph density std` | `float` | Standardabweichung der Dichte-Scores je Satz