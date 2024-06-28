import random
from .models import TournamentMatch, Lobby

def create_tournament_match(tournament, playerList):
    match_lobby = Lobby.objects.create()
    player1 = playerList.pop()
    player2 = playerList.pop() if len(playerList) > 0 else None
    winner = player1 if player2 is None else None
    finished = False if player2 is not None else True
    match = TournamentMatch.objects.create(
        round=tournament.current_round,
        player1=player1,
        player2=player2,
        winner=winner,
        lobby_id=match_lobby.uuid,
        finished=finished
    )
    print(f"match: {match}")
    tournament.matchups.add(match)
    tournament.save()

def get_round_winners(tournament):
    winners = []
    for match in tournament.matchups.filter(round=tournament.current_round - 1):
        if match.winner == match.player1:
            winners.append(match.player1)
        else:
            winners.append(match.player2)
    print(f"winners: {winners}")
    winners.reverse()
    return winners

def generate_bracket(tournament):
    if tournament.current_round == 1:
        participants = list(tournament.participants.values_list('tournament_username', flat=True))
        random.shuffle(participants)
    else:
        participants = get_round_winners(tournament)

    while len(participants) >= 1:
        create_tournament_match(tournament, participants)

    tournament.save()

# import random
# from .models import TournamentMatch, Lobby

# def create_tournament_match(tournament, player1, player2):
#     match_lobby = Lobby.objects.create()
#     winner = player1 if player2 is None else None
#     finished = False if player2 is not None else True
#     match = TournamentMatch.objects.create(
#         round=tournament.current_round,
#         player1=player1,
#         player2=player2,
#         winner=winner,
#         lobby_id=match_lobby.uuid,
#         finished=finished
#     )
#     tournament.matchups.add(match)
#     tournament.save()

# def get_round_winners(tournament):
#     winners = []
#     for match in tournament.matchups.filter(round=tournament.current_round - 1):
#         if match.winner == match.player1:
#             winners.append(match.player1)
#         else:
#             winners.append(match.player2)
#     print(f"Winners: {winners}")
#     return winners

# def generate_bracket(tournament):
#     if tournament.current_round == 1:
#         participants = list(tournament.participants.values_list('tournament_username', flat=True))
#         random.shuffle(participants)
#     else:
#         participants = get_round_winners(tournament)

#     # Ensure an even number of participants for pairing
#     if len(participants) % 2 != 0:
#         participants.append(None)

#     for i in range(0, len(participants), 2):
#         player1 = participants[i]
#         player2 = participants[i + 1] if i + 1 < len(participants) else None
#         create_tournament_match(tournament, player1, player2)

#     tournament.save()
