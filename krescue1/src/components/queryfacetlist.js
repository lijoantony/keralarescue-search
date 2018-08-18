import React, { Component, PropTypes } from 'react';
import { makeSetFilterAction, makeClearFiltersAction } from "../actions";

/*
 * A component implementing a query facet list.
 *
 * props should be like:
 *    facets: the query facet names in an array
 *    facetData: the .facets response from Solr
 *    searchParams: the URL search params
 *    handleActions: handle one or more actions
 */

class QueryFacetList extends Component {
  constructor() {
    super();
    this.unsetAll = this.unsetAll.bind(this);
  }
  render() {
   const searchParamKeys = Object.keys(this.props.searchParams);
   let haveSelectedValue = false;


   let facitems = this.props.facets.map(fac => {
      const selected = searchParamKeys.find(key =>
        key === "filter_" + fac.facet) !== undefined;

      haveSelectedValue = haveSelectedValue || selected;
      const count = this.props.facetData[fac.facet].count;

      if (selected || count === 0) {
        return <li key={"facet_" + fac.facet}>
          <label className={count === 0? "app_gray" : "app_underline"}>
          {fac.label + " (" + count + ")"}</label></li>;
      }  else {
        const handler = (event) => {
          event.preventDefault();
          this.setFilter(fac.facet, true);
        };
        return <li key={"facet_" + fac.facet}>
          <a href="#" onClick={handler}><label className="app_normal">{fac.label}</label></a>
          { " (" + count + ")"}
        </li>;
      }
   });

    /*
     * the "any" link should only be active when a facet is selected
     */
    const any = haveSelectedValue ? <a className="app_any" href="#" onClick={this.unsetAll}>
      <em>❎ clear</em></a> : <em>clear</em>;

    return <ul className="app_ul">
      {facitems}
      <li>{any}</li>
    </ul>;
  }

  // set/unset a single filter
  setFilter(facet, apply) {
    // remove any other facets in this group
    let actions = this.props.facets.reduce((o, fac) => {
      o.push(makeClearFiltersAction(fac.facet));
      return o;
    }, []);
    actions.push(makeSetFilterAction(facet, "true", apply));
    this.props.handleActions(actions);
  }

  // unset all selected filters
  unsetAll(event) {
    event.preventDefault();
    this.props.handleActions(this.props.facets.reduce((o, fac) => {
      o.push(makeClearFiltersAction(fac.facet));
      return o;
    }, []));
  }
}

QueryFacetList.propTypes = {
  multiselect: PropTypes.bool,
  facets: PropTypes.arrayOf(PropTypes.object),
  facetData: PropTypes.object,
  searchParams: PropTypes.object,
  handleActions: PropTypes.func
};

export default QueryFacetList;
