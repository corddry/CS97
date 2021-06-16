import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

function Square(props) {
    return(
        <button className="square" onClick={props.onClick}>
            {props.value}
        </button>
    );
}
  class Board extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            squares: Array(9).fill(null),
            xIsNext: true,
            numP: 0,
            heldPiece: -1,
        }
    }

    tryMove(i, squares) {   //Controlls movement when trying to move a piece
      let c = this.state.heldPiece;

      //true if the current player occupies the middle square
      let hasMiddle = (c !== 4 && (squares[4] == 'X' && this.state.xIsNext)
                       || (squares[4] == 'O' && !this.state.xIsNext));
      
      squares[i] = this.state.xIsNext ? 'X' : 'O';

      //Always allow replacement & dont switch turns if so
      if (i === c) {
        this.setState({
          squares: squares,
          heldPiece: -1,
        });
        return;
      }

    //Check that you're trying to move adjacent or replace
      let left = (c - 1);
      let right = (c + 1);
      let up = (c - 3);
      let down = (c + 3);
      let ul = (c - 3 - 1);
      let ur = (c - 3 + 1);
      let dl = (c + 3 - 1);
      let dr = (c + 3 + 1);
      if( !(i === up || i === down   //returns true if not adjacent
         || ((i%3) !== 2 && (i === left || i === ul || i === dl)) //only for non left siders
         || ((i%3) !== 0 && (i === right || i === ur || i === dr)) )) { //only for non right siders
        return;
      }

      //Check that if not moving out from middle, you have a gamewinning move
      if (hasMiddle) {
        if (calculateWinner(squares) === null) {
          return;
        }
      }

      //If successful move, update state
      this.setState({
        squares: squares,
        heldPiece: -1,
        xIsNext: !this.state.xIsNext
      });
    }

    handleClick(i) {
        const squares = this.state.squares.slice();

        if (calculateWinner(squares)) { //Do nothing if game over
          return;
        }

        if (this.state.numP < 6) {  //Adding new pieces
          if(squares[i]) {
            return;
          }
          squares[i] = this.state.xIsNext ? 'X' : 'O';
          this.setState({
            squares: squares,
            numP: this.state.numP + 1,
            xIsNext: !this.state.xIsNext
          });
        } else if(this.state.heldPiece !== -1) {
          this.tryMove(i, squares);
        } else {                      //Pick up a new piece
          if((squares[i] == 'X' && this.state.xIsNext) 
              || (squares[i] == 'O' && !this.state.xIsNext)) {
            squares[i] = null;
            this.setState({
              squares: squares, 
              heldPiece: i,
              });
          }
        }
    }

    renderSquare(i) {
      return (
        <Square 
            value={this.state.squares[i]}
            onClick={() => this.handleClick(i)}
            />
      );
    }
    
  
    render() {
        const winner = calculateWinner(this.state.squares);
        let status;
        if (winner) {
          status = 'Winner: ' + winner;
        } else {
          status = 'Next player: ' + (this.state.xIsNext ? 'X' : 'O');
        }

      return (
        <div>
          <div className="status">{status}</div>
          <div className="board-row">
            {this.renderSquare(0)}
            {this.renderSquare(1)}
            {this.renderSquare(2)}
          </div>
          <div className="board-row">
            {this.renderSquare(3)}
            {this.renderSquare(4)}
            {this.renderSquare(5)}
          </div>
          <div className="board-row">
            {this.renderSquare(6)}
            {this.renderSquare(7)}
            {this.renderSquare(8)}
          </div>
        </div>
      );
    }
  }
  
  class Game extends React.Component {
    render() {
      return (
        <div className="game">
          <div className="game-board">
            <Board />
          </div>
          <div className="game-info">
            <div>{/* status */}</div>
            <ol>{/* TODOn't */}</ol>
          </div>
        </div>
      );
    }
  }
  
  // ========================================
  
  ReactDOM.render(
    <Game />,
    document.getElementById('root')
  );
  
  function calculateWinner(squares) {
    const lines = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8],
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8],
      [0, 4, 8],
      [2, 4, 6],
    ];
    for (let i = 0; i < lines.length; i++) {
      const [a, b, c] = lines[i];
      if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
        return squares[a];
      }
    }
    return null;
  }