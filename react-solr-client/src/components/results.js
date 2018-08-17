import React, { PropTypes }  from 'react';
import classNames from 'classnames';

/*
 * A component implementing a simple results list.
 *
 * props are:
 *  results: an array of objects holding data for each result
 */

const Results = ({searchResults, highlighting}) => {

    function get_hl_or_normal_title(hit) {
        let place =  hit.place_s;
        if (highlighting && highlighting[hit.id] && highlighting[hit.id].place_s) {
            place = highlighting[hit.id].place_s;
        }

        let dist =  hit.district_full_s;
        if (highlighting && highlighting[hit.id] && highlighting[hit.id].district_full_s) {
            dist = highlighting[hit.id].district_full_s;
        }
        const title =  place + '(' + dist + ')';
        const detailUrl = "https://keralarescue.in/request_details/"+hit.id+"/";
        return title + "&nbsp;&nbsp;<a target='_blank' href=\""+detailUrl+"\">details</a><span>";
            /*+(hit.link_type_s === "video"? "&nbsp; ▶️":"") + "</span>";*/
    }

    function get_hl_or_normal_contact(hit) {
      let contact = hit.requestee_t;
      if (highlighting && highlighting[hit.id] && highlighting[hit.id].requestee_t) {
        contact = highlighting[hit.id].requestee_t;
      }
      const mapLocation =  "http://maps.google.com/maps?q=" + encodeURI(hit.location_str);
      return contact + "&nbsp;&nbsp;<a href='tel:"+ hit.requestee_phone_t +"'>" + hit.requestee_phone_t + "</a>"
            + "&nbsp;&nbsp; <a target='_blank' href='" + mapLocation + "'>Map</a>";
    }

    function get_notes(hit) {
        let detail = '';
        if (hit.needothers_t) {
            detail = hit.needothers_t;
        }
        if (hit.detailcloth_t) {
            detail += " " +hit.detailcloth_t;
        }
        if (hit.detailfood_t) {
            detail += " " +hit.detailfood_t;
        }
        if (hit.detailkit_util_t) {
            detail += " " +hit.detailkit_util_t;
        }
        if (hit.detailmed_t) {
            detail += " " +hit.detailmed_t;
        }
        if (hit.detailrescue_t) {
            detail += " " +detailrescue_t;
        }
        if (hit.detailtoilet_t) {
            detail += " " +detailtoilet_t;
        }
        if (hit.detailwater_t) {
            detail += " " +detailwater_t;
        }
        if (detail) {
            return <div className="app_normal"><em>🗒 </em>{detail}</div>
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
      const titleHtml = { __html: get_hl_or_normal_title(hit) };
      const ingredientsHtml =  { __html: '<span>Contact: </span>' + get_hl_or_normal_contact(hit) };

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
        <hr/>
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
