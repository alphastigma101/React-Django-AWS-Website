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
  const [winnerHandled, setWinnerHandled] = useState(false);
  const [prevMove, setPrevMove] = useState(0);
  // Create the winner board
  const winnerBoard = {
    'X': X,
    'O': O
  }
  // Mount the react component to record logging for it 
  useEffect(() => {
    if (loggingCreated === false) {
      logging('Creating the logging Data!');
      setLoggingCreated(true); // set loggingCreated to true
    }
  }, [loggingCreated]);
  // Make a post request and send the history data to the Django API End Point
  const sendHistory = async (data) => {
    if (remote === 1) {
      try {
        // Check to see if EC2 is up and running
        const response  = await axios.post('http://52.41.13.5/polls/start_game', data);
      } catch(error) { logging(String(error)); }
    }
    else {
      try {
        // Check to see if the app is running locally
        const response = await axios.post('http://localhost:8000/polls/start_game', data);
      } 
      catch(error) { logging(String(error)); }
    }
  }
  /*
   * (handlePlay): Is a private function of the Game Function
   * Params:
      *  nextSquares: 
  */
  function handlePlay(nextSquares) {
    const nextHistory = [...history.slice(0, currentMove + 1), nextSquares];
    setHistory(nextHistory);
    setCurrentMove(nextHistory.length - 1);
  }
  // Check if currentMove is greater than prevMove
  useEffect(() => {
    if (currentMove > prevMove) {
      sendHistory(history);
      setPrevMove(currentMove);
    }
  }, [currentMove, prevMove]);

  /*
   * (jumpTo): Is a private function of Game Function
   * Params:
      * nextMove: Determines who's turn it is 
   *
  */
  function jumpTo(nextMove) { setCurrentMove(nextMove);} // increment the component value by 1
  const currentSquares = history[currentMove];
  const xIsNext = currentMove % 2 === 0;
  useEffect(() => {
    const winner = calculateWinner(currentSquares);
    if (winner != null && !winnerHandled) {
      handleWinner(winner);
      setWinnerHandled(true);
    }
  }, [currentSquares, winnerHandled]);
  /*
   * (handleWinner): This function will get executed once there is a winner
   * Params:
        *  winner: is a string that can be either X or O
   * Returns:
      * Returns nothing. It populates the winnerBoard
   */
  function handleWinner(winner) {
    if (winner === 'X') {  X += 1; } 
    else { O += 1; }
    setWinnerHandled(false); // set it back to false 
  }
  const moves = history.map((squares, move) => {
    const description = move > 0 ? `Go to move #${move}` : 'Go to game start';
    return (
      <li key={move}>
        <button onClick={() => jumpTo(move)}>{description}</button>
      </li>
    );
  });
  /*
   * (handleClick): Is a private function of Game Function
   * Params:
      * i: Determines who's turn it is 
   *
  */
  function handleClick(i) {
    if (calculateWinner(currentSquares) || currentSquares[i]) {
      return;
    }
    const nextSquares = [...currentSquares];
    nextSquares[i] = xIsNext ? 'X' : 'O';
    handlePlay(nextSquares);
  }

  if (winnerHandled === true) {
    const sendWinnerBoard = async (data) => {
      if (remote === 1) {
        try {
          // Check to see if EC2 is up and running
          const response  = await axios.post('http://52.41.13.5/polls/winner', JSON.stringify(winnerBoard));
        } 
        catch(error) { logging(String(error)); }
      }
      else {
        try {
          // Check to see if the app is running locally
          const response = await axios.post('http://localhost:8000/polls/winner', data);
        } 
        catch(error) { logging(String(error)); }
      }
    }
    // Check if nextHistory is not empty before sending it
    if (Object.keys(winnerBoard).length > 0) {
      sendWinnerBoard(winnerBoard);
    }
  }
  /* 
   * (logging): This is a private method. Set the React component called setLog if it is not set 
   * Params:
      * error: is a string type that represents a string literal of the error that occurred
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
    if (Object.keys(log).length > 0) { sendLogging(log); }
    // NOTE: Always attach an else statement to double check and see if the if statement expression is working as intended 
  }
  // Render the game which will call the Board function
  return (
    <div className="game">
      <div className="game-board">
        <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} />
      </div>
      <div className="game-info">
        <div className="status">{`Next player: ${xIsNext ? 'X' : 'O'}`}</div>
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

