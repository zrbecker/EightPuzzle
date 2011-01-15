
import wx

from NPuzzleState import *
from NPuzzleAgent import *


class EightPuzzle(wx.Window):
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition,
            size=(300, 300), puzzle_size=3, free_piece=0, filename=""):
        wx.Window.__init__(self, parent, id, pos, size)
        self.filename = filename
        self.puzzle_size = puzzle_size
        self.free_piece = free_piece
        self.use_picture_size = (size == None)
        self._init_image()
        self._init_puzzle()
        self._init_buffer()
        self._event_handlers()

    def reset_puzzle(self):
        self._init_puzzle()
        self.reinit_buffer = True

    def set_image(self, filename):
        self.filename = filename
        self._init_image()
        self.reinit_buffer = True

    def set_puzzle_size(self, puzzle_size):
        self.puzzle_size = puzzle_size
        self._init_puzzle()
        self.reinit_buffer = True

    def set_free_piece(self, free_piece):
        self.free_piece = free_piece
        self._init_puzzle()
        self.reinit_buffer = True

    def move_tile(self, row, col):
        for (r, c, a) in self.model.valid_moves():
            if r == row and c == col:
                self.model = self.model.do_action(r, c, a)
                self.reinit_buffer = True
                break
        if self.model.is_solved():
            self.solved = True

    def tile_size(self):
        window_width, window_height = self.GetClientSize()
        return (window_width / self.puzzle_size,
                window_height / self.puzzle_size)

    def _init_image(self):
        self.raw_image = wx.Image(self.filename)
        if self.raw_image.Ok():
            if self.use_picture_size:
                w, h = self.raw_image.GetSize()
                if w > 640:
                    ratio = float(h) / w
                    w = 640
                    h = w * ratio
                if h > 480:
                    ratio = float(w) / h
                    h = 480
                    w = h * ratio
                self.SetInitialSize((w, h))
        else:
            self.raw_image = None

    def _init_puzzle(self):
        self.solved = False
        self.model = RandomNPuzzleState(self.puzzle_size, self.free_piece)

    def _init_buffer(self):
        self.buffer = wx.EmptyBitmap(*self.GetClientSize())
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush('Black'))
        dc.Clear()
        self._make_tiles()
        self._draw_scene(dc)
        self.reinit_buffer = False

    def _draw_scene(self, dc):
        tile_width, tile_height = self.tile_size()
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
            if self.raw_image:
                image = self.raw_image.Copy()
                image.Rescale(*self.GetClientSize())
                image = image.ConvertToBitmap()
                row = number // self.puzzle_size
                col = number % self.puzzle_size
                self.tiles[number] = \
                    ImageTile(row, col, image, self.tile_size())
            else:
                self.tiles[number] = NumberTile(number, self.tile_size())

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
        if self.reinit_buffer:
            self._init_buffer()
            self.Refresh(False)

    def _on_leftdown(self, event):
        if not self.model.is_solved():
            mouse_x, mouse_y = event.GetPositionTuple()
            tile_width, tile_height = self.tile_size()
            row = int(mouse_y / tile_height)
            col = int(mouse_x / tile_width)
            self.move_tile(row, col)


class NumberTile(object):
    def __init__(self, number, size=(100, 100)):
        self.number = number
        self.size = size
        self._make_bitmap()

    def _make_bitmap(self):
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
        self._make_bitmap()

    def _make_bitmap(self):
        w, h = self.size
        self.bmp = wx.EmptyBitmap(w, h)
        srcdc = wx.MemoryDC(self.bitmap)
        dstdc = wx.MemoryDC(self.bmp)
        dstdc.SetBackground(wx.Brush('Black'))
        dstdc.Clear()
        dstdc.Blit(0, 0, w, h, srcdc, self.column * w, self.row * h)
        srcdc.SelectObject(wx.NullBitmap)
        dstdc.SelectObject(wx.NullBitmap)
    