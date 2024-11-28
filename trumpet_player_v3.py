import music21 as m21
import random

def create_random_trumpet_score():
    # Erstellen einer neuen Partitur
    score = m21.stream.Score()

    # Trompetenpart hinzufügen
    trumpet_part = m21.stream.Part()
    trumpet_part.instrument = m21.instrument.Trumpet()

    # Erweiterte Liste der möglichen Noten
    possible_notes = [
        'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5', 'C6'
    ]

    # Erweiterte Liste der möglichen Notenlängen
    possible_lengths = [0.25, 0.5, 0.75, 1, 1.5, 2]  # Achtel-, Viertel-, Halbe-, Ganze Noten

    notes = []

    for _ in range(128):  # Erstellen von 16 zufälligen Noten
        note_name = random.choice(possible_notes)
        note_length = random.choice(possible_lengths)
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

    # Erweiterte Liste der möglichen Notenlängen
    possible_lengths = [0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4]

    # Algorithmus für aufsteigende Notenfolge mit unterschiedlichen Notenlängen
    notes = []
    start_note = m21.pitch.Pitch('C4')  # Beginn bei C4

    for i in range(16):  # 16 Noten erzeugen
        new_note = m21.note.Note(start_note)
        new_note.quarterLength = random.choice(possible_lengths)
        notes.append(new_note)
        start_note = start_note.transpose(random.choice([1, 2, 3]))  # Erhöhen der Tonhöhe um eine Sekunde, Terz oder andere Intervalle

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
