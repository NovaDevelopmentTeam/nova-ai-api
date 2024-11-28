import music21 as m21
import random

def create_random_trumpet_chords():
    """
    Erstellt eine Partitur mit zufälligen dreistimmigen Akkorden für drei Trompeten.
    """
    # Erstellen einer neuen Partitur
    score = m21.stream.Score()

    # Erstellen von mehreren Trompetenparts (für Akkorde)
    trumpet_parts = []
    for _ in range(3):  # Simuliere 3 Trompeten für dreistimmige Akkorde
        trumpet_part = m21.stream.Part()
        trumpet_part.append(m21.instrument.Trumpet())  # Instrument hinzufügen
        trumpet_parts.append(trumpet_part)

    # Erweiterte Liste der möglichen Noten
    possible_notes = [
        'A2', 'B2', 'C3', 'D3', 'E3', 'F3', 'G3',
        'A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4',
        'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5',
        'A5', 'B5', 'C6', 'D6', 'E6', 'F6', 'G6',
        'A6', 'B6', 'C7'
    ]

    # Erweiterte Liste der möglichen Notenlängen
    possible_lengths = [1, 1.5, 2, 3]  # Halbe, Viertel, Ganze Noten etc.

    for _ in range(64):  # 64 Akkorde erzeugen
        chord_notes = random.sample(possible_notes, 3)  # Wähle 3 zufällige Noten
        note_length = random.choice(possible_lengths)

        # Jeder Trompetenpart spielt eine Note des Akkords
        for i, trumpet_part in enumerate(trumpet_parts):
            note = m21.note.Note(chord_notes[i], quarterLength=note_length)
            trumpet_part.append(note)

    # Alle Trompetenparts zur Partitur hinzufügen
    for part in trumpet_parts:
        score.append(part)

    return score

def create_algorithmic_trumpet_chords():
    """
    Erstellt eine Partitur mit algorithmisch generierten dreistimmigen Akkorden für drei Trompeten.
    """
    # Erstellen einer neuen Partitur
    score = m21.stream.Score()

    # Erstellen von mehreren Trompetenparts (für Akkorde)
    trumpet_parts = []
    for _ in range(3):  # Simuliere 3 Trompeten für dreistimmige Akkorde
        trumpet_part = m21.stream.Part()
        trumpet_part.append(m21.instrument.Trumpet())  # Instrument hinzufügen
        trumpet_parts.append(trumpet_part)

    # Erweiterte Liste der möglichen Notenlängen
    possible_lengths2 = [1, 1.5, 2, 3]  # Halbe, Viertel, Ganze Noten etc.

    # Erzeugung einer aufsteigenden Akkordfolge
    root_note = m21.pitch.Pitch('C4')  # Beginn bei C4

    for _ in range(64):  # 64 Akkorde erzeugen
        # Akkordbasis und Intervalle festlegen (Terz- und Quintabstände für Dur-Akkord)
        chord_intervals = [
            m21.interval.Interval('P1'),  # Grundton
            m21.interval.Interval('M3'),  # Große Terz
            m21.interval.Interval('P5')   # Perfekte Quinte
        ]
        chord_notes = [root_note.transpose(interval) for interval in chord_intervals]
        note_length = random.choice(possible_lengths2)

        # Jeder Trompetenpart spielt eine Note des Akkords
        for i, trumpet_part in enumerate(trumpet_parts):
            note = m21.note.Note(chord_notes[i], quarterLength=note_length)
            trumpet_part.append(note)

        root_note = root_note.transpose(2)  # Akkordbasis um eine Sekunde erhöhen

    # Alle Trompetenparts zur Partitur hinzufügen
    for part in trumpet_parts:
        score.append(part)

    return score

def save_score_as_midi(score, filename="trumpet_output.mid"):
    """
    Speichert die übergebene Partitur als MIDI-Datei.
    """
    mf = m21.midi.translate.music21ObjectToMidiFile(score)
    mf.open(filename, 'wb')
    mf.write()
    mf.close()
    print(f"MIDI-Datei gespeichert als {filename}")

# Hauptprogramm
if __name__ == "__main__":
    # Wähle entweder den zufälligen oder den algorithmischen Ansatz:

    # Zufällige Akkorde erzeugen
    trumpet_score = create_random_trumpet_chords()

    # Algorithmische Akkordfolge erzeugen
    # trumpet_score = create_algorithmic_trumpet_chords()

    # Zeige die Partitur (optional, falls du es nicht brauchst, kommentiere es aus)
    trumpet_score.show()

    # Speichere die Partitur als MIDI-Datei
    save_score_as_midi(trumpet_score)
