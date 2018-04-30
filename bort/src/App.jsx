import React, { Component } from 'react';
import moment from 'moment';
import Chat from './components/Chat';
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
    const {
      handleCambiarMensaje,
      handleAddMessage,
      state: {
        mensajes,
        mensajeActual,
      } 
    }= this;
    return (
      <Chat
        mensajes={mensajes}
        onEnviar={handleAddMessage}
        onCambiarMsj={handleCambiarMensaje}
        msjActual={mensajeActual}
      />
    );
  }
}

export default App;
