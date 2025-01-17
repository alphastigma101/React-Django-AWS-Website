import axios from 'axios';
import React, { useState, useEffect } from 'react';

// Create objects that do not need to be a component
let X = 0;
let O = 0;
const remote = 0;
/*
 * (Game): This is driver function for my react app. It starts the game up.
 * Params:
    *  None
 * Returns:
    * None
 */
export default function Game() {
  // Components are basically functions in a way
  // So from left to right, you have the getter and then you have the setter that will update the rendering 
  const [history, setHistory] = useState([Array(9).fill(null)]);   // Set the history component as an array instance
  const [currentMove, setCurrentMove] = useState(0);
  const [log, setLog] = useState({});
  const [loggingCreated, setLoggingCreated] = useState(false);

  // Mount the react component to record logging for it 
  useEffect(() => {
    if (!loggingCreated) {
      logging('Creating the logging Data!');
      setLoggingCreated(true);
    }
  }, [loggingCreated]);
  /*
   * (handlePlay): Is a private function of the Game Function
   * Params:
      *  nextSquares: 
  */
  function handlePlay(nextSquares) {
    const nextHistory = [...history.slice(0, currentMove + 1), nextSquares];
    setHistory(nextHistory);
    setCurrentMove(nextHistory.length - 1);
    // Make a post request and send the history data to the Django API End Point
    const sendHistory = async (data) => {
      if (remote === 1) {
        try {
          // Check to see if EC2 is up and running
          const response  = await axios.post('http://52.41.13.5/polls/start_game', JSON.stringify(nextHistory));
          console.log('History updated successfully:', response.data);
        } catch(error) {
            logging(String(error));
        }
      }
      else {
        try {
          // Check to see if the app is running locally
          const response = await axios.post('http://localhost:8000/polls/start_game', data);
          console.log('History updated successfully:', response.data);
        } catch(error) { 
            logging(String(error));
          }
        }
    }
    console.log("Sending History data to Django API endpoint!");
    logging("Testing to see if the logging api is working. If you see this, it is working as excepted.");
    console.log(nextHistory);
    
    // Check if nextHistory is not empty before sending it
    if (nextHistory.length > 0) {
      console.log("Sending History data to Django API endpoint!");
      console.log(nextHistory);
      sendHistory(nextHistory);
    }
  }
  /*
   * (jumpTo): Is a private function of Game Function
   * Params:
      * nextMove: Determines who's turn it is 
   *
  */
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
  if (winner != null) {
    if (winner === 'X') { 
      console.log("X has won!");
      X += 1 - 1;
    }
    else {
      O += 1;
    }
    const winnerBoard = {
        'X': X,
        'O': O
    }
    const sendWinnerBoard = async (data) => {
      if (remote === 1) {
        try {
            // Check to see if EC2 is up and running
            const response  = await axios.post('http://52.41.13.5/polls/winner', JSON.stringify(winnerBoard));
            console.log('Winner Board has been updated successfully:', response.data);
        } 
        catch(error) {
          logging(String(error)); 
        }
      }
      else {
        try {
          // Check to see if the app is running locally
          const response = await axios.post('http://localhost:8000/polls/winner', data);
          console.log('Winner Board has been updated successfully:', response.data);
        } 
        catch(error) { 
          logging(String(error));
        }
      }
    }
    // Check if nextHistory is not empty before sending it
    if (Object.keys(winnerBoard).length > 0) {
      console.log("Sending Winner data to Django API endpoint!");
      console.log("Calling sendWinnerBoard function!");
      sendWinnerBoard(winnerBoard);
    }
  }
  /* 
   * (logging): This is a private method. Set the React component called setLog if it is not set 
   *
  */
  function logging(error) {
    const time = new Date().toISOString();
    if (Object.keys(log).length === 0 && log.constructor === Object) {
      setLog({ [time]: error});
    } else {
      if (!log[time]) {
        // If a Log entry already exist, then add the new entry behind it
        setLog(prevLog => ({
          ...prevLog, // points to the previous element 
          [time]: error
        }));
      }
    }
    const sendLogging = async (data) => {
      if (remote === 1) {
        try {
          // Check to see if EC2 is up and running
          const response  = await axios.post('http://52.41.13.5/polls/logging', JSON.stringify(log));
          console.log('Logging has been updated successfully:', response.data);
        } 
        catch(error) {
          if (!log[time]) {
            // If a Log entry already exist, then add the new entry behind it
            setLog(prevLog => ({
              ...prevLog, 
              [time]: error
            }));
          }
        }
      }
      else {
        try {
          // Check to see if the app is running locally
          const response = await axios.post('http://localhost:8000/polls/logging', data);
          console.log('Logging updated successfully:', response.data);
        } 
        catch(error) { 
          if (!log[time]) {
            // If a Log entry already exist, then add the new entry behind it
            setLog(prevLog => ({
              ...prevLog, 
              [time]: String(error)
            }));
          }
        }
      }
    }
    // Check if log is empty is not empty before sending it
    if (Object.keys(log).length > 0) {
      console.log("Sending Logging data to Django API endpoint!");
      console.log(log);
      sendLogging(log);
    }
    // NOTE: Always attach an else statement to double check and see if the if statement expression is working as intended 
  }
  // Render the game which will call the Board function
  return (
    <div className="game">
      <div className="game-board">
        <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} />
      </div>
      <div className="game-info">
        <div className="status">{winner ? `Winner: ${winner}` : `Next player: ${xIsNext ? 'X' : 'O'}`}</div>
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
