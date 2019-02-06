import React, { Component } from 'react';
import Main from './components/Main';
import Aside from './components/Aside';
import Footer from './components/Footer';
import Header from './components/Header';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Header />      
        <Main />
        <Aside />
        <Footer />
      </div>
    );
  }
}

export default App;
