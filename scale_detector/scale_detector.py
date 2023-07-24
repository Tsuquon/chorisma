from musthe import *
import sys

class ScaleDetector:
    
    def __init__(self, arguments: list):
        self.arguments = arguments
        self.notes = [Note(argument) for argument in arguments]
        self.lim_scales = []
    
    def check_chords(self) -> list:
        for scale in Scale.all():
            if self.notes in scale:
                self.lim_scales.append(scale)
                
        # print(self.lim_scales)
        return self.lim_scales
                  
    
    
if __name__ == "__main__":
    scale_detector = ScaleDetector(sys.argv[1:])
    scale_detector.check_chords()
    
