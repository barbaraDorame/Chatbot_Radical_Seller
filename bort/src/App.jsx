import React, { Component } from 'react';
import moment from 'moment';
import Chat from './components/Chat';
import './App.css';

moment.locale('es');

const crearMensaje = (id, texto, hora, humano = true) => ({
  texto, hora, humano, id,
});

const convertirMensaje = ({
  id, texto, hora_creacion, humano,
}) => ({
  id, texto, hora: moment(hora_creacion), humano,
});

class App extends Component {
  constructor(props) {
    super(props);
    this.handleAddMessage = this.handleAddMessage.bind(this);
    this.handleCambiarMensaje = this.handleCambiarMensaje.bind(this);
    this.state = {
      loaded: true,
      conversationId: null,
      mensajes: [],
      mensajeActual: '',
    };
  }

  componentDidMount() {
    fetch('/api/conversacion', { method: 'post' })
      .then(res => res.json())
      .then((conversation) => {
        this.setState(prevState => ({
          ...prevState,
          loaded: true,
          conversationId: conversation.id,
          mensajes: conversation.mensajes.map(convertirMensaje),
        }));
      });
  }

  handleAddMessage(event) {
    event.preventDefault();
    const texto = this.state.mensajeActual;
    fetch(`/api/conversacion/${this.state.conversationId}/mensajes`, {
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      method: 'post',
      body: JSON.stringify({ texto }),
    }).then(res => res.json())
      .then((msg) => {
        this.setState(prevState => ({
          ...prevState,
          mensajes: [
            ...prevState.mensajes,
            convertirMensaje(msg),
          ],
        }));
      });
  }

  handleCambiarMensaje(event) {
    const texto = event.target.value;

    this.setState(prevState => ({
      ...prevState,
      mensajeActual: texto,
    }));
  }

  render() {
    const {
      handleCambiarMensaje,
      handleAddMessage,
      state: {
        mensajes,
        mensajeActual,
        loaded,
      },
    } = this;

    if (!loaded) {
      return <div>Cargando...</div>;
    }

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
