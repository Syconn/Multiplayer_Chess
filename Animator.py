import pygame


class ImageAnimation:

    def __init__(self, texture_path : str, extension : str, frames : int, square_size : int, scale : int, time_limit : int):
        self._frame = 0
        self._timer = frames
        self._timer_limit = time_limit
        self._frames = frames
        self._texture_path = texture_path
        self._ext = extension
        self._upscale = scale * square_size
        self._images = [pygame.transform.scale(pygame.image.load(self._texture_path + str(f + 1) + self._ext),(self._upscale, self._upscale)) for f in range(frames)]

    def animate(self, screen, pos : tuple[int, int]):
        screen.blit(self._images[self._frame], (pos[0] * self._upscale, pos[1] * self._upscale))
        self._timer -= 1
        if self._timer <= 0:
            self._timer = self._timer_limit
            self._frame = (self._frame + 1) % self._frames

    def single_play(self, screen, pos : tuple[int, int]):
        screen.blit(self._images[self._frame], (pos[0] * self._upscale, pos[1] * self._upscale))
        self._timer -= 1
        if self._timer <= 0 and self._frame >= 1:
            self._timer = self._timer_limit
            self._frame -= 1