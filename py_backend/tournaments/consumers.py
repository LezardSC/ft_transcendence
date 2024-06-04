import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

from users.models import CustomUser
from stats.models import Match
from .models import Tournament, TournamentMatch
from .bracket import generate_bracket

class TournamentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.tournament = await self.get_tournament()
        if self.tournament is None:
            return await self.close()
        await self.accept()
        await self.channel_layer.group_add(
            self.tournament.name,
            self.channel_name
        )
        participants = await self.get_tournament_participants()
        await self.channel_layer.group_send(
            self.tournament.name,
            {
                'type': 'tournament.participants',
                'participants': participants
            }
        )

    async def auth(self, text_data_json):
        username = text_data_json.get('username')
        user = await self.authenticate_user_with_username(username)
        if user:
            self.scope["user"] = user
            await self.send(text_data=json.dumps({"type": "auth", "status": "success"}))
            await self.check_tournament_start()
        else:
            await self.send(text_data=json.dumps({"type":"auth", "status": "failed"}))

    async def validate_foreign_keys(self):
        try:
            tournament = await Tournament.objects.aget(id=self.scope['url_route']['kwargs']['tournament_id'])
            match = await TournamentMatch.objects.aget(lobby_id=self.match.lobby_id)
            return True
        except Tournament.DoesNotExist:
            print("Tournament does not exist")
            return False
        except TournamentMatch.DoesNotExist:
            print("Match does not exist")
            return False

    async def match_is_over(self):
        if not await self.validate_foreign_keys():
            return
        self.match.finished = True
        await self.channel_layer.group_send(
            self.tournament.name,
            {
                'type': 'tournament.status',
                'status': 'endGame'
            }
        )
        await self.match.asave()

    async def send_bracket(self):
        bracket = await sync_to_async(self.tournament.get_tournament_bracket)()
        await self.send(text_data=json.dumps({'type': 'bracket', 'bracket': bracket}))

    async def handler_status(self, status):
        if status == 'endGame':

            await self.match_is_over()
            await self.set_match_info()
            await self.send_bracket()

    async def send_disqualified(self, username):
        await self.channel_layer.group_send(
            self.tournament.name,
            {
                'type': 'tournament.status',
                'status': 'disqualified',
                'username': username
            }
        )

    async def set_match_info(self):
        try:
            match = await Match.objects.aget(uuid=self.match.lobby_id)
            self.match.player1 = match.player1
            self.match.player2 = match.player2
            self.match.score_player_1 = match.player1_score
            self.match.score_player_2 = match.player2_score
            self.match.winner = match.winner
            loser = match.player1 if match.winner == match.player2 else match.player2
            await self.match.asave()
            await self.send_disqualified(loser)
        except Match.DoesNotExist:
            print("Match does not exist")
            return
        

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json.get('type') == 'auth':
            await self.auth(text_data_json)
        if text_data_json.get('type') == 'status':
            await self.handler_status(text_data_json.get('status'))


    async def disconnect(self, close_code):
        print('disconnected')
        participants = await self.get_tournament_participants()
        await self.channel_layer.group_send(
            self.tournament.name,
            {
                'type': 'tournament.participants',
                'participants': participants
            }
        )
        await self.channel_layer.group_discard(
            self.tournament.name,
            self.channel_name
        )

    @database_sync_to_async
    def get_tournament(self):
        try:
            return Tournament.objects.get(pk=self.scope['url_route']['kwargs']['tournament_id'])
        except Tournament.DoesNotExist:
            return None

    @database_sync_to_async
    def get_tournament_participants(self):
        return [p.tournament_username for p in self.tournament.participants.all()]
    
    async def launch_tournament(self):
        await self.channel_layer.group_send(
            self.tournament.name,
            {
                'type': 'tournament.status',
                'status': 'start'
            }
        )
        self.tournament.started = True
        await sync_to_async(self.tournament.save)()
        await sync_to_async(generate_bracket)(self.tournament)
        await self.send_matchups()


    async def check_tournament_start(self):
        if await self.is_tournament_full() and not self.tournament.started:
            await self.launch_tournament()
        elif self.tournament.started:
            await self.send_bracket()
    
    async def send_matchups(self):
        await self.channel_layer.group_send(
            self.tournament.name,
            {
                'type': 'tournament.matchups'
            }
        )

    @database_sync_to_async
    def is_tournament_full(self):
        if self.tournament.participants.count() == self.tournament.max_players:
            return True
        return False

    @database_sync_to_async
    def get_player_match(self, username):
        return self.tournament.get_matches_by_player(username).first()

    @database_sync_to_async
    def get_match_infos(self, match):
        return {
            'lobby_id': str(match.lobby_id),
            'player_1': match.player1,
            'player_2': match.player2 if match.player2 else None,
            'round': match.round
        }
    
    @database_sync_to_async
    def authenticate_user_with_username(self, username):
        try:
            return CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return None

    async def tournament_participants(self, event):
        await self.send(
            text_data=json.dumps({'type': 'participants', 'participants': event['participants']}))
        
    async def tournament_matchups(self, event):
        self.match = await self.get_player_match(self.scope['user'].tournament_username)
        if self.match:
            match_infos = await self.get_match_infos(self.match)
            await self.send(text_data=json.dumps({'type': 'matchup', 'match': match_infos}))

    async def tournament_status(self, event):
        if event['status'] == 'disqualified':
            print('disqualified: ', event['username'])
            if event['username'] == self.scope['user'].tournament_username:
                await self.send(text_data=json.dumps({'type': 'status', 'status': 'disqualified'}))
        else:
            await self.send(text_data=json.dumps({'type': 'status', 'status': event['status']}))
