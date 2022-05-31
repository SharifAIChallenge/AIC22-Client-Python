from src.grpc_stubs.hide_and_seek_pb2 import GameView
from src.grpc_stubs.hide_and_seek_pb2_grpc import GameHandlerStub
import logging, grpc, yaml


class GameClient:
    def __init__(self, token, stub: GameHandlerStub, view: GameView):
        pass

    def handle_client(self, view: GameView):
        pass

    def send_message(self, view: GameView):
        pass

    def move(self, view: GameView):
        pass

    def set_ai_method(self, view: GameView):
        pass

    def get_game_command(self, view: GameView):
        pass


def run():
    pass


if __name__ == "__main__":
    run()
