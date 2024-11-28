from flask import Flask, request, jsonify, send_file, render_template
import music21 as m21
import random
from magenta.music import midi_io

app = Flask(__name__)

def create_harmonious_random_trumpet_chords():
    """
    Erstellt eine Partitur mit zufälligen, harmonisch passenden dreistimmigen Akkorden für drei Trompeten.
    """
    score = m21.stream.Score()
    trumpet_parts = []
    for _ in range(3):
        trumpet_part = m21.stream.Part()
        trumpet_part.append(m21.instrument.Trumpet())
        trumpet_parts.append(trumpet_part)

    key = m21.key.Key('C')
    scale = key.getScale('major')
    possible_notes = [note.nameWithOctave for note in scale.getPitches('C3', 'C6')]
    possible_lengths = [1, 1.5, 2, 3]

    for _ in range(64):
        root_note = random.choice(possible_notes)
        chord_type = random.choice(['major', 'minor'])
        intervals = ['P1', 'M3', 'P5'] if chord_type == 'major' else ['P1', 'm3', 'P5']
        chord_pitches = [m21.pitch.Pitch(root_note).transpose(m21.interval.Interval(interval)) for interval in intervals]
        note_length = random.choice(possible_lengths)
        for i, trumpet_part in enumerate(trumpet_parts):
            note = m21.note.Note(chord_pitches[i], quarterLength=note_length)
            trumpet_part.append(note)

    for part in trumpet_parts:
        score.append(part)

    return score

def save_score_as_midi(score, filename):
    mf = m21.midi.translate.music21ObjectToMidiFile(score)
    mf.open(filename, 'wb')
    mf.write()
    mf.close()
    return filename

def analyze_midi_with_magenta(midi_file):
    midi_data = midi_io.midi_file_to_sequence_proto(midi_file)
    total_notes = len(midi_data.notes)
    analysis = f"Die Datei enthält {total_notes} Noten.\n"

    for note in midi_data.notes[:10]:
        analysis += f"Note: {note.pitch}, Startzeit: {note.start_time}, Dauer: {note.end_time - note.start_time}\n"

    analysis += "Magenta-Analyse abgeschlossen."
    return analysis

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Erstelle zufällige Akkorde
    score = create_harmonious_random_trumpet_chords()
    midi_filename = "trumpet_output.mid"
    save_score_as_midi(score, midi_filename)

    # Analysiere mit Magenta
    analysis = analyze_midi_with_magenta(midi_filename)

    # Speichere Analyse als Log
    analysis_filename = "analysis_log.txt"
    with open(analysis_filename, "w") as f:
        f.write(analysis)

    return jsonify({
        "midi_file": midi_filename,
        "log_file": analysis_filename
    })

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
