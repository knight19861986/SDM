# -*- coding: utf-8 -*-
from GameAssistant.gameboards.boards import Role, Board

class Werewolf(Board):
    name = 'Werewolf'
    roles = [
        Role('Moderator','The game of Mafia is run by a moderator, who does not participate as a player'),

        Role('Odinary Townfolk','Odinary Townfolks don\'t have any special power except thinking and the right to vote.',6),

        Role('Seer','Each night, they can discover the real identity of a player. '),
        Role('Hunter','If they are killed by werewolves or eliminated by vote, they must immediately kill another player of their choice.'),
        Role('Witch','She has two potions: to save the werewolves\'s victim; or to eliminate a player'),
        Role('Ancient',''),
        Role('Idiot',''),
        Role('Savior',''),        
        Role('Fox',''),
        Role('Bear',''),
        Role('Nine-Tailed Fox',''),
        Role('Magician',''),

        Role('Werewolf','Each night, the werewolves pick 1 player to kill.',6),
        Role('Werewolf Beauty',''),
        Role('White Werewolf',''),
        Role('Werewolf King',''),
        Role('Demon',''),

        Role('Cupid',''),
        Role('Thief','')

    ]

