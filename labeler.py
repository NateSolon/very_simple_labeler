from ipywidgets import widgets, Layout
from IPython.display import display, clear_output
from fastai import *
from fastai.vision import *

def load_image(fn):
    with open(fn, 'rb') as f:
        image = f.read()
    return image
    
class Labeler:
    def __init__(self, path, labels):
        self.path = Path(path)
        self.fns = [x for x in self.path.ls() if x.is_file()]
        self.ll = []
        self.labels = labels
        self.widgets = self.make_widgets()
        self.counter = 0
        
    def make_widgets(self):
        w = {}
        w['image'] = widgets.Image()
        w['label'] = widgets.ToggleButtons(options=self.labels)
        w['next'] = widgets.Button(description='Next')
        return w
    
    def get_next_image(self):
        self.counter += 1
        if self.counter == len(self.fns):
            clear_output()
            print('No more images')
        else:
            self.widgets['image'].value = load_image(self.fns[self.counter])
    
    def next(self, _):
        self.ll.append(self.widgets['label'].value)
        self.get_next_image()        
    
    def label(self):
        self.widgets['image'].value = load_image(self.fns[self.counter])
        self.widgets['next'].on_click(self.next)
        for _, widget in self.widgets.items(): display(widget)
    
    def move_files(self):
        for label in self.labels:
            (self.path/label).mkdir(exist_ok=True)
        for fn, label in zip(self.fns, self.ll):
            fn.rename(self.path/label/fn.name)