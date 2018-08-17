import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, Redirect, Link, hashHistory } from 'react-router';
import NavBar from './components/navbar';
import SearchApp from './components/searchapp';
import Conf from './conf';

const App = (props) =>
  <div>
    <NavBar/>
    {props.children}
  </div>;

const About = () =>
  <h1>About</h1>;

const leftMargin = {
    marginLeft: "20px"
};
const Contact = () =>
    <div style={leftMargin}>
        <h1>Contact:</h1>
        <p>Email ajitsen [at] tokostudios [dot] com; Phone: +91-9880302719</p>
    </div>


const RoutedApp = () =>
  <Router history={hashHistory}>
    <Redirect from="/" to="/search" />
    <Route path="/" component={App}>
      <Route path="search" component={SearchApp}/>
      <Route path="about" component={About} />
      <Route path="contact" component={Contact} />
    </Route>
  </Router>;

ReactDOM.render(<RoutedApp/>, document.getElementById('app'));
