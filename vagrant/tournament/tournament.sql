-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
create table tournaments
    (id serial primary key,
    name text not null,
    total_number_of_players integer not null,
    winner_id integer,
    loser_id integer);

create table matches
    (id serial primary key not null,
    player1_id integer references players (id) not null,
    player1_name text not null,
    player2_id integer references players (id) not null,
    player2_name text not null,
    winner_id integer references players (id),
    loser_id integer references players (id),
    round_number integer not null,
    tournament_id integer references tournaments (id) not null);

create table players
    (id serial primary key not null,
    name text not null,
    number_of_wins integer not null,
    number_of_losses integer not null,
    number_of_ties integer not null);

