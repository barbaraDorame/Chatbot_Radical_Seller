import React, { Component } from 'react';
import moment from 'moment';
import Mensaje from './components/Message';
import './App.css';

let counter = 0;

moment.locale('es');

const crearMensaje = (texto, hora, humano = true) => ({
  texto, hora, humano, id: (counter += 1),
});

class App extends Component {
  constructor(props) {
    super(props);
    this.handleAddMessage = this.handleAddMessage.bind(this);
    this.handleCambiarMensaje = this.handleCambiarMensaje.bind(this);
    this.state = {
      mensajes: [
        crearMensaje('Hola', moment(), false),
        crearMensaje('Hola', moment(), true),
        crearMensaje('¿Como estas?', moment(), false),
        crearMensaje('Bien, ¿y tú?', moment(), true),
      ],
      mensajeActual: '',
    };
  }

  handleAddMessage(event) {
    event.preventDefault();
    this.setState(prevState => ({
      ...prevState,
      mensajes: [
        ...prevState.mensajes,
        crearMensaje(prevState.mensajeActual, moment()),
      ],
      mensajeActual: '',
    }));
  }

  handleCambiarMensaje(event) {
    const text = event.target.value;
    this.setState(prevState => ({
      ...prevState,
      mensajeActual: text,
    }));
  }

  render() {
    return (
      <div id="wrapper">
        <div id="menu">
          <p className="welcome">Hola, me llamo Bort</p>
          <p className="logout"><a id="exit" href="https://google.com">Salir del chat</a></p>
        </div>

        <div id="chatbox">
          { this.state.mensajes.map((msg, i) => <Mensaje key={i} {...msg} />) }
        </div>

        <form name="message" onSubmit={this.handleAddMessage}>
          <input
            type="text"
            value={this.state.mensajeActual}
            onChange={this.handleCambiarMensaje}
            size="63"
          />
          <input name="submitmsg" type="submit" id="submitmsg" value="Send" />
        </form>
      </div>
    );
  }
}

export default App;
