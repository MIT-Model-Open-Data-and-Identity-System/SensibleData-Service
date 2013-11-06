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


class PrisonersDilemmaGame(Game):
    def __init__(self):
        super(PrisonersDilemmaGame, self).__init__(allowed_answers={'give': True, 'keep': True})


def get_game(type):
    if type == 'pdg':
        return PrisonersDilemmaGame()
    elif type == 'dg-responder' or type == 'dg-proposer':
        return DictatorGame()

if __name__=="__main__":
    dg = DictatorGame()
    print repr(dg.answer_allowed("give"))
    print repr(dg.answer_allowed("lol"))
