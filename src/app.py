from src.grpc_stubs.hide_and_seek_pb2 import GameView
from src.grpc_stubs.hide_and_seek_pb2_grpc import GameHandlerStub
import logging, grpc, yaml


class GameClient:
    def __init__(self, token, stub: GameHandlerStub):
        self.token = token
        self.game_stub = stub

    def handle_client(self):
        index = 0
        try:
            for view in self.game_stub.Watch(token=self.token):
                logging.info(view)
                game_status = view.status
                index += 1
                if index == 1:
                    print(self.token)
                    try:
                        self.game_stub.DeclareReadiness(self.get_game_command(view))
                    except Exception as e:
                        print(e)
                    self.set_ai_method(view)
                elif game_status == GameView.ONGOING:
                    try:
                        self.send_message(view)
                        self.move(view)
                    except Exception as e:
                        print(e)
                elif game_status == GameView.FINISHED:
                    self.channel.unsubscribe(lambda _: None)

        except Exception as e:
            print(e)
            self.channel.unsubscribe()
            exit()

    def send_message(self, view: GameView):
        pass

    def move(self, view: GameView):
        pass

    def set_ai_method(self, view: GameView):
        pass

    def get_game_command(self, view: GameView):
        pass


def run():
    config = {}

    with open("./config/application.yml", "r") as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)

    with grpc.insecure_channel(f"{config['grpc']['server']}:{config['grpc']['port']}") as channel:
        game_stub = GameHandlerStub(channel)

    client = GameClient(token=f"{config['grpc']['token']}", stub=game_stub)
    client.handle_client()


if __name__ == "__main__":
    run()
