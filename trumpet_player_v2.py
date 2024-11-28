import music21 as m21
import random

def create_random_trumpet_score():
    # Erstellen einer neuen Partitur
    score = m21.stream.Score()

    # Trompetenpart hinzufügen
    trumpet_part = m21.stream.Part()
    trumpet_part.instrument = m21.instrument.Trumpet()

    # Noten erstellen (hier zufällig)
    notes = []
    possible_notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']  # Bereich der möglichen Noten

    for _ in range(64):  # Erstellen von 8 zufälligen Noten
        note_name = random.choice(possible_notes)
        note_length = random.choice([0.5, 1, 1.5, 2])  # Zufällige Dauer (Halbe, Ganze, usw.)
        note = m21.note.Note(note_name, quarterLength=note_length)
        notes.append(note)

    # Noten zum Trompetenpart hinzufügen
    for n in notes:
        trumpet_part.append(n)

    # Trompetenpart zur Partitur hinzufügen
    score.append(trumpet_part)

    return score

def create_algorithmic_trumpet_score():
    # Erstellen einer neuen Partitur
    score = m21.stream.Score()

    # Trompetenpart hinzufügen
    trumpet_part = m21.stream.Part()
    trumpet_part.instrument = m21.instrument.Trumpet()

    # Algorithmus für aufsteigende Notenfolge
    notes = []
    start_note = m21.pitch.Pitch('C4')  # Beginn bei C4

    for i in range(8):  # 8 Noten erzeugen
        new_note = m21.note.Note(start_note)
        new_note.quarterLength = 1  # Viertelnote
        notes.append(new_note)
        start_note = start_note.transpose(2)  # Erhöhen der Tonhöhe um eine Sekunde

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
    # Wähle entweder den zufälligen oder den algorithmischen Ansatz:
    
    # Zufällige Noten erzeugen
    trumpet_score = create_random_trumpet_score()
    
    # Algorithmische Notenfolge erzeugen
    # trumpet_score = create_algorithmic_trumpet_score()

    # Zeige die Partitur (optional, falls du es nicht brauchst, kommentiere es aus)
    trumpet_score.show()

    # Speichere die Partitur als MIDI-Datei
    save_score_as_midi(trumpet_score)
