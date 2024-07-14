//import 
import express from 'express';
import path from 'path';
import { useState, useEffect } from 'react';
import axios from 'axios';


let X = 0;
let O = 0;
let log = {};
let time = Date.now.toString();
let logging_created = false;

/*
 * Params:
      * value: Can be either X or O 
      * onSqureClick: Ending the user's turn 
 * Returns: A Updated JSX data
*/
function Square({ value, onSquareClick }) { 
  return (
    <button className="square" onClick={onSquareClick}>
    {value}
    </button>
  );
}

/*
 * Params:
    * xIsNext:
    * squares:
    * onPlay:
 * Returns: 
 */
function Board({ xIsNext, squares, onPlay }) {
  /*
   * Params:
      * i: and iteratable object that iterates through the board to find 
   * Returns:
      * Nothing. It simply displays who's turn it is 
  */
  function handleClick(i) {
    if (calculateWinner(squares) || squares[i]) {
      return;
    }
    const nextSquares = squares.slice();
    if (xIsNext) {
      nextSquares[i] = "X";
    } 
    else {
      nextSquares[i] = "O";
    }
    onPlay(nextSquares);
  }
  const winner = calculateWinner(squares);
  let status;
  if (Winner(winner) === true) {
    if (winner === "X") { X += 1; }
    else { O += 1; }
    const  winnerBoard = {
      'X': X,
      'O': O
    }
     axios.get('http://localhost:8000/polls/winner', { winner_history: winnerBoard })
      .then(response => {
        log[time] = 'History updated successfully:' + String(response.data);
      })
      .catch(error => {
        log[time] = 'Error updating history:' + String(error);
      });
  } 
  else { 
    status = "Next player: " + (xIsNext ? "X" : "O"); 
  }
  return (
            <>
                <div className="status">{status}</div>
                <div className="board-row">
                  <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
                  <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
                  <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
                </div>
                <div className="board-row">
                  <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
                  <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
                  <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
                </div>
                <div className="board-row">
                  <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
                  <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
                  <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
                </div>
            </>
        );
}

/*
 * This is the driver function
 *
*/
export default function Game() {
  const [history, setHistory] = useState([Array(9).fill(null)]);
  const [currentMove, setCurrentMove] = useState(0);
  const xIsNext = currentMove % 2 === 0;
  const currentSquares = history[currentMove];
  /*
   * Params: 
      * nextSquares:
   * Returns: 
      * Nothing. It calls another function called setCurrentMove
  */
  function handlePlay(nextSquares) {
    const nextHistory = [...history.slice(0, currentMove + 1), nextSquares];
    setHistory(nextHistory);
    setCurrentMove(nextHistory.length - 1);
    axios.get('http://localhost:8000/polls/start_game', {
      params: { history: JSON.stringify(nextHistory) }
    }).then(response => {
      console.log('History updated successfully:', response.data);
    }).catch(error => {
        console.error('Error updating history:', error);
    });
  }
  /*
   * Params:
      * nextMove: 
   * Returns:
      * Nothing. It calls in a function 
   */
  function jumpTo(nextMove) {
    setCurrentMove(nextMove);
  }

  const moves = history.map((squares, move) => {
    let description;
    if (move > 0) {
      description = "Go to move #" + move;
    } else {
      description = "Go to game start";
    }
    return (
      <li key={move}>
        <button onClick={() => jumpTo(move)}>{description}</button>
      </li>
    );
  });
  if (logging_created == false) {
    logging('Creating the logging Data!');
    logging_created = true;
  }
  return (
              <div className="game">
                <div className="game-board">
                <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} />
              </div>
              <div className="game-info">
                <ol>{moves}</ol>
              </div>
              </div>
        );
}

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}


export function Winner(winner) {
  if (winner != null) {
    return true;
  }
  return false;
}

export function logging({ error }) {
  const [message, setMessage] = useState(error);
  if (Object.keys(log).length === 0 && log.constructor === Object) {
    log[time] = String(error);                                                
  }
  else {                                                                        
    if (log[time] == undefined) {                                               
      log[time] = String(error);                                              
    }                                                                                                                                                                                                  
  }
  if (logging_created == false) {
    axios.get('http://localhost:8000/polls/logging', { log_history: { log } })
      .then(response => {
        log[time] =  'Logged data fetched:' + String(response.data);
      })
      .catch(error => {
        log[time] = 'Error fetching logs:' + String(error);
      });
  } 
  else {
    axios.get('http://localhost:8000/polls/logging', { log })
      .then(response => {
        log[time] = 'Logged data sent successfully:';
      })
      .catch(error => {
        log[time] = String(error);
      });
  }
}

app.use(express.static(path.join(__dirname, 'build')));

app.get('/', function (req, res) {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

app.listen(3000);
