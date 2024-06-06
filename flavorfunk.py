import streamlit as st
import pandas as pd
from datetime import datetime


# Klassenerstellung
class Bestellung:
    def __init__(self, tischnummer: int, speise_mengen_dict: dict[str, int], info: str =""):
        """
        Initialisiert den Bestellvorgang.
        
        args:
            tischnummer: Die Tischnummer
            speise_mengen_dict: Ein Dictionary aus Artikel und der bestellten Menge
            info: Zusatzinfo zur Bestellung
        """
        self.bestell_id = self.generate_bestell_id()
        self.datum = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Aktuelles Datum/Uhrzeit zum Bestellzeitpunkt
        self.tischnummer = tischnummer
        self.status = "offen"                                      # Bestellstatus standartmäßig "offen" bei neuer Bestellung
        self.speisen = speise_mengen_dict
        self.info = info


    @staticmethod
    def generate_bestell_id() -> int:
        """
        Generiert eine einzigartige Bestell-ID pro bestelltem Artikel.
        """
        if "bestell_counter" not in st.session_state:    # st.session_state zwischenspeichert Variablen zur weiteren Verwendung
            st.session_state.bestell_counter = 1         # in dem Fall wird "bestell_counter" zwischengespeichert 
        bestell_id = st.session_state.bestell_counter
        st.session_state.bestell_counter += 1
        return bestell_id


    def to_dataframe(self) -> pd.DataFrame:
        """
        Erstellt aus der Bestellung ein Dataframe.
        
        returns:
            pd.Dataframe: Ein Dataframe, welches die Details der Bestellung enthält
        """

        # self.speisen.items wird iterierbar gemacht, sodass speise_name und menge aus dem dictionary 
        # entnommen werden und dem neuen Dictionary hinzugefügt werden können. 
        speise_name, menge = next(iter(self.speisen.items()))  
        bestellung = {
            "Bestell ID": self.bestell_id,
            "Datum": self.datum,
            "Tischnummer": self.tischnummer,
            "Speise": speise_name,
            "Menge": menge,
            "Status": self.status,
            "Zusatz": self.info
            }
        return pd.DataFrame([bestellung])



class BestellungenVerwaltung:
    def __init__(self, speisekarte_df: pd.DataFrame):
        """
        Initialisiert die Verwaltung der Bestellung mit der Speisekarte.
        
        args:
            speisekarte_df: Das geladene Dataframe der Speisekarte
        """
        self.speisekarte_df = speisekarte_df
        self.spalten = ["Bestell ID", "Datum", "Tischnummer", "Speise", "Menge", "Status", "Zusatz"]
        if "bestellungen_df" not in st.session_state:
            st.session_state.bestellungen_df = pd.DataFrame(columns=self.spalten)

   
    def neue_bestellung(self, tischnummer: int, speise_mengen_dict: dict[str,int], info: str="") ->bool:
        """
        Fügt eine neue Bestellung hinzu.

        args:
            tischnummer: Tischnummer der Bestellung
            speise_mengen_dict: Dictionary mit Speisen und deren bestelle Menge
            info: Zusatzinformationen zur Bestellung

        return:
            True, wenn die Bestellung erfolgreich hinzugefügt wurde, sonst False
        """
        bestellung = Bestellung(tischnummer, speise_mengen_dict, info)
        bestellung_df = bestellung.to_dataframe()
        st.session_state.bestellungen_df = (
            pd.concat([st.session_state.bestellungen_df, bestellung_df], ignore_index=True)
            )
        return True


    def anzeigen_bestellungen(self):
        """
        Zeigt Bestellungen an und ermöglicht Stornierungen.
        """
        st.header("Bestellübersicht")
        tischnummern_lst = st.session_state.bestellungen_df["Tischnummer"].unique()
        ausgewaehlte_tischnummer = st.selectbox("Tischnummer auswählen:", tischnummern_lst)

        gefiltertes_df = (
            st.session_state.bestellungen_df[st.session_state.bestellungen_df["Tischnummer"] == ausgewaehlte_tischnummer]
            .drop("Tischnummer", axis=1)
            .reset_index(drop=True)
            )

        if gefiltertes_df.empty:
            st.info(f"Keine Bestellungen für Tischnummer {ausgewaehlte_tischnummer} vorhanden.")
        else:
            st.subheader(f"Tischnummer {ausgewaehlte_tischnummer}")
            st.dataframe(gefiltertes_df, width=1000)

            # Stornieroption
            st.subheader("Bestellung stornieren")
            storno_id = st.number_input("Bestell-ID", min_value=1)
            if st.button("Bestellung stornieren"):
                if self.storno(storno_id):
                    st.success("Bestellung erfolgreich storniert.")
                else:
                    st.error("Fehler beim Stornieren der Bestellung. Überprüfen Sie die Bestell-ID.")


    def storno(self, storno_id: int) -> bool:
        """
        Stornierung einer Bestellung.
        
        args:
            storno_id: Bestell-ID des zu stornierenden Artikels
        
        returns:
            True wenn Stornierung erfolgreich, ansonsten False
            """
        if storno_id in st.session_state.bestellungen_df["Bestell ID"].values:
            st.session_state.bestellungen_df.loc[st.session_state.bestellungen_df["Bestell ID"] == storno_id, "Status"] = "storno"
            return True
        return False


    def bezahlung(self, tischnummer: int, bezahl_methode: str, trinkgeld: float=0) -> dict|bool:
        """
        Bezahlung aller offener Bestellungen an einem Tisch. 
        Status wird auf "bezahlt" gesetzt.
    
        args:
            tischnummer: Tischnummer an der die Bezahlung erfolgt
            bezahl_methode: Ausgewählte Bezahlmethode
            trinkgeld: Optionales Trinkgeld. default=0
    
        returns:
            Ein Dictionary aus Bezahldetails, oder ein False wenn Bezahlvorgang nicht möglich
        """
        rechnung_df = st.session_state.bestellungen_df[
            (st.session_state.bestellungen_df["Tischnummer"] == tischnummer) &
            (st.session_state.bestellungen_df["Status"] == "offen")
            ]
        if rechnung_df.empty:
            return False
    
        total_brutto = 0
        rechnungs_details = []
    
        updated_df = st.session_state.bestellungen_df.copy()    # Kopie des DataFrames erstellen
    
        for _, order in rechnung_df.iterrows():
            speise_name = order["Speise"]
            menge = order["Menge"]
            preis = self.speisekarte_df.loc[self.speisekarte_df["Name"] == speise_name, "Preis (in €)"].iloc[0]
            total = preis * menge
            total_brutto += total
            total_netto = total_brutto / (1 + 0.19)
            steuerbetrag = total_brutto - total_netto
            rechnungs_details.append((speise_name, menge, preis, total))

            # Status wird auf 'bezahlt' geändert, jedoch nur auf der Kopie von bestellungen_df
            updated_df.loc[updated_df["Bestell ID"] == order["Bestell ID"], "Status"] = "bezahlt"  
    
        return {
            "details": rechnungs_details,
            "total_brutto": total_brutto,
            "trinkgeld": trinkgeld,
            "mwst": "19%",
            "total_netto": total_netto,
            "steuerbetrag": steuerbetrag,
            "bezahl_methode": bezahl_methode,
            "updated_df": updated_df
            }


# Anwendungscode
def main():
    """
    Hauptfunktion der App.
    """
    speisekarte_df = pd.read_csv("Speisekarte.csv", index_col="Art.-Nr.", encoding="utf-8")
    verwaltung = BestellungenVerwaltung(speisekarte_df)

    # Streamlit Grundlayout 
    st.title("FlavorFunk")
    st.sidebar.title("Navigation")
    menu_option = st.sidebar.selectbox(
        "Bitte auswählen",
        ("Speisekarte anzeigen", "Neue Bestellung erstellen", "Bestellungen anzeigen", "Bestellung bezahlen")
        )

    # Optionen und deren Ausführung
    if menu_option == "Speisekarte anzeigen":
        st.header("Golden Seagull - Speisekarte")
        st.dataframe(speisekarte_df, width=900)

    elif menu_option == "Neue Bestellung erstellen":
        st.header("Neue Bestellung")

        # Eingabe-/Auswahlfelder
        tischnummer = st.selectbox("Wählen Sie die Tischnummer:", list(range(1, 14)))
        col1, col2 = st.columns([1, 1])
        with col1:
            speise_name = st.selectbox("Artikel auswählen:", speisekarte_df["Name"].tolist())
        with col2:
            menge = st.number_input("Menge", min_value=1, step=1)
        info = st.text_input("Zusatzinfo:")
        
        # Abschicken der Bestellung
        if st.button("Bestellung hinzufügen"):
            if verwaltung.neue_bestellung(tischnummer, {speise_name: menge}, info):
                st.success("Bestellung erfolgreich hinzugefügt.")
            else:
                st.error("Fehler beim Hinzufügen der Bestellung. Überprüfen Sie die Auswahl.")

    elif menu_option == "Bestellungen anzeigen":
        verwaltung.anzeigen_bestellungen()
    
    elif menu_option == "Bestellung bezahlen":
        st.header("Bestellung bezahlen")
        tischnummer = st.selectbox("Wählen Sie die Tischnummer:", list(range(1, 14)))

        # Ausgabe der Rechnung des jeweiligen Tisches
        if tischnummer:
            st.subheader("Rechnungsdetails:")
            rechnung = verwaltung.bezahlung(tischnummer, "")
            if rechnung:
                for detail in rechnung["details"]:
                    st.write(f"{detail[0]} ({detail[1]} x {detail[2]:.2f} €) - Total: {detail[3]:.2f} €")
                st.write("==========================================================")
                st.write(f"**Gesamtsumme:** {rechnung["total_brutto"]:.2f} €")
                st.write("==========================================================")
                st.write(f"Mwst: {rechnung["mwst"]}")
                st.write(f"Netto: {rechnung["total_netto"]:.2f} €")
                st.write(f"Steuerbetrag: {rechnung["steuerbetrag"]:.2f} €")

                # Anschließende Auswahl über Bezahlmethode und optionalem Trinkgeld
                bezahl_methode = st.radio("Zahlungsmethode auswählen:", ("Bar", "Karte"))
                trinkgeld = st.number_input("Trinkgeld", min_value=0.00, step=0.50)

                # Entgültige Zahlbestätigung mit Ausgabe
                if st.button("Bezahlung bestätigen"):
                    rechnung = verwaltung.bezahlung(tischnummer, bezahl_methode, trinkgeld)
                    st.success(
                        "Zahlung erfolgreich. Gesamtbetrag (inkl. Trinkgeld): " 
                        f"{rechnung["total_brutto"] + rechnung["trinkgeld"]:.2f} €"
                        )
                    st.write(f"Zahlungsmethode: {rechnung["bezahl_methode"]}")
                    st.write(f"Trinkgeld: {rechnung["trinkgeld"]:.2f} €")
                    st.session_state.bestellungen_df = rechnung["updated_df"]   # Überschreiben des Original Dataframes
            else:
                st.info("Keine offenen Bestellungen für diese Tischnummer.")


# Prüfen ob direkte Ausführung des Skripts oder über Import
if __name__ == "__main__":
    main()