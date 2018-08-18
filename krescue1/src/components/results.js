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
            contact = '<em>'+getData(hit, 'requestee_t')+'</em>';
        }

        const phoneNo = getData(hit, 'requestee_phone_t');
        let phone = '';
        if (phoneNo) {
            phone = "<span>☎<a href='tel:"+ phoneNo +"'>" + phoneNo + "</a></span>";
        }

        const locStr = getData(hit, 'location_str');
        let mapLocation = '';
        if (locStr) {
            const mapUrl = "http://maps.google.com/maps?q=" + encodeURI(locStr);
            mapLocation =  "<span><a target='_blank' href='"+mapUrl+"'>Map</a></span>";
        }
        return contact +'&nbsp;&nbsp;'+ phone +'&nbsp;&nbsp;'+ mapLocation;
    }

    function get_details(hit) {
        let detail = '';
        const no = getData(hit, "needothers_t");
        if (no) {
            detail = no;
        }
        const c = getData(hit, 'detailcloth_t');
        if (c) {
            detail += " " + c;
        }
        const f = getData(hit, 'detailfood_t');
        if (f) {
            detail += " " + f;
        }
        const k = getData(hit, 'detailkit_util_t');
        if (k) {
            detail += " " + k;
        }
        const med = getData(hit, 'detailmed_t');
        if (med) {
            detail += " " + med;
        }
        const res = getData(hit, 'detailrescue_t');
        if (res) {
            detail += " " + res;
        }
        const t = getData(hit, 'detailtoilet_t');
        if (t) {
            detail += " " + t;
        }
        const w = getData(hit, 'detailwater_t');
        if (w) {
            detail += " " + w;
        }
        if (detail) {
            return <div className="app_normal"><em>🗒 </em>{detail}</div>
        }
        return '';
    }

    function get_needs(hit) {
        let fields = {"needcloth_b":"Cloth", "needfood_b": "Food", "needkit_util_b":"Kit", "needmed_b":"Medicine",
            "needrescue_b":"Rescue", "needtoilet_b":"Toilet", "needwater_b":"Water"};
        let needStr = "";
        for (let field in fields){
            let data = getData(hit, field, false);
            if (data) {
                if (needStr) {
                    needStr += ", " + fields[field];
                } else {
                    needStr = fields[field];
                }
            }
        }
        if (needStr) {
            return <div>{"Needs: " + needStr}</div>;
        }
        return '';
    }

    function get_time(hit) {
        const lastMod = getData(hit, 'last_modified');
        const monthNames = [
            "January", "February", "March",
            "April", "May", "June", "July",
            "August", "September", "October",
            "November", "December"
        ];
        let time = '';
        if (lastMod && lastMod instanceof Array) {
            const date = new Date(lastMod[0]);
            let day = date.getDate();
            let monthIndex = date.getMonth();
            let hours = date.getHours();
            let time = '';
            if (hours > 12) {
                time = hours - 12 +' PM';
            } else {
                time = hours + ' AM';
            }
            return <em>{"⏱ "+monthNames[monthIndex]+" "+ day + ", " +time}</em>;
        }
    }

    const results = searchResults.map((hit) => {
      const titleHtml = { __html: get_title(hit) };
      const ingredientsHtml =  { __html: '<span>Name: </span>' + get_contact_map(hit) };

      const ingClassNames = classNames({"app_vsp03":true, "app_capitalize":true, "app_content": true});
        const notes = get_details(hit);
        const time = get_time(hit);
        const needs = get_needs(hit);

      return <div key={hit.id} className="app_hit">
        <h4 className={"app_title"} dangerouslySetInnerHTML={titleHtml} />
        <div className={ingClassNames} dangerouslySetInnerHTML={ingredientsHtml} />
        {notes}
        <div className="text-muted app_vsp03">
            {time}
            {needs}
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
