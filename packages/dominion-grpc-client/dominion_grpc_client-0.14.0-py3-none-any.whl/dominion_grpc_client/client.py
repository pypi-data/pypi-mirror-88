import json
import time

import multiprocessing as mp
from threading import Thread

import grpc

from dominion_object_model import object_model
from dominion_grpc_proto import dominion_pb2_grpc
from dominion_grpc_proto.dominion_pb2 import PlayerInfo, Card, ActionResponse


class Client(object_model.GameClient):
    def __init__(self,
                 name,
                 in_queue: mp.Queue,
                 out_queue: mp.Queue,
                 out_response_queue: mp.Queue):
        self.name = name
        self._in_queue = in_queue
        self._out_queue = out_queue
        self._out_response_queue = out_response_queue
        self._server = None

    def _process_incoming_messages(self, host, port):
        """ """
        try:
            with grpc.insecure_channel(f'{host}:{port}') as channel:
                self._server = dominion_pb2_grpc.DominionServerStub(channel)
                messages = self._server.Join(PlayerInfo(name=self.name))
                while True:
                    for message in messages:
                        try:
                            data = json.loads(message.data) if message.data else ''
                            self._in_queue.put((message.type, data))
                        except Exception as e:
                            print(exception=e)
        except Exception as ee:
            print(exception=ee)

    def _process_outgoing_messages(self):
        """ """
        while True:
            if not self._out_queue.empty():
                action, data = self._out_queue.get_nowait()
                if action == 'play_action_card':
                    self.play_action_card(data)
                elif action == 'buy':
                    self.buy(data)
                elif action == 'done':
                    self.done()
                elif action == 'start_game':
                    self.start_game()
                else:
                    raise RuntimeError('Unknown action in out queue: ' + action)

            if not self._out_response_queue.empty():
                action, data = self._out_response_queue.get_nowait()
                if action == 'respond':
                    self.respond(*data)
                else:
                    raise RuntimeError('Unknown action in response queue: ' + action)

    def run(self, host='localhost', port=50051):
        Thread(target=self._process_outgoing_messages).start()
        self._process_incoming_messages(host, port)

    def start_game(self):
        pi = PlayerInfo(name=self.name)
        self._server.Start(pi)

    def respond(self, action, response):
        card = Card(name=action)
        payload = json.dumps(response)
        response = ActionResponse(card=card, payload=payload)
        self._server.Respond(response)

    # GameClient interface
    def play_action_card(self, card_name):
        self._server.PlayCard(Card(name=card_name))

    def buy(self, card_type):
        self._server.Buy(Card(name=card_type))

    def done(self):
        self._server.Done(PlayerInfo(name=self.name))
