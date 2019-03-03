import React, { Component } from 'react';
import Navbar from './components/Navbar/Index'
import Footer from './components/Footer/Index'


class App extends Component {
  render() {
    return (
      <div className="App">
        <Navbar/>
        <Footer/>
      </div>
    );
  }
}

export default App;
