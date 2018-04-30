import React from 'react';
import PropTypes from 'prop-types';

const obtenerUsuario = humano => (humano
  ? <span style={{ color: 'blue' }}>Tu</span>
  : <span style={{ color: 'red' }}>Bort</span>
);

const Mensaje = ({ humano, hora, texto }) => (
  <div>[{hora.format('LTS')}] {obtenerUsuario(humano)}: {texto}</div>
);

Mensaje.propTypes = {
  humano: PropTypes.bool.isRequired,
  texto: PropTypes.string.isRequired,
  hora: PropTypes.any.isRequired,
};

export default Mensaje;
