import logging
import traceback

import grpc
import yaml

from src.grpc_stubs import hide_and_seek_pb2_grpc
from src.grpc_stubs.hide_and_seek_pb2 import WatchCommand, GameStatus, TurnType, AgentType, MoveCommand, \
    GameView, DeclareReadinessCommand, ChatCommand


class GameClient:
    __slots__ = (
        'token', 'channel', 'has_moved', 'turn_number', 'ai', 'stub', 'server_address', 'ai_move_method')

    def __init__(self, token: str, server_address: str, ai=None) -> None:
        self.server_address = server_address
        self.channel = grpc.insecure_channel(self.server_address)
        self.stub = hide_and_seek_pb2_grpc.GameHandlerStub(channel=self.channel)
        self.ai = ai
        self.token = token
        self.has_moved = False
        self.turn_number = 1
        self.ai_move_method = None

    def handle_client(self):
        index = 0
        watch_command = WatchCommand(token=self.token)
        try:
            for view in self.stub.Watch(watch_command):
                self.check_and_end_the_game(view)
                if view.turn.turnNumber != self.turn_number:
                    self.turn_number = view.turn.turnNumber
                    self.has_moved = False
                logging.info(view)
                index += 1
                if index == 1:
                    print(self.token)
                    try:
                        self.stub.DeclareReadiness(self.get_join_game_command(view))
                    except Exception as e:
                        print(str(e))
                    self.set_ai_methods(view)
                elif self.check_if_is_client_turn_to_move(view):
                    self.move(view)
        except Exception:
            print(traceback.format_exc())
            self.channel.unsubscribe(None)
            exit()

    def check_and_end_the_game(self, view):
        if view.status == GameStatus.FINISHED:
            self.channel.unsubscribe(lambda _: None)

    def check_if_is_client_turn_to_move(self, view: GameView):
        if view.status == GameStatus.ONGOING and not self.has_moved:
            if view.turn.turnType == TurnType.THIEF_TURN and view.viewer.type == AgentType.THIEF:
                return True
            if view.turn.turnType == TurnType.POLICE_TURN and view.viewer.type == AgentType.POLICE:
                return True
            return False
        return False

    def move(self, view):
        node_id = self.ai_move_method(view)
        move_command = MoveCommand(token=self.token, toNodeId=node_id)
        if move_command:
            try:
                self.stub.Move(move_command)
                self.has_moved = True
            except Exception as e:
                print(e)

    def send_message(self, message):
        chat_command = ChatCommand(token=self.token, text=message)
        try:
            self.stub.SendMessage(chat_command)
        except Exception as e:
            print(e.__repr__())

    def get_join_game_command(self, view: GameView) -> DeclareReadinessCommand:
        player = view.viewer
        agent_type = player.type
        if agent_type == AgentType.THIEF:
            from src import AI
            start_node_id = AI.get_thief_starting_node(view)
            return DeclareReadinessCommand(token=self.token, startNodeId=start_node_id)
        else:
            return DeclareReadinessCommand(token=self.token, startNodeId=1)

    def set_ai_methods(self, view: GameView) -> None:
        from src.AI import AI,Phone
        self.ai = AI(Phone(self))
        viewer_type = view.viewer.type
        if viewer_type == AgentType.THIEF:
            self.ai_move_method = self.ai.thief_move_ai
        else:
            self.ai_move_method = self.ai.police_move_ai


def main():
    with open("./config/application.yml", "r") as config_file:
        cfg = yaml.load(config_file, Loader=yaml.FullLoader)
    server_address = f"{cfg['grpc']['server']}:{cfg['grpc']['port']}"
    token = cfg['grpc']['token']
    client = (GameClient(token=token, server_address=server_address))
    client.handle_client()


if __name__ == '__main__':
    main()
