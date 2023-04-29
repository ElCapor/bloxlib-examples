# Imports
import os
import pygame
import OpenGL.GL as gl

import imgui as imgui
from imgui.integrations.pygame import PygameRenderer
from pygameoverlay.imgui_menu import menu
import sys
import win32api
import win32con
import win32gui


"""Bloxlib imports !!"""

from bloxlib.Memory import GetDataModel
from bloxlib.instance import Instance, shared_instances
from bloxlib.Players import Players
from bloxlib.Player import Player
from bloxlib.Highlight import Highlight
from bloxlib.Camera import Vector3
class Cheat():
    def __init__(self):
        Game = Instance(GetDataModel())
        Workspace = Game.FindFirstChild("Workspace")
        PlayersService = Players(Game.FindFirstChild("Players"))
        shared_instances["Workspace"] = Workspace
        shared_instances["Players"] = PlayersService


class Overlay_menu():
    # Инициализация imgui оверлея
    def __init__(self, target_process: str) -> None:

        # Инициализация pygame
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(win32api.GetSystemMetrics(0)) + "," + str(win32api.GetSystemMetrics(1))

        # Получение hwnd выбранного процесса
        self.target_window_hwnd = win32gui.FindWindow(None, target_process)

        # Проверка на наличие процесса
        if not self.target_window_hwnd:
            print(f'Could not find window with {target_process} title')
            raise Exception(f'Could not find window with {target_process} title')

        """ Параметры оверлея """

        # Создания окна оверлея
        self.overlay_screen = pygame.display.set_mode((0, 0), pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)

        # Получение hwnd оверлея
        self.overlay_hwnd = pygame.display.get_wm_info()['window']

        # Параметры окна Windows
        win32gui.SetForegroundWindow(self.overlay_hwnd)
        win32gui.SetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW)
        win32gui.SetLayeredWindowAttributes(self.overlay_hwnd, 0, 255, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)
        win32gui.BringWindowToTop(self.overlay_hwnd)
        win32gui.SetWindowPos(self.overlay_hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 1 | 2)
        win32gui.ShowWindow(self.overlay_hwnd, win32con.SW_SHOW)

        """ Интерфейс ImGui """

        # Инициализация ImGui
        imgui.create_context()
        self.impl = PygameRenderer()

        # Установка размера дисплея ImGui
        self.io = imgui.get_io()
        self.io.display_size = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

        # Очистака пиксельной сетки OpenGL
        gl.glColorMask(True, True, True, True)
        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # Сохранение размера окна
        self.window_size_save = ""

        self.Game = Instance(GetDataModel())
        self.Workspace = self.Game.FindFirstChild("Workspace")
        self.PlayersService = Players(self.Game.FindFirstChild("Players"))
        shared_instances["Workspace"] = self.Workspace
        shared_instances["Players"] = self.PlayersService
        self.FillColor = [1.0,0.0,0.0]
        self.isEsp = False

    def update_overlay_menu(self, menu_status: bool):
        win32gui.SetWindowPos(self.overlay_hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 1 | 2)
        window_rect = win32gui.GetWindowRect(self.target_window_hwnd)
        window_size = window_rect[2] - window_rect[0], window_rect[3] - window_rect[1]

        if self.window_size_save != window_size:
            pygame.display.set_mode(window_size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE | pygame.NOFRAME)
            self.io.display_size = (window_size[0], window_size[1])

        self.window_size_save = window_size

        win32gui.MoveWindow(self.overlay_hwnd, window_rect[0], window_rect[1], window_size[0], window_size[1], True)

        for event in pygame.event.get():
            # pygame.event.get()
            self.impl.process_event(event)

        imgui.new_frame()

        # if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == self.target_window_hwnd:
            
        if menu_status:
            imgui.set_next_window_size(250, 250)
            # imgui.set_next_window_position(50, 50)
            imgui.begin(
                "Bloxlib - Overlay Demo",
                # imgui.WINDOW_NO_MOVE
                flags=imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_SAVED_SETTINGS)
            imgui.text("Demo of an ESP made with bloxlib in python !")
            changed , self.FillColor = imgui.color_edit3("Fill Color",
                                                         *self.FillColor)
            clicked, self.isEsp = imgui.checkbox(label="ESP ", state=self.isEsp)
            if self.isEsp:
                if self.Game: # we got the game
                    for player in self.Workspace.FindFirstChild("Players").FindFirstChild("Bright orange").GetChildren():
                        if player and player.HasChildren():
                            if not player.FindFirstChildOfClass("Highlight"):
                                newStuff = Highlight(Instance().new("Highlight"))
                                newStuff.SetProperty("Parent", player.getAddress())
                                newStuff.SetFillColor(Vector3(self.FillColor[0], self.FillColor[1], self.FillColor[2]))

            
            # if imgui.checkbox

            imgui.end()
            #imgui.show_test_window()

        # Очистака пиксельной сетки OpenGL
        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # Рендер
        imgui.render()
        self.impl.render(imgui.get_draw_data())

        # Обновление окна
        pygame.display.flip()
        win32gui.BringWindowToTop(self.overlay_hwnd)
        win32gui.ShowWindow(self.overlay_hwnd, win32con.SW_SHOW)