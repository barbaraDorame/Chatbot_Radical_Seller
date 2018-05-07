import React from 'react';
import PropTypes from 'prop-types';
import Mensaje from './Mensaje';

const Chat = ({
  mensajes,
  onEnviar,
  onCambiarMsj,
  msjActual,
}) => (
  <div id="wrapper">
    <div id="menu">
      <p className="welcome">Hola, me llamo Bort</p>
    </div>

    <div id="chatbox">
      { mensajes.map(msg => <Mensaje key={msg.id} {...msg} />) }
    </div>

    <form name="message" onSubmit={onEnviar}>
      <input
        type="text"
        value={msjActual}
        onChange={onCambiarMsj}
        size="63"
      />
      <input name="submitmsg" type="submit" id="submitmsg" value="Send" />
    </form>
  </div>
);

Chat.propTypes = {
  mensajes: PropTypes.array.isRequired,
  onEnviar: PropTypes.func.isRequired,
  onCambiarMsj: PropTypes.func.isRequired,
  msjActual: PropTypes.string.isRequired,
};

export default Chat;

