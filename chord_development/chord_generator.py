from pychord import Chord, find_chords_from_notes
from pydub import AudioSegment
import random
import os
import sys
import fnmatch

"""
This function generates random chords, creates an audiowave saves file
system arguments can be given:
    dest=<directory destination>; by default is stored-chords
    -chord-develop: by default; choose to develop chords
    -no-develop-chord: doesn't develop chord
    -debug-mode: prints outputs
"""


class ChordGenerator:
    def __init__(self, args=None):
        self.args = args

    # has selection of notes and develops a custom chord
    def rand_selection(self) -> None:
        letters = ["A", "B", "C", "D", "E", "F", "G"]
        accidentals = ["","b","#"]
        numbers = [1, 2, 3, 4, 5, 6, 7]

        basic_notes, notes, chord = self.note_combiner(letters, numbers, accidentals)
        
        if "-debug-mode" in self.args:
            print('basic_notes:', basic_notes)
            print('notes:', notes)
            print('chord:', chord)

        if "-develop-chord" in self.args or "-no-develop-chord" not in self.args:
            self.audio_note_combiner(notes)

    # chooses notes, and provides namesake of chord
    def note_combiner(self, letters, numbers, accidentals) -> tuple():
        basic_notes = []
        notes = []
        no_of_notes = random.randrange(2, 6)
        random.seed()

        def number_choice(number_list):
            number = random.choice(number_list)

            if len(notes) == 0:
                return number

            comparer = int(notes[0][-1])
            if abs(comparer - number) > 2:
                return number_choice(number_list)

            return number

        def sort_chord(item):
            item = item[1]
            if len(item) == 2:
                return (item[1], item[0])

            if len(item) == 3:
                return (item[2], item[0], item[1])

            else:
                raise ValueError("The note is not the correct size")

        for i in range(no_of_notes):
            letter = random.choice(letters)
            accidental = random.choice(accidentals)
            number = number_choice(numbers)
            if letter == 'B' and accidental == '#':
                letter = 'C'
                accidental = ''
            
            if letter == 'E' and accidental == '#':
                letter = 'F'
                accidental = ''
                
            if letter == 'F' and accidental == 'b':
                letter = 'E'
                accidental = ''
            
            if letter == 'C' and accidental == 'b':
                letter = 'B'
                accidental = ''
            
            chord_prefix = letter + accidental + str(number)

            if chord_prefix not in notes:
                basic_notes.append(letter + accidental)
                notes.append(chord_prefix)

        # combine here using zip, then sort ascending by octave then by note
        zipped = zip(basic_notes, notes)
        zipped = sorted(zipped, key=sort_chord)
        print(zipped)
        basic_notes = [note[0] for note in zipped]
        notes = [note[1] for note in zipped]
        print(basic_notes)
        # problem here that E#, B# and Fb don't exist
        chord = find_chords_from_notes(basic_notes)

        if len(chord) == 0:
            try:
                return self.note_combiner(letters, numbers, accidentals)

            except RecursionError:
                print("Error happened")
                print(notes)
                exit()

        return basic_notes, notes, chord

    # creates audiofile of combined notes i.e chord
    def audio_note_combiner(self, notes):
        # combine notes
        name = []
        try:
            combined_sounds = AudioSegment.from_mp3(
                f"./chord_development/piano-mp3/{notes[0]}.mp3"
            )

        except FileNotFoundError:
            raise FileNotFoundError(
                f"The file path for the specified note '{notes[0]}' doesn't exist"
            )

        name.append(notes[0])
        notes.pop(0)

        for note in notes:
            if not os.path.exists(f"./chord_development/piano-mp3/{note}.mp3"):
                raise FileNotFoundError(
                    f"The file path for the specified note '{note}' doesn't exist"
                )

            sound = AudioSegment.from_mp3(f"./chord_development/piano-mp3/{note}.mp3")
            combined_sounds = combined_sounds.overlay(sound)
            name.append(note)

        sep = "_"
        name = sep.join(name)
        
        if any(
            fnmatch.fnmatch(my_args := argument, "dest=*") for argument in self.args
        ):
            store_directory = my_args[5:]
        else:
            store_directory = "stored-chords"

        try:
            combined_sounds.export(f"{store_directory}/{name}.mp3", format="mp3")

        except FileNotFoundError:
            raise FileNotFoundError("Make sure directory exists")


if __name__ == "__main__":
    chord_generator = ChordGenerator(sys.argv)
    chord_generator.rand_selection()
