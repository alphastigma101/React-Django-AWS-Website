import axios from 'axios';
import React, { useState, useEffect } from 'react';

export default function Game() {
  const [history, setHistory] = useState([Array(9).fill(null)]);
  const [currentMove, setCurrentMove] = useState(0);
  const [log, setLog] = useState({});
  const [loggingCreated, setLoggingCreated] = useState(false);

  let X = 0;
  let O = 0;
  let time = Date.now().toString();

  useEffect(() => {
    if (!loggingCreated) {
      logging('Creating the logging Data!');
      setLoggingCreated(true);
    }
  }, [loggingCreated]);

  function handlePlay(nextSquares) {
    const nextHistory = [...history.slice(0, currentMove + 1), nextSquares];
    setHistory(nextHistory);
    setCurrentMove(nextHistory.length - 1);

    axios.get('http://34.219.59.64:8000/polls/start_game', {
      params: { history: JSON.stringify(nextHistory) }
    }).then(response => {
      console.log('History updated successfully:', response.data);
    }).catch(error => {
      console.error('Error updating history:', error);
    });
  }

  function jumpTo(nextMove) {
    setCurrentMove(nextMove);
  }

  const currentSquares = history[currentMove];
  const xIsNext = currentMove % 2 === 0;

  const moves = history.map((squares, move) => {
    const description = move > 0 ? `Go to move #${move}` : 'Go to game start';
    return (
      <li key={move}>
        <button onClick={() => jumpTo(move)}>{description}</button>
      </li>
    );
  });

  function handleClick(i) {
    if (calculateWinner(currentSquares) || currentSquares[i]) {
      return;
    }
    const nextSquares = [...currentSquares];
    nextSquares[i] = xIsNext ? 'X' : 'O';
    handlePlay(nextSquares);
  }

  const winner = calculateWinner(currentSquares);

  useEffect(() => {
    if (Winner(winner)) {
      if (winner === 'X') { X += 1; }
      else { O += 1; }
      const winnerBoard = {
        'X': X,
        'O': O
      };
      axios.get('http://34.219.59.64:8000/polls/winner', { params: { winner_history: winnerBoard } })
        .then(response => {
          setLog(prevLog => ({
            ...prevLog,
            [time]: `History updated successfully: ${response.data}`
          }));
        })
        .catch(error => {
          setLog(prevLog => ({
            ...prevLog,
            [time]: `Error updating history: ${error}`
          }));
        });
    }
  }, [winner]);

  function logging(error) {
    if (Object.keys(log).length === 0 && log.constructor === Object) {
      setLog({ [time]: String(error) });
    } else {
      if (!log[time]) {
        setLog(prevLog => ({
          ...prevLog,
          [time]: String(error)
        }));
      }
    }

    axios.get('http://34.219.59.64:8000/polls/logging', { params: { log_history: log } })
      .then(response => {
        setLog(prevLog => ({
          ...prevLog,
          [time]: `Logged data fetched: ${response.data}`
        }));
      })
      .catch(error => {
        setLog(prevLog => ({
          ...prevLog,
          [time]: `Error fetching logs: ${error}`
        }));
      });
  }

  return (
    <div className="game">
      <div className="game-board">
        <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} />
      </div>
      <div className="game-info">
        <div className="status">{Winner(winner) ? `Winner: ${winner}` : `Next player: ${xIsNext ? 'X' : 'O'}`}</div>
        <ol>{moves}</ol>
      </div>
    </div>
  );
}

function Board({ xIsNext, squares, onPlay }) {
  function handleClick(i) {
    if (calculateWinner(squares) || squares[i]) {
      return;
    }
    const nextSquares = [...squares];
    nextSquares[i] = xIsNext ? 'X' : 'O';
    onPlay(nextSquares);
  }

  return (
    <>
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

function Square({ value, onSquareClick }) {
  return (
    <button className="square" onClick={onSquareClick}>
      {value}
    </button>
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
  return winner != null;
}

