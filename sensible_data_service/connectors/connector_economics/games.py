# -*- coding: UTF-8 -*-

# This got more complicated than intended...
class Game(object):
    def __init__(self, allowed_answers):
        self.allowed_answers = allowed_answers

    def answer_allowed(self, answer):
        return answer in self.allowed_answers

class DictatorGame(Game):
    def __init__(self):
        super(DictatorGame, self).__init__(allowed_answers={'give': True, 'share': True, 'keep': True})

    def outcome(answers):
        pass 


class PrisonersDilemmaGame(Game):
    def __init__(self):
        super(PrisonersDilemmaGame, self).__init__(allowed_answers={'give': True, 'keep': True})

    def outcome(self, answers):
        users = dict([(answer['user'],0) for answer in answers])

        for i in (0,1):
            if answers[i]['answer'] == "give":
                users[answers[(i+1)%2]['user']] += 2 # (i+1)%2 makes i=0 -> 1 and i=1 -> 0 
            elif answers[i]['answer'] == "keep":
                users[answers[i]['user']] += 1

        return users


def get_game(type):
    if type == 'game-pdg':
        return PrisonersDilemmaGame()
    elif type == 'game-dg-responder' or type == 'game-dg-proposer':
        return DictatorGame()

def clean_game(game):
    return {'_id': str(game['_id']),
              'type': game['type'],
              'participants': len(game['participants']),
              'started': game['started']}

def get_outcome(game):
    G = get_game(game['type'])
    return G.outcome(game['answers'])


if __name__=="__main__":
    dg = PrisonersDilemmaGame()
    print repr(dg.answer_allowed("give"))
    print repr(dg.answer_allowed("test"))
