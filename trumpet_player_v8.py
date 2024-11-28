import music21 as m21
import random

def create_harmonious_random_trumpet_chords():
    """
    Erstellt eine Partitur mit zufälligen, harmonisch passenden dreistimmigen Akkorden für drei Trompeten.
    """
    # Erstellen einer neuen Partitur
    score = m21.stream.Score()

    # Erstellen von mehreren Trompetenparts (für Akkorde)
    trumpet_parts = []
    for _ in range(3):  # Simuliere 3 Trompeten für dreistimmige Akkorde
        trumpet_part = m21.stream.Part()
        trumpet_part.append(m21.instrument.Trumpet())  # Instrument hinzufügen
        trumpet_parts.append(trumpet_part)

    # Tonart festlegen (z. B. C-Dur)
    key = m21.key.Key('C')  # C-Dur, du kannst dies ändern (z. B. "G", "F#m")
    scale = key.getScale('major')  # Verwende die Dur-Tonleiter

    # Erweiterte Liste der möglichen Noten basierend auf der Tonleiter
    possible_notes = [note.nameWithOctave for note in scale.getPitches('C3', 'C6')]

    # Erweiterte Liste der möglichen Notenlängen
    possible_lengths = [1, 1.5, 2, 3]  # Halbe, Viertel, Ganze Noten etc.

    for _ in range(64):  # 64 Akkorde erzeugen
        # Wähle eine zufällige Stufe der Tonleiter als Akkordbasis
        root_note = random.choice(possible_notes)

        # Generiere einen Dur- oder Moll-Akkord aus der Tonleiter
        chord_type = random.choice(['major', 'minor'])  # Dur oder Moll
        if chord_type == 'major':
            intervals = ['P1', 'M3', 'P5']  # Grundton, große Terz, Quinte
        else:
            intervals = ['P1', 'm3', 'P5']  # Grundton, kleine Terz, Quinte

        chord_pitches = [
            m21.pitch.Pitch(root_note).transpose(m21.interval.Interval(interval))
            for interval in intervals
        ]

        note_length = random.choice(possible_lengths)

        # Jeder Trompetenpart spielt eine Note des Akkords
        for i, trumpet_part in enumerate(trumpet_parts):
            note = m21.note.Note(chord_pitches[i], quarterLength=note_length)
            trumpet_part.append(note)

    # Alle Trompetenparts zur Partitur hinzufügen
    for part in trumpet_parts:
        score.append(part)

    return score

def save_score_as_midi(score, filename="harmonious_trumpet_output.mid"):
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
    # Zufällige harmonische Akkorde erzeugen
    trumpet_score = create_harmonious_random_trumpet_chords()

    # Zeige die Partitur (optional, falls du es nicht brauchst, kommentiere es aus)
    trumpet_score.show()

    # Speichere die Partitur als MIDI-Datei
    save_score_as_midi(trumpet_score)
