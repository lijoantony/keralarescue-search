import React, { PropTypes } from 'react';
import QueryInput from './queryinput';
import Stats from './stats';
import Results from './results';
import Pager from './pager';
import TermFacetList from './termfacetlist';
import QueryFacetList from './queryfacetlist';
import conf from '../conf';


const SearchAppRenderer = props => {
  const response = props.solrConnector.response ?
    props.solrConnector.response.response : null;

  const hl = props.solrConnector.response ?
    props.solrConnector.response.highlighting : null;

  const header = props.solrConnector.response ?
    props.solrConnector.response.responseHeader : null;
  const haveResults = response && response.numFound > 0;

  let row2 = null;
  let row3 = null;
  let row4 = null;


   if (response) {

      row2 = <div className="row app_vsp05">
      <Stats qtime={header.QTime}
        numFound={response.numFound}
        start={response.start}
        len={response.docs.length} />
      <div className="col-sm-4">
          <strong>Refine search</strong>
      </div>
   </div>;


    if (haveResults) {
      const facets = props.solrConnector.response.facets;

      row3 = <div className="row">
        <Results searchResults={response.docs} highlighting={hl}/>
        {/*Right Rail*/}
        <div className="col-sm-4">
          <h5 className="app_vsp25">Cuisine:</h5>
          <TermFacetList multiselect={false}
             facet={"cuisine"}
             buckets={facets.cuisine.buckets}
             filters={props.searchParams.filter_cuisine}
             handleActions={props.handleActions} />
          <h5>Main Ingredients:</h5>
          <TermFacetList multiselect={true}
            facet={"ingredients"}
            buckets={facets.ingredients.buckets}
            filters={props.searchParams.filter_ingredients}
            handleActions={props.handleActions} />
          <h5 className="app_vsp25">Dish Type: <em>🍽</em></h5>
          <TermFacetList multiselect={false}
            facet={"dish_type"}
            buckets={facets.dish_type.buckets}
            filters={props.searchParams.filter_dish_type}
            handleActions={props.handleActions} />
          <h5 className="app_vsp25">Time to Cook: <em>⏱</em></h5>
          <QueryFacetList facets={[
              { facet: "prep_time_10", label: "Up to 10min"},
              { facet: "prep_time_10_20", label: "10 to 20min" },
              { facet: "prep_time_20_", label: "20min and more" }
            ]}
            facetData={facets}
            searchParams={props.searchParams}
            handleActions={props.handleActions} />
          <h5 className="app_vsp25">Food Type:</h5>
          <QueryFacetList facets={[
                { facet: "avoid_non_veg", label: "Only Veg"},
                { facet: "avoid_egg", label: "Avoid Egg" },
                { facet: "avoid_cruciferous", label: "No Cruciferous" }
            ]}
            facetData={facets}
            searchParams={props.searchParams}
            handleActions={props.handleActions} />
          <h5 className="app_vsp25">Avoid Utensils:</h5>
          <QueryFacetList facets={[
                { facet: "avoid_oven", label: "No Oven"},
                { facet: "avoid_blender", label: "No Blender" },
                { facet: "avoid_microwave", label: "No Microwave" }
            ]}
            facetData={facets}
            searchParams={props.searchParams}
            handleActions={props.handleActions} />
        </div>
      </div>;

      // only show pager if required
      if (response.start > 0 || response.numFound > response.docs.length) {
        row4 = <div className="row app_vsp05">
          <div className="col-sm-8">
            <Pager numFound={response.numFound}
              start={response.start}
              len={response.docs.length}
              handleActions={props.handleActions}
              pageSize={conf.pageSize} />
          </div>
        </div>;
      }
    }
  }

  const busy = props.solrConnector.busy ? <h4>searching...</h4> : null;

  return <div className="container">
    <div className="row">
      <QueryInput initialQuery={props.searchParams.query}
                  handleActions={props.handleActions} />
    </div>
    {row2} {row3} {row4}
    {busy}
  </div>;
};



SearchAppRenderer.propTypes = {
  searchParams: PropTypes.object
};

export default SearchAppRenderer;
