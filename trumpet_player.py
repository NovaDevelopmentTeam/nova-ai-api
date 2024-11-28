import music21 as m21


def create_trumpet_score():
    # Erstellen einer neuen Partitur
    score = m21.stream.Score()

    # Trompetenpart hinzufügen
    trumpet_part = m21.stream.Part()
    trumpet_part.instrument = m21.instrument.Trumpet()

    # Erstellen von Noten für die Trompete
    notes = [
        m21.note.Rest(quarterLength=1),  # Ruhe für 1 Viertelnote
        m21.note.Note('C4', quarterLength=1),  # C4 (mittleres C) für 1 Viertelnote
        m21.note.Note('E4', quarterLength=1),  # E4 für 1 Viertelnote
        m21.note.Note('G4', quarterLength=1)   # G4 für 1 Viertelnote
    ]

    # Noten zum Trompetenpart hinzufügen
    for n in notes:
        trumpet_part.append(n)

    # Trompetenpart zur Partitur hinzufügen
    score.append(trumpet_part)

    return score

def save_score_as_midi(score, filename="trumpet_output.mid"):
    # MIDI-Datei speichern
    mf = m21.midi.translate.music21ObjectToMidiFile(score)
    mf.open(filename, 'wb')
    mf.write()
    mf.close()
    print(f"MIDI-Datei gespeichert als {filename}")

# Hauptprogramm
if __name__ == "__main__":
    # Erstelle Trompeten-Partitur
    trumpet_score = create_trumpet_score()

    # Zeige die Partitur (optional)
    trumpet_score.show()

    # Speichere die Partitur als MIDI-Datei
    save_score_as_midi(trumpet_score)
