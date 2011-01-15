
import os
import time
import threading

import wx

from EightPuzzleWindow import *


class EightPuzzleFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Eight Puzzle")
        self._arrage_widgets()
        self._event_handers()
        self.agent_thread = None

    def _arrage_widgets(self):
        sizer = wx.GridBagSizer(hgap=10, vgap=10)
        self.puzzle = EightPuzzle(self, size=None, filename='funny-cat.jpg',
            puzzle_size=3, free_piece=8)
        _, btn_h = wx.Button.GetDefaultSize()
        self.btn_new = wx.Button(self, label='New Puzzle', size=(100, btn_h))
        self.btn_image = wx.Button(self, label='New Image', size=(100, btn_h))
        self.btn_solve = wx.Button(self, label='Solve', size=(100, btn_h))
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
        self.puzzle.reset_puzzle()

    def _on_imageclick(self, event):
        dlg = wx.FileDialog(self, "Open sketch file...",
            os.getcwd(), style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            self.puzzle.set_image(filename)
            self.GetSizer().Fit(self)
        dlg.Destroy()

    def _agent_finished(self):
        self.agent_thread = None
        self.btn_new.Enable()
        self.btn_image.Enable()
        self.btn_solve.SetLabel('Solve')
        self.puzzle.Bind(wx.EVT_LEFT_DOWN, self.puzzle._on_leftdown)

    def _on_solveclick(self, event):
        if not self.agent_thread:
            self.btn_new.Disable()
            self.btn_image.Disable()
            self.btn_solve.SetLabel('Stop')
            self.agent_thread = SolverThread(self, self.puzzle.model)
            self.agent_thread.start()
            self.puzzle.Unbind(wx.EVT_LEFT_DOWN)
        else:
            self.agent_thread.stop()


class SolverThread(threading.Thread):
    def __init__(self, frame, puzzle):
        threading.Thread.__init__(self)
        self.time_to_quit = threading.Event()
        self.time_to_quit.clear()
        problem = NPuzzleProblem(puzzle.size, puzzle)
        self.agent = NPuzzleAgent(problem)
        self.frame = frame

    def stop(self):
        self.agent.keep_working = False
        self.time_to_quit.set()

    def run(self):
        solution = self.agent.astar_search(max_depth=80)
        if solution:
            for (r, c, _) in solution.actions:
                if self.time_to_quit.is_set():
                    break
                wx.CallAfter(self.frame.puzzle.move_tile, r, c)
                time.sleep(1.0)
        wx.CallAfter(self.frame._agent_finished)


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = EightPuzzleFrame(None)
    frame.Show()
    app.MainLoop()
