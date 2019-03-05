import React, { Component} from 'react';
import {Router, browserHistory} from 'react-router'
import './App.css'
import routes from './route'
import Navbar from './components/Navbar/Index'
import Footer from './components/Footer/Index'


class App extends Component {

  render() {
    return (
      <div className="App">
        <Navbar />
          <Router history={browserHistory} routes={routes} />
        <Footer />
      </div>
    );
  }
}

export default App;
