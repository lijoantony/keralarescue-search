import React, { PropTypes }  from 'react';
import classNames from 'classnames';

/*
 * A component implementing a simple results list.
 *
 * props are:
 *  results: an array of objects holding data for each result
 */

const Results = ({searchResults, highlighting}) => {

    function getData(object, field, defaultVal="") {
        if (object && object.hasOwnProperty(field) && object[field]) {
            return object[field];
        }
        return defaultVal;
    }

    function getHighlighted(highlighting, id, field) {
        if (highlighting && highlighting[id] && highlighting[id][field]) {
            return highlighting[id][field].join("");
        }
        return '';
    }

    function get_title(hit) {
        let title = getHighlighted(highlighting, hit.id, 'dist_place_t');
        if (!title) {
            title = getData(hit, 'dist_place_t') || " id" + hit.id;
        }
        const detailUrl = "https://keralarescue.in/request_details/"+hit.id+"/";
        return "<a target='_blank' href=\""+detailUrl+"\">"+title+"</a>";
    }

    function get_contact_map(hit) {
        let contact = getHighlighted(highlighting, hit.id, 'requestee_t')
        if (!contact) {
            contact = getData(hit, 'requestee_t');
        }

        const phoneNo = getData(hit, 'requestee_phone_t');
        let phone = '';
        if (phoneNo) {
            phone = "<span><a href='tel:"+ phoneNo +"'>" + phoneNo + "</a></span>";
        }

        const locStr = getData(hit, 'location_str');
        let mapLocation = '';
        if (locStr) {
            const mapUrl = "http://maps.google.com/maps?q=" + encodeURI(locStr);
            mapLocation =  "<span><a target='_blank' href='"+mapUrl+"'>Map</a></span>";
        }
        return contact +'&nbsp;&nbsp;'+ phone +'&nbsp;&nbsp;'+ mapLocation;
    }

    function get_notes(hit) {
        if (hit.notes_t && /\S/.test(hit.notes_t)) {
            return <div className="app_normal"><em>🗒 </em>{hit.notes_t}</div>
        }
        return '';
    }

    function get_dish_type(hit) {
        if (hit.dish_type_s && /\S/.test(hit.dish_type_s)) {
            return <span className="app_capitalize"><em>🍽</em>{hit.dish_type_s}&nbsp;&nbsp;</span>
        }
        return '';
    }

    function get_utensils(hit) {
        let utensils = hit.microwave_b ? ' Microwave' : '';
        if (hit.blender_b) {
            if (utensils !== '') {
                utensils += ' |';
            }
            utensils += ' Blender';
        }
        if (hit.oven_b) {
            if (utensils !== '') {
                utensils += ' |';
            }
            utensils += ' Oven';
        }
        if (utensils !== '') {
            utensils = <span>Utensil: {utensils}&nbsp;&nbsp;</span>
        }
        return utensils;
    }

    const results = searchResults.map((hit) => {
      const titleHtml = { __html: get_title(hit) };
      const ingredientsHtml =  { __html: '<span>Contact: </span>' + get_contact_map(hit) };

      const ingClassNames = classNames({"app_vsp03":true, "app_capitalize":true, "app_content": true});
      const prepTime = hit.prep_time_i ?  <em>⏱ {hit.prep_time_i} m&nbsp;&nbsp;</em>:"";
      const utensils = get_utensils(hit);
      const dishType = get_dish_type(hit);
      const notes = get_notes(hit);

      return <div key={hit.id} className="app_hit">
        <h4 className={"app_title"} dangerouslySetInnerHTML={titleHtml} />
        <div className={ingClassNames} dangerouslySetInnerHTML={ingredientsHtml} />
        {notes}
        <div className="text-muted app_vsp03">
          {prepTime}
          {utensils}
          {dishType}
        </div>
      </div>;
    });

  return <div className="col-sm-8">
    {results}
  </div>;
};

Results.propTypes = {
  searchResults: PropTypes.arrayOf(PropTypes.object).isRequired,
  highlighting: PropTypes.object
};

export default Results;
