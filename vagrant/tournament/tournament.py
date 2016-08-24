#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from itertools import tee, izip
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("delete from matches")
    cursor.execute("update players set number_of_wins = 0 ,number_of_losses = 0,number_of_ties = 0")
    connection.commit()
    cursor.close()
    connection.close()



def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("delete from players")
    connection.commit()
    cursor.close()
    connection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("select count(*) as player_count from players")
    player_count = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return player_count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        "Insert into players (name, number_of_wins, number_of_losses, number_of_ties) values (%s,%s,%s,%s)",
        (name,0,0,0)
    )
    connection.commit()
    cursor.close()
    connection.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        "select id, name, number_of_wins, (number_of_wins + number_of_losses + number_of_ties) as matches from players order by number_of_wins desc"
    )
    rows = cursor.fetchall()
    player_standings = [(row[0], row[1], row[2], row[3]) for row in rows]
    print player_standings
    connection.commit()
    cursor.close()
    connection.close()
    return player_standings



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("select name from players where id = (%s)",[winner])
    winner_name = cursor.fetchone()[0]
    cursor.execute("select name from players where id = (%s)", [loser])
    loser_name = cursor.fetchone()[0]
    cursor.execute(
        '''insert into matches
        (player1_id, player1_name, player2_id, player2_name, winner_id, loser_id, round_number, tournament_id)
         values (%s,%s,%s,%s,%s,%s,%s,%s)
         ''',(winner,winner_name,loser,loser_name,winner,loser,1,1)
    )
    connection.commit()
    cursor.execute("select count(*) as number_of_wins from matches where winner_id = (%s)",[winner])
    number_of_wins = cursor.fetchone()[0]
    cursor.execute("select count(*) as number_of_losses from matches where loser_id = (%s)", [loser])
    number_of_losses = cursor.fetchone()[0]
    cursor.execute("update players set number_of_wins = (%s) where id = (%s)",(number_of_wins,winner))
    cursor.execute("update players set number_of_losses = (%s) where id = (%s)",(number_of_losses,loser))
    connection.commit()
    cursor.close()
    connection.close()

 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        "select id,name from players order by (number_of_wins-number_of_losses) desc"
    )
    rows = cursor.fetchall()
    swiss_parings = []
    i=0
    for rowa, rowb in pairwise(rows):
        if((i%2) is  0):
            swiss_parings.append((rowa[0],rowa[1],rowb[0],rowb[1]))
        i=i+1
    connection.commit()
    cursor.close()
    connection.close()
    return swiss_parings





