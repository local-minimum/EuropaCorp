import React from 'react';
import ReactDOM from 'react-dom';
import ViewMain from './js/components/ViewMain';

const wrapper = document.getElementById('app');
wrapper ? ReactDOM.render(<ViewMain />, wrapper) : alert('Error on Page!');
