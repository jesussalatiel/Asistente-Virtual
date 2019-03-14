import React, { Component } from 'react';
import './App.css';
import BaseRouter from './routers';
import { BrowserRouter } from 'react-router-dom'; 

class App extends Component {
  render() {
    return (
      <div className="App">
      <BrowserRouter>
        
        <BaseRouter />
        
      </BrowserRouter>
      </div>
    );
  }
}

export default App;
