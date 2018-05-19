# A game server for m,n,k games like Tic-Tac-Toe

M,n,k games beyond the simplest 3,3,3 version most people played as children
are largely of mathematical interest.  However, as they become more larger
and especially if you start playing in dimensions > 2, tactics and strategy
can become very important.

You can read more about tic-tac-toe like games at:
[Wikipedia](https://en.wikipedia.org/wiki/M,n,k-game)

This game server is designed to be autonomous.  It runs in one of three modes by
executing one of the scripts supplied with the client
after you've configured the client to talk to a server.
It can operate in player-vs-player mode by having one client execute the `./create`
script, and another execute the `./join [uuid-key]` command that the first will
supply in its output.  In the final mode, you can enter the tournament lobby on the
server by executing `./lobby`.  Your client will then wait for the tournament to
start and play games under direction of the server.

Because the server uses webhook calls back to the client, it's important that the
client and server be able to reach each other for http requests (both directions).
If they're on opposite sides of NAT's, firewalls, etc then it's likely the server
will be unable to make requests back to the client.

## Getting the Software and its Dependencies

* Install homebrew (or equivalent package manager on windows or linux)
  * Mac OSX
    * https://brew.sh/
    * `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
  * `brew install python@2`
* The following is only necessary if you want to maintain separate python environments for dependencies
  * `brew install pyenv`
  * `brew install pyenv-virtualenv`
* `git clone git@github.com:anthonyclifton/n-dimensional-tic-tac-toe.git t3server`
* The following is only necessary if you want to maintain separate python environments for dependencies
  * `cd t3server`
  * `pyenv install 2.7.13`
  * `pyenv virtualenv 2.7.13 t3server`
  * `pyenv local t3server`
  * `pyenv local` (to verify you're using the environment you specified)
* `pip install -Ur requirements.txt` (should download lots of fun dependencies)

## Game Flow

* Player versus Player Mode
  * Execute `./create` on a client to create a new game
  * The create client sends an http post the game server, notifying it that a new
  game should be started.
  * The server responds with the empty game object (no moves yet).
  * The create client starts a web server so it can listen for game updates.
  * Execute `./join [game-uuid-key]` on another client to the join that game.
  When you create a game it will provide output with the join command followed by
  the relevant game key
  * The join client sends an http post to the game server, notifying it that it
  wants to join the game created by the create client.
  * The server responds with the empty game object (no moves yet).
  * The join client starts a web server so it can listen for game updates.
  * The server sends an http post to the create client with the game object.
  * The create client responds with its move after analyzing the board.
  * The server sends an http post to the join client with the game object and
  the create client's move.
  * (Note that the create client always plays X and the join client always plays O).
  * The server continues back and forth, sending updates to the clients and receiving
  the client's move as the response.
  * This continues until the board is full or the game is won, in which case final
  game updates are sent to both clients with the value of the `state` key set to 4
  (or GAME_COMPLETED).  While in the play the `state` is set to 1 (or GAME_INPROGRESS).
* Tournament Mode
  * Execute `./lobby` on each client you'd like to have participate in a tournament.
  * Each client sends an http post to the game server, notifying it that it would like
  to enter the tournament lobby.
  * The server responds to each client with the player object.
  * When the tournament master sends an post to the `http://server-host:server-port/tournament`
  endpoint, a new tournament is created with the players in the lobby at that time.
  Players who
  subsequently enter the lobby cannot participate in that tournament.
  * When the tournament master sends a post to `http://server-host:server-port/round`
  the server starts a round.
  * The server generates every combination of 2 players from all the players in the lobby.
  * From each of these combinations, it starts a new game.
  * This game operates the same as in player-vs-player mode, with the server alternating
  between the two clients participating in the game, posting to their /update endpoints
  and receiving back their moves.
  * When all the games in a round are completed, the server displays the results of
  each individual game and of the round as a whole.
  * Subsequent rounds can also be executed.  It is possible to adjust the round's
  board size and winning line length in the post body so that rounds can increase in
  difficulty.
  * When the tournament master sends a delete to `http://server-host:server-port/tournament`
  all tournaments are closed and the results of each tournament are displayed on the
  server's output.

## Running the Server

* You can run the server locally by executing the `run.sh` script in its project directory.
* The server will run on port 3334.
* If you just do `./create` and `./join` it will run automatically.
* If you wish to run it in tournament mode, then you will need to install Postman so you
can do some GETs and POSTs to control it.
* `GET http://localhost:3334/lobby` will give you a list of everyone in the lobby.
* `POST http://localhost:3334/tournament` will allow you to create a tournament.  You must
supply an `application/json` raw post body like the following:

`{
	"tournament_name": "Test Tournament 5"
}`

* `POST http://localhost:3334/round` will start a game round.  The server will run
one game at a time for each pair of player participants.  You can run as many rounds
as you want by executing the request multiple times.  You can configure each round
by supplying a post body with the tournament key like the following:

`{
	"tournament_key": "8fd11a8d-687d-4487-b773-4c86d8d5c624",
	"x_size": 3,
	"y_size": 3,
	"winning_length": 3
}`

* `DELETE http://localhost:3334/tournament` will complete the tournament and display
tournament results on stdout.

## Notes

* Sending a move that is outside the boundary of the game board will result in a draw.
* The points assigned to the round are the larger of the X and Y dimensions of the board
divided by 3 and multiplied by 2.
* On a draw, the points are split 50/50 between the game participants.

