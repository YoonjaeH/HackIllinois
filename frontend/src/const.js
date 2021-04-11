// State -> [latitude, longitude]

const GEO_CENTER = {
    "Alabama" :             [32.78, 86.83],
    "Alaska" :              [64.07, 152.28],
    "Arizona" :             [34.27, 111.66],
    "Arkansas" :            [34.89, 92.44],
    "California" :          [37.18, 119.47],
    "Colorado" :            [39.00, 105.55],
    "Connecticut" :         [41.62, 72.73],
    "Delaware" :            [38.99, 75.51],
    "Distric of Columbia" : [38.91, 77.01],
    "Florida" :             [28.63, 82.45],
    "Georgia" :             [32.64, 83.44],
    "Hawaii" :              [20.29, 156.37],
    "Idaho" :               [44.35, 114.61],
    "Illinois" :            [40.04, 89.20],
    "Indiana":              [39.89, 86.28],
    "Iowa" :                [42.08, 93.50],
    "Kansas" :              [38.49, 98.38],
    "Kentucky" :            [37.53, 85.30],
    "Louisiana" :           [31.07, 92.00],
    "Maine" :               [45.37, 69.24],
    "Maryland" :            [39.06, 76.79],
    "Massachusetts" :       [42.26, 71.80],
    "Michigan" :            [44.35, 85.41],
    "Minnesota" :           [46.28, 94.31],
    "Mississippi" :         [32.74, 89.67],
    "Missouri" :            [38.36, 92.46],
    "Montana" :             [47.05, 109.63],
    "Nebraska" :            [41.54, 99.80],
    "Nevada" :              [39.33, 116.63],
    "New Hampshire" :       [43.68, 71.58],
    "New Jersey" :          [40.19, 74.67],
    "New Mexico" :          [34.41, 103.11],
    "New York" :            [42.95, 75.53],
    "North Carolina" :      [35.56, 79.39],
    "North Dakota" :        [47.45, 100.47],
    "Ohio" :                [40.29, 82.79],
    "Oklahoma" :            [35.59, 97.49],
    "Oregon" :              [43.93, 120.56],
    "Pennsylvania" :        [40.88, 77.80],
    "Rhode Island" :        [41.68, 71.56],
    "South Carolina" :      [33.92, 80.90],
    "South Dakota" :        [44.44, 110.27],
    "Tennessee" :           [35.86, 86.35],
    "Texas" :               [31.48, 99.33],
    "Utah" :                [39.31, 111.67],
    "Vermont" :             [44.07, 72.67],
    "Virginia" :            [37.52, 78.85],
    "Washington" :          [47.38, 120.45],
    "West Virginia" :       [38.64, 80.62],
    "Wisconsin" :           [44.62, 89.99],
    "Wyoming" :             [43.00, 107.55]
};

/**
 * Returns the radious and the hue of based on 
 * the prediction percentage of the state.
 * @param {Float} p the prediction percentage value between 0 and 1
 * @returns {Array} the radious and hue of the circle
 */
function pred_rad_and_hue(p) {
    r = (2 * p + 1) * 10000;

    r_comp = Math.floor(255 * (1 - p)).toString(16);
    g_comp = Math.floor(255 * p).toString(16);
    b_comp = "00";
    h = r_comp + g_comp + b_comp;

    return { "rad" : r, "hue" : h}
}
