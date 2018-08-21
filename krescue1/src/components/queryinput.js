import React, { Component, PropTypes }  from 'react';
import { makeSetQueryAction } from "../actions";

/*
 * A component implementing a simple query input
 *
 * props are:
 *  initialQuery: the initial query, which may be edited by the user
 *  handleActions: handle one or more actions
 */

class QueryInput extends Component {
  /*
   * Set the initial query
   */
  constructor(props) {
    super(props);
    this.state = { query: props.initialQuery || "" };
    this.onSubmit = this.onSubmit.bind(this);
    this.onChange = this.onChange.bind(this);
    this.iconClicked = this.iconClicked.bind(this);
  }

  /*
   * User has clicked the search button or hit Return. Pass the current query up
   */
  onSubmit(event) {
    event.preventDefault();
    this.props.handleActions([makeSetQueryAction(this.state.query)]);
  }

  onChange(event) {
    this.setState({ query: event.target.value });
  }

  iconClicked(text) {
    this.setState({query: text});
    this.props.handleActions([makeSetQueryAction(text)]);
  }

  render() {
    return <form className="navbar-form"
            role="search" onSubmit={this.onSubmit}>
      <div className="input-group col-sm-8">
        <input type="text" className="form-control" placeholder="Search"
          value={this.state.query} onChange={this.onChange} />
        <div className="input-group-btn">
          <button className="btn btn-primary" type="submit"><i className="glyphicon glyphicon-search"/></button>
        </div>
      </div>
      <div className="row app_icon_row col-sm-8">
        <button className="iconsbaby70px" onClick={() => this.iconClicked("\"small kid\" baby കുഞ്ഞ് " + "കുട്ടികളു" + " കുട്ടി കുഞ്ഞിന്" + "\"മാസം പ്രായമായ\"")}/>
        <button className="iconspregnant70px" onClick={() => this.iconClicked("pregnant ഗർഭിണി ഗർഭിണിയായ")}/>
        <button className="iconselder70px" onClick={() => this.iconClicked("grandmother grandfather parents old elder aged പ്രായം")}/>
        <button className="iconshungry70px" onClick={() => this.iconClicked("food hunger പട്ടിണി" + " ഭക്ഷണം" + " ആഹാരം " + " ഫുഡ്‌  ")}/>
        <button className="iconsmedicine70px" onClick={() => this.iconClicked("asthmatic diabetic medicine Doxycycline mg insuline tablets" + " മരുന്ന്" +"  രോഗി   " + " മരുന്നെ")}/>
        <button className="iconslate70px" onClick={() => this.iconClicked("trapped \"2 days\" \"3 days\" \"4 days\" \"5 days\"")}/>
        <button className="iconspeople70px" onClick={() => this.iconClicked("ആളുകൾ " + " പേരോളം  " + " പേർക്കുള്ള " + "\"50 people\" \"100 people\" \"200 people\" \"300 people\" \"400 people\" \"500 people\" \"600 people\" \"700 people\" \"800 people\" \"900 people\" \"1000 people\" \"1100 people\" \"1200 people\" \"1300 people\" \"1400 people\" \"1500 people\"")}/>
        <button className="iconswater70px" onClick={() => this.iconClicked("water " + " വെള്ളം  ")}/>
        <button className="iconscloth70px" onClick={() => this.iconClicked("cloth undergarments Paavada nighty " + "വസ്ത്രങ്ങള്‍ " + " വസ്ത്രം")}/>
        <button className="iconssanitary70px" onClick={() => this.iconClicked("toilet " + " ടോയ്ലറ്റ്   " + "\"chlorine powder\"")}/>
        <button className="iconsmissing70px" onClick={() => this.iconClicked("missing contact find " + " കാണുന്നില്ല ")}/>
        <button className="iconsdisease70px" onClick={() => this.iconClicked("\"loose motion\" vomiting patients mentally \"Urgent Medicine\" " + " പനി " + " fever cold ")}/>
      </div>
    </form>;
  }
}

QueryInput.propTypes = {
  initialQuery: PropTypes.string,
  handleActions: PropTypes.func
};

export default QueryInput;
