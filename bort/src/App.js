import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
        <div id="wrapper">
          <div id="menu">
              <p class="welcome">Hola, me llamo Bort</p>
              <p class="logout"><a id="exit" href="#">Salir del chat</a></p>
              <div></div>
          </div>

          <div id="chatbox"></div>

          <form name="message" action="">
              <input name="usermsg" type="text" id="usermsg" size="63" />
              <input name="submitmsg" type="submit"  id="submitmsg" value="Send" />
          </form>
        </div>
    );
  }
}

export default App;
