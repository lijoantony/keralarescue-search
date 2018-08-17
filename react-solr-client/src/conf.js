export default {
    solrSearchUrl: "http://localhost:8983/solr/krescue10/select",
    pageSize: 10,

    facet: {
        district: {
            type: "field",
            limit: 20,
            field: "district_full_s"
        },
        place: {
            type: "field",
            limit: 40,
            field: "place_s"
        },
        is_request_for_others: {
            type: "query",
            q: "is_request_for_others_b:true"
        },
        needfood: {
            type: "query",
            q: "needfood_b:true"
        },
        needcloth: {
            type: "query",
            q: "needcloth_b:true"
        },
        needkit_util: {
            type: "query",
            q: "needkit_util_b:true"
        },
        needmed: {
            type: "query",
            q: "needmed_b:true"
        },
        needrescue: {
            type: "query",
            q: "needrescue_b:true"
        },
        needtoilet: {
            type: "query",
            q: "needtoilet_b:true"
        },
        needwater: {
            type: "query",
            q: "needwater_b:true"
        }
    },
    highlightParams: {
        "hl": "on",
        "hl.fl": "place_s district_full_s",
        "hl.snippets": 1,
        "hl:fragsize": 1000,
        "hl.preserveMulti": true
    }
};