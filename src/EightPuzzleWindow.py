
import os
import time
import threading

import wx

from NPuzzleState import *
from NPuzzleAgent import *


class EightPuzzle(wx.Window):
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition,
            size=(300, 300), puzzle_size=3, free_piece=0, filename=None):
        wx.Window.__init__(self, parent, id, pos, size)
        self.filename = filename
        self.puzzle_size = puzzle_size
        self.free_piece = free_piece
        self.size = size
        self.input_allowed = True
        self._init_puzzle()
        self._event_handlers()

    def reset_puzzle(self):
        self._init_puzzle()

    def set_image(self, filename):
        self.filename = filename
        self._init_puzzle()

    def set_puzzle_size(self, puzzle_size):
        self.puzzle_size = puzzle_size
        self._init_puzzle()

    def set_free_piece(self, free_piece):
        self.free_piece = free_piece
        self._init_puzzle()

    def _init_puzzle(self):
        self.solved = False
        if self.filename:
            self.raw_image = wx.Image(self.filename)
            if self.size is None:
                self.SetSize(self.raw_image.GetSize())
        self.model = RandomNPuzzleState(self.puzzle_size, self.free_piece)
        self._init_buffer()
        self.size = self.GetClientSize()

    def _init_buffer(self):
        self.buffer = wx.EmptyBitmap(*self.GetClientSize())
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush('Black'))
        dc.Clear()
        self._draw_scene(dc)
        self.reinit_buffer = False
        
    def _tile_size(self):
        window_width, window_height = self.GetClientSize()
        return (window_width / self.puzzle_size,
                window_height / self.puzzle_size)

    def _draw_scene(self, dc):
        self._make_tiles()
        tile_width, tile_height = self._tile_size()
        for row in range(self.puzzle_size):
            for col in range(self.puzzle_size):
                x = col * tile_width
                y = row * tile_height
                number = self.model.state[row * self.puzzle_size + col]
                if number != self.model.free or self.solved == True:
                    dc.DrawBitmap(self.tiles[number].bmp, x, y)

    def _make_tiles(self):
        self.tiles = {}
        for number in range(self.puzzle_size ** 2):
            if self.filename:
                if 'raw_image' not in dir(self):
                    self.raw_image = wx.Image(self.filename)
                image = self.raw_image.Copy()
                image.Rescale(*self.GetClientSize())
                image = image.ConvertToBitmap()
                row = number // self.puzzle_size
                col = number % self.puzzle_size
                self.tiles[number] = \
                    ImageTile(row, col, image, self._tile_size())
            else:
                self.tiles[number] = NumberTile(number, self._tile_size())

    def _event_handlers(self):
        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_SIZE, self._on_size)
        self.Bind(wx.EVT_IDLE, self._on_idle)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_leftdown)

    def _on_paint(self, event):
        wx.BufferedPaintDC(self, self.buffer)

    def _on_size(self, event):
        self.reinit_buffer = True

    def _on_idle(self, event):
        #if self.reinit_buffer:
        self._init_buffer()
        self.Refresh(False)

    def _on_leftdown(self, event):
        if not self.model.is_solved() and self.input_allowed:
            mouse_x, mouse_y = event.GetPositionTuple()
            tile_width, tile_height = self._tile_size()
            row = int(mouse_y / tile_height)
            col = int(mouse_x / tile_width)
            for (r, c, a) in self.model.valid_moves():
                if r == row and c == col:
                    self.model = self.model.do_action(r, c, a)
                    self.reinit_buffer = True
                    break
            if self.model.is_solved():
                self.solved = True


class NumberTile(object):
    def __init__(self, number, size=(100, 100)):
        self.number = number
        self.size = size
        self.make_bitmap()

    def make_bitmap(self):
        w, h = self.size
        self.bmp = wx.EmptyBitmap(w, h)
        dc = wx.MemoryDC(self.bmp)
        dc.SetBackground(wx.Brush('Black'))
        dc.Clear()
        dc.DrawRectangle(1, 1, w - 1, h - 1)
        dc.DrawText(str(self.number), w / 2, h / 2)
        dc.SelectObject(wx.NullBitmap)


class ImageTile(object):
    def __init__(self, row, column, bitmap, size=(100, 100)):
        self.row = row
        self.column = column
        self.size = size
        self.bitmap = bitmap
        self.make_bitmap()

    def make_bitmap(self):
        w, h = self.size
        self.bmp = wx.EmptyBitmap(w, h)
        srcdc = wx.MemoryDC(self.bitmap)
        dstdc = wx.MemoryDC(self.bmp)
        dstdc.SetBackground(wx.Brush('Black'))
        dstdc.Clear()
        dstdc.Blit(0, 0, w, h, srcdc, self.column * w, self.row * h)
        srcdc.SelectObject(wx.NullBitmap)
        dstdc.SelectObject(wx.NullBitmap)


class EightPuzzleFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Eight Puzzle")
        self._arrage_widgets()
        self._event_handers()

    def _arrage_widgets(self):
        sizer = wx.GridBagSizer(hgap=10, vgap=10)
        self.puzzle = EightPuzzle(self, size=None, filename='funny-cat.jpg',
            free_piece=8)
        self.btn_new = wx.Button(self, label='New Puzzle', size=(100, 20))
        self.btn_image = wx.Button(self, label='New Image', size=(100, 20))
        self.btn_solve = wx.Button(self, label='Solve', size=(100, 20))
        sizer.Add(self.puzzle, pos=(0, 0), span=(4, 1), flag=wx.EXPAND)
        sizer.Add(self.btn_new, pos=(0, 1))
        sizer.Add(self.btn_image, pos=(1, 1))
        sizer.Add(self.btn_solve, pos=(2, 1))
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(3)
        self.SetSizer(sizer)
        self.Fit()

    def _event_handers(self):
        self.Bind(wx.EVT_BUTTON, self._on_newclick, self.btn_new)
        self.Bind(wx.EVT_BUTTON, self._on_imageclick, self.btn_image)
        self.Bind(wx.EVT_BUTTON, self._on_solveclick, self.btn_solve)

    def _on_newclick(self, event):
        if self.puzzle.input_allowed:
            self.puzzle.reset_puzzle()
        
    def _on_imageclick(self, event):
        if self.puzzle.input_allowed:
            dlg = wx.FileDialog(self, "Open sketch file...",
                os.getcwd(), style=wx.OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
                self.puzzle.set_image(filename)
                self.GetSizer().Fit(self)
            dlg.Destroy()

    def _on_solveclick(self, event):
        if self.puzzle.input_allowed:
            SolverThread(self).start()

class SolverThread(threading.Thread):
    def __init__(self, frame):
        threading.Thread.__init__(self)
        self.frame = frame
        
    def run(self):
        self.frame.puzzle.input_allowed = False
        problem = NPuzzleProblem(self.frame.puzzle.model.size,
                                 self.frame.puzzle.model)
        agent = NPuzzleAgent(problem)
        solution = agent.astar_search(max_depth=32)
        for action in solution.actions:
            self.frame.puzzle.model = self.frame.puzzle.model.do_action(*action)
            self.frame.puzzle.reinit_buffer = True
            time.sleep(1.0)
        self.frame.puzzle.solved = True
        self.frame.puzzle.input_allowed = True



if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = EightPuzzleFrame(None)
    frame.Show()
    app.MainLoop()
    