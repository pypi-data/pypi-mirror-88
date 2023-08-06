import io
import socket
from random import random
from select import select
from threading import Thread

from loguru import logger
from pydantic import BaseModel, ValidationError
import orjson
from typing import List, Tuple
import pygame
from base64 import b64decode
import typer


class ApiModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = lambda v, default: orjson.dumps(v, default=default).decode()


class Face(ApiModel):
    image_src: str


class FacesFrame(ApiModel):
    faces: List[Face]
    timestamp_taken: str
    timestamp_processed: str


def load_image(face: Face) -> Tuple['pygame.image', int, int]:
    img_bytes = b64decode(face.image_src)
    img = pygame.image.load((io.BytesIO(img_bytes)))
    width, height = img.get_rect().size
    return img, width, height


def render_frame(screen, frame, screen_width: int, screen_height: int, use_original_width: bool):
    screen.fill((0, 0, 0))
    cur_x = 0
    for face in frame.faces:
        img, width, height = load_image(face)
        act_width = int(width * screen_height / height) if not use_original_width else width
        img = pygame.transform.scale(img, (act_width, screen_height))
        screen.blit(img, (cur_x, 0))
        cur_x += act_width


class MessageReader:

    def __init__(self, connection, buffer_size):
        self._connection = connection
        self._buffer_size = buffer_size
        self._buffer = ''

    def next_message(self):
        recv = ''
        while '\n' not in recv:
            recv = self._connection.recv(self._buffer_size).decode()
            if not recv:
                self._connection.close()
                return None
            self._buffer += recv
        message, self._buffer = self._buffer.split('\n', maxsplit=1)
        return message


def check_quit():
    if pygame.QUIT in (e.type for e in pygame.event.get()):
        pygame.quit()
        raise typer.Exit()
    return True


def run(host: str = typer.Option(default='0.0.0.0'), port: int = typer.Option(default=9000),
        width: int = typer.Option(default=1000), height: int = typer.Option(default=300),
        use_original_width: bool = typer.Option(default=False),
        buffer_size: int = typer.Option(default=20480)):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()

    while check_quit():
        logger.info(f'Listening on {host}:{port}')
        connection, address = sock.accept()
        reader = MessageReader(connection, buffer_size)
        while check_quit():
            msg = reader.next_message()
            if not msg:
                break
            try:
                frame = FacesFrame.parse_raw(msg)
            except ValidationError:
                logger.warning(f'Exception occurred when parsing frame.')
                break
            render_frame(screen, frame, width, height, use_original_width)
            pygame.display.update()
            logger.info(f'Rendered frame {frame.timestamp_taken}'
                        f' {frame.timestamp_processed}')


def main():
    typer.run(run)
