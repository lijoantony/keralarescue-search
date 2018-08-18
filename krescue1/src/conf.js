export default {
    solrSearchUrl: "http://localhost:8983/solr/recipe_v2/select",
    pageSize: 10,
    facet: {
        ingredients: {
            type: "field",
            field: "main_ingred",
        },
        dish_type: {
            type: "field",
            field: "dish_type_s",
        },
        prep_time_10: {
            type: "query",
            q: "prep_time_i:[0 TO 10]",
        },
        prep_time_10_20: {
            type: "query",
            q: "prep_time_i:[10 TO 20]",
        },
        prep_time_20_: {
            type: "query",
            q: "prep_time_i:[20 TO *]",
        },
        cuisine: {
            type: "field",
            field: "cuisine_s"
        },
        avoid_non_veg: {
            type: "query",
            q: "veg_b:true",
        },
        avoid_egg: {
            type: "query",
            q: "egg_b:false",
        },
        avoid_cruciferous: {
            type: "query",
            q: "cruciferous_b:false",
        },
        avoid_oven: {
            type: "query",
            q: "oven_b:false",
        },
        avoid_blender: {
            type: "query",
            q: "blender_b:false",
        },
        avoid_microwave: {
            type: "query",
            q: "microwave_b:false",
        }
    },
    highlightParams: {
        "hl": "on",
        "hl.fl": "name main_ingred",
        "hl.snippets": 1,
        "hl:fragsize": 1000,
        "hl.preserveMulti": true
    },
};