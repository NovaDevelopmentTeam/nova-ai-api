import music21 as m21
import random
from magenta.music import midi_io, sequences_lib

def create_harmonious_random_trumpet_chords():
    """
    Erstellt eine Partitur mit zufälligen, harmonisch passenden dreistimmigen Akkorden für drei Trompeten.
    """
    score = m21.stream.Score()
    trumpet_parts = []
    for _ in range(3):  # Simuliere 3 Trompeten für dreistimmige Akkorde
        trumpet_part = m21.stream.Part()
        trumpet_part.append(m21.instrument.Trumpet())  # Instrument hinzufügen
        trumpet_parts.append(trumpet_part)

    key = m21.key.Key('C')  # C-Dur, du kannst dies ändern
    scale = key.getScale('major')
    possible_notes = [note.nameWithOctave for note in scale.getPitches('C3', 'C6')]
    possible_lengths = [1, 1.5, 2, 3]  # Halbe, Viertel, Ganze Noten etc.

    for _ in range(64):  # 64 Akkorde erzeugen
        root_note = random.choice(possible_notes)
        chord_type = random.choice(['major', 'minor'])
        if chord_type == 'major':
            intervals = ['P1', 'M3', 'P5']
        else:
            intervals = ['P1', 'm3', 'P5']

        chord_pitches = [
            m21.pitch.Pitch(root_note).transpose(m21.interval.Interval(interval))
            for interval in intervals
        ]

        note_length = random.choice(possible_lengths)
        for i, trumpet_part in enumerate(trumpet_parts):
            note = m21.note.Note(chord_pitches[i], quarterLength=note_length)
            trumpet_part.append(note)

    for part in trumpet_parts:
        score.append(part)

    return score

def create_algorithmic_trumpet_chords():
    """
    Erstellt eine Partitur mit algorithmisch generierten dreistimmigen Akkorden für drei Trompeten.
    """
    score = m21.stream.Score()
    trumpet_parts = []
    for _ in range(3):  # Simuliere 3 Trompeten für dreistimmige Akkorde
        trumpet_part = m21.stream.Part()
        trumpet_part.append(m21.instrument.Trumpet())  # Instrument hinzufügen
        trumpet_parts.append(trumpet_part)

    possible_lengths2 = [1, 1.5, 2, 3]
    key = m21.key.Key('C')  # C-Dur, du kannst dies ändern
    scale = key.getScale('major')
    root_note = m21.pitch.Pitch('C4')  # Beginn bei C4

    for _ in range(64):  # 64 Akkorde erzeugen
        chord_intervals = ['P1', 'M3', 'P5']
        chord_notes = [root_note.transpose(m21.interval.Interval(interval)) for interval in chord_intervals]
        note_length = random.choice(possible_lengths2)

        for i, trumpet_part in enumerate(trumpet_parts):
            note = m21.note.Note(chord_notes[i], quarterLength=note_length)
            trumpet_part.append(note)

        root_note = root_note.transpose(2)

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

def analyze_midi_with_magenta(midi_file):
    """
    Analysiert eine MIDI-Datei mit Magenta und bewertet musikalische Eigenschaften.
    """
    midi_data = midi_io.midi_file_to_sequence_proto(midi_file)
    total_notes = len(midi_data.notes)
    print(f"Die Datei enthält {total_notes} Noten.")

    for note in midi_data.notes[:10]:
        print(f"Note: {note.pitch}, Startzeit: {note.start_time}, Dauer: {note.end_time - note.start_time}")

    print("Magenta-Analyse abgeschlossen.")
    return midi_data

if __name__ == "__main__":
    choice = input("Wähle Methode (random/algorithmic): ").strip().lower()

    if choice == "random":
        trumpet_score = create_harmonious_random_trumpet_chords()
    elif choice == "algorithmic":
        trumpet_score = create_algorithmic_trumpet_chords()
    else:
        print("Ungültige Auswahl. Standard: Zufällige Akkorde.")
        trumpet_score = create_harmonious_random_trumpet_chords()

    trumpet_score.show()
    midi_filename = "trumpet_output.mid"
    save_score_as_midi(trumpet_score, midi_filename)

    analyze_choice = input("Soll die MIDI-Datei mit Magenta analysiert werden? (y/n): ").strip().lower()
    if analyze_choice == "y":
        analyze_midi_with_magenta(midi_filename)
