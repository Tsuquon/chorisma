import sys
from chord_development import chord_generator

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    
    num_chords = 500 # times this by note number for true value
    note_num_max = 7
    
    for chord_dev in range(num_chords):
        for note_num in range(2, note_num_max):
            
            
            # as an argument, usually sys.argv but can provide own if it is a list
            chord_gen = chord_generator.ChordGenerator([f"num-notes={note_num}","-debug-mode"])
            chord_gen.rand_selection()