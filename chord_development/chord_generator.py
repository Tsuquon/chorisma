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
    num-notes=<int>: give predefined notes
    -chord-develop: by default; choose to develop chords (deprecated)
    -no-develop-chord: doesn't develop chord
    -debug-mode: prints outputs
    -sort: enables sorting of letters (only enable if program is not working) (likely deprecated)
    notes=<list of notes separated by commas>
    # make file name to be chord name
    # need to add # support through extra files

"""


class ChordGenerator:
    def __init__(self, args=None):
        self.args = args

    # has selection of notes and develops a custom chord
    def rand_selection(self) -> None:
        letters = ["A", "B", "C", "D", "E", "F", "G"]
        accidentals = ["", "b", "#"]
        numbers = [1, 2, 3, 4, 5, 6, 7]

        basic_notes, notes, chord = self.note_combiner(letters, numbers, accidentals)

        if "-debug-mode" in self.args:
            print("basic_notes:", basic_notes)
            print("notes:", notes)
            print("chord:", chord)

        if "-develop-chord" in self.args or "-no-develop-chord" not in self.args:
            self.audio_note_combiner(notes)

    # chooses notes, and provides namesake of chord
    def note_combiner(self, letters, numbers, accidentals) -> tuple():
        random.seed()
        
        basic_notes = []
        notes = []
        
        if any(fnmatch.fnmatch(num := number, 'num-notes=*') for number in self.args):
            my_num = int(num[10:])
            no_of_notes = my_num
        
        else: 
            no_of_notes = random.randrange(2, 6)

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
            
        if any(fnmatch.fnmatch(my_args := argument, 'notes=*') for argument in self.args):
            
            set_notes: str = my_args[6:] # (A5, B5, C5)
            set_notes = set_notes.split(',')
            set_notes = [item.strip() for item in set_notes]
            notes = set_notes
            basic_notes = [item[:-1] for item in set_notes]
            
        else:
            i = 0
            while i < no_of_notes:
                letter = random.choice(letters)
                accidental = random.choice(accidentals)
                number = number_choice(numbers)
                if letter == "B" and accidental == "#":
                    letter = "C"
                    accidental = ""

                if letter == "E" and accidental == "#":
                    letter = "F"
                    accidental = ""

                if letter == "F" and accidental == "b":
                    letter = "E"
                    accidental = ""

                if letter == "C" and accidental == "b":
                    letter = "B"
                    accidental = ""

                chord_prefix = letter + accidental + str(number)

                
                if chord_prefix not in notes:
                    basic_notes.append(letter + accidental)
                    notes.append(chord_prefix)
                    i += 1
                
                    

        # combine here using zip, then sort ascending by octave then by note
        zipped = zip(basic_notes, notes)
        if '-sort' in self.args:
            zipped = sorted(zipped, key=sort_chord)
        
        else:
            zipped = sorted(zipped, key=lambda x: x[1][-1])
        basic_notes = [note[0] for note in zipped]
        notes = [note[1] for note in zipped]
        chord = find_chords_from_notes(basic_notes)

        if len(chord) == 0:
            try:
                return self.note_combiner(letters, numbers, accidentals)

            except RecursionError:
                raise RecursionError(
                    "Error happened. If using pre-defined notes or number of notes, it may be because the arrangment does not exist\n"
                                    f"notes: {notes}"
                                    ) from None


        return basic_notes, notes, chord

    # creates audiofile of combined notes i.e chord
    def audio_note_combiner(self, notes):
        sharp_to_flat = {'A#':'Bb', 'C#':'Db', 'D#':'Eb', 'F#':'Gb', 'G#':'Ab'}

        
        # combine notes
        name = []
        name_note = notes[0]
        
        if notes[0][:-1] in sharp_to_flat:
            notes[0] = sharp_to_flat.get(notes[0][:-1]) + notes[0][-1]
        
        try:
            combined_sounds = AudioSegment.from_mp3(
                f"./chord_development/piano-mp3/{notes[0]}.mp3"
            )

        except FileNotFoundError:
            raise FileNotFoundError(
                f"The file path for the specified note '{notes[0]}' doesn't exist"
            )

        name.append(name_note)
        notes.pop(0)

        for note in notes:
            name_note = note
            
            if note[:-1] in sharp_to_flat:
                note = sharp_to_flat.get(note[:-1]) + note[-1]
            
            if not os.path.exists(f"./chord_development/piano-mp3/{note}.mp3"):
                raise FileNotFoundError(
                    f"The file path for the specified note '{name_note}' doesn't exist"
                )

            sound = AudioSegment.from_mp3(f"./chord_development/piano-mp3/{note}.mp3")
            combined_sounds = combined_sounds.overlay(sound)
            name.append(name_note)

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
    sys.setrecursionlimit(10000)
    chord_generator = ChordGenerator(sys.argv)
    chord_generator.rand_selection()
