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

const Contact = () =>
  <div>
    <h1>Contact:</h1>
    <h4>&nbsp;&nbsp;ajitsen [at] tokostudios [dot] com</h4>
    <a href="https://github.com/ajitsen/keralarescue-search/tree/master/krescue1">&nbsp;&nbsp;Github</a>
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
