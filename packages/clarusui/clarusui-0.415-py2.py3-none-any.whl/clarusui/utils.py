"""Some useful utility methods/constants."""

import os
import webbrowser

COLOURS = {
        'Default' :['#636efa', '#EF553B', '#00cc96', '#ab63fa', '#19d3f3', '#e763fa'],
        'Reds' :['#F44336', '#FFCDD2', '#EF9A9A', '#E57373', '#EF5350', '#E53935',
                 '#D32F2F', '#C62828', '#B71C1C', '#FF8A80', '#FF5252', '#FF1744',
                 '#D50000'],
        'LightBlues' :['#03A9F4', '#B3E5FC', '#81D4FA', '#4FC3F7', '#29B6F6',
                       '#039BE5', '#0288D1', '#0277BD', '#01579B', '#80D8FF',
                       '#40C4FF', '#00B0FF', '#0091EA'],
        'Pinks':['#E91E63', '#F8BBD0', '#F48FB1', '#F06292', '#EC407A', '#D81B60',
                 '#C2185B', '#AD1457', '#880E4F', '#FF80AB', '#FF4081', '#F50057',
                 '#C51162'],
        'Purples' :['#9C27B0', '#E1BEE7', '#CE93D8', '#BA68C8', '#AB47BC', '#8E24AA',
                    '#7B1FA2', '#6A1B9A', '#4A148C', '#EA80FC', '#E040FB', '#D500F9',
                    '#AA00FF'],
        'Blues':['#2196F3', '#BBDEFB', '#90CAF9', '#64B5F6', '#42A5F5', '#1E88E5',
                 '#1976D2', '#1565C0', '#0D47A1', '#82B1FF', '#448AFF', '#2979FF',
                 '#2962FF'],
        'Greens':['#4CAF50', '#C8E6C9', '#A5D6A7', '#81C784', '#66BB6A', '#43A047',
                  '#388E3C', '#2E7D32', '#1B5E20', '#B9F6CA', '#69F0AE', '#00E676',
                  '#00C853']
        }

HEAT_SCALES = {'Blues' : ['#E3F2FD', '#BBDEFB', '#90CAF9', '#64B5F6', '#42A5F5',
                          '#2196F3', '#1E88E5', '#1976D2', '#1565C0', '#0D47A1'],
               'Reds' :['#FFEBEE', '#FFCDD2', '#EF9A9A', '#E57373', '#EF5350',
                        '#F44336', '#E53935', '#D32F2F', '#C62828', '#B71C1C'],
               'Greens' : ['#E8F5E9', '#C8E6C9', '#A5D6A7', '#81C784', '#66BB6A',
                           '#4CAF50', '#43A047', '#388E3C', '#2E7D32', '#1B5E20']}

COUNTRY_CODES = {"Aruba":"AW",
                 "Afghanistan":"AF",
                 "Angola":"AO",
                 "Anguilla":"AI",
                 "Albania":"AL",
                 "Andorra":"AD",
                 "United Arab Emirates":"AE",
                 "Argentina":"AR",
                 "Armenia":"AM",
                 "American Samoa":"AS",
                 "Antarctica":"AQ",
                 "French Southern Territories":"TF",
                 "Antigua and Barbuda":"AG",
                 "Australia":"AU",
                 "Austria":"AT",
                 "Azerbaijan":"AZ",
                 "Burundi":"BI",
                 "Belgium":"BE",
                 "Benin":"BJ",
                 "Bonaire, Sint Eustatius and Saba":"BQ",
                 "Burkina Faso":"BF",
                 "Bangladesh":"BD",
                 "Bulgaria":"BG",
                 "Bahrain":"BH",
                 "Bahamas":"BS",
                 "Bosnia and Herzegovina":"BA",
                 "Belarus":"BY",
                 "Belize":"BZ",
                 "Bermuda":"BM",
                 "Bolivia, Plurinational State of":"BO",
                 "Brazil":"BR",
                 "Barbados":"BB",
                 "Brunei Darussalam":"BN",
                 "Bhutan":"BT",
                 "Bouvet Island":"BV",
                 "Botswana":"BW",
                 "Central African Republic":"CF",
                 "Canada":"CA",
                 "Cocos (Keeling) Islands":"CC",
                 "Switzerland":"CH",
                 "Chile":"CL",
                 "China":"CN",
                 "Cameroon":"CM",
                 "Congo, The Democratic Republic of the":"CD",
                 "Congo":"CG",
                 "Cook Islands":"CK",
                 "Colombia":"CO",
                 "Comoros":"KM",
                 "Cabo Verde":"CV",
                 "Costa Rica":"CR",
                 "Cuba":"CU",
                 "Christmas Island":"CX",
                 "Cayman Islands":"KY",
                 "Cyprus":"CY",
                 "Czechia":"CZ",
                 "Germany":"DE",
                 "Djibouti":"DJ",
                 "Dominica":"DM",
                 "Denmark":"DK",
                 "Dominican Republic":"DO",
                 "Algeria":"DZ",
                 "Ecuador":"EC",
                 "Egypt":"EG",
                 "Eritrea":"ER",
                 "Western Sahara":"EH",
                 "Spain":"ES",
                 "Estonia":"EE",
                 "Ethiopia":"ET",
                 "Finland":"FI",
                 "Fiji":"FJ",
                 "Falkland Islands (Malvinas)":"FK",
                 "France":"FR",
                 "Faroe Islands":"FO",
                 "Micronesia, Federated States of":"FM",
                 "Gabon":"GA",
                 "United Kingdom":"GB",
                 "Georgia":"GE",
                 "Guernsey":"GG",
                 "Ghana":"GH",
                 "Gibraltar":"GI",
                 "Guinea":"GN",
                 "Guadeloupe":"GP",
                 "Gambia":"GM",
                 "Guinea-Bissau":"GW",
                 "Equatorial Guinea":"GQ",
                 "Greece":"GR",
                 "Grenada":"GD",
                 "Greenland":"GL",
                 "Guatemala":"GT",
                 "French Guiana":"GF",
                 "Guam":"GU",
                 "Guyana":"GY",
                 "Hong Kong":"HK",
                 "Heard Island and McDonald Islands":"HM",
                 "Honduras":"HN",
                 "Croatia":"HR",
                 "Haiti":"HT",
                 "Hungary":"HU",
                 "Indonesia":"ID",
                 "Isle of Man":"IM",
                 "India":"IN",
                 "British Indian Ocean Territory":"IO",
                 "Ireland":"IE",
                 "Iran, Islamic Republic of":"IR",
                 "Iraq":"IQ",
                 "Iceland":"IS",
                 "Israel":"IL",
                 "Italy":"IT",
                 "Jamaica":"JM",
                 "Jersey":"JE",
                 "Jordan":"JO",
                 "Japan":"JP",
                 "Kazakhstan":"KZ",
                 "Kenya":"KE",
                 "Kyrgyzstan":"KG",
                 "Cambodia":"KH",
                 "Kiribati":"KI",
                 "Saint Kitts and Nevis":"KN",
                 "Korea, Republic of":"KR",
                 "Kuwait":"KW",
                 "Lao People's Democratic Republic":"LA",
                 "Lebanon":"LB",
                 "Liberia":"LR",
                 "Libya":"LY",
                 "Saint Lucia":"LC",
                 "Liechtenstein":"LI",
                 "Sri Lanka":"LK",
                 "Lesotho":"LS",
                 "Lithuania":"LT",
                 "Luxembourg":"LU",
                 "Latvia":"LV",
                 "Macao":"MO",
                 "Saint Martin (French part)":"MF",
                 "Morocco":"MA",
                 "Monaco":"MC",
                 "Moldova, Republic of":"MD",
                 "Madagascar":"MG",
                 "Maldives":"MV",
                 "Mexico":"MX",
                 "Marshall Islands":"MH",
                 "Macedonia, Republic of":"MK",
                 "Mali":"ML",
                 "Malta":"MT",
                 "Myanmar":"MM",
                 "Montenegro":"ME",
                 "Mongolia":"MN",
                 "Northern Mariana Islands":"MP",
                 "Mozambique":"MZ",
                 "Mauritania":"MR",
                 "Montserrat":"MS",
                 "Martinique":"MQ",
                 "Mauritius":"MU",
                 "Malawi":"MW",
                 "Malaysia":"MY",
                 "Mayotte":"YT",
                 "Namibia":"NA",
                 "New Caledonia":"NC",
                 "Niger":"NE",
                 "Norfolk Island":"NF",
                 "Nigeria":"NG",
                 "Nicaragua":"NI",
                 "Niue":"NU",
                 "Netherlands":"NL",
                 "Norway":"NO",
                 "Nepal":"NP",
                 "Nauru":"NR",
                 "New Zealand":"NZ",
                 "Oman":"OM",
                 "Pakistan":"PK",
                 "Panama":"PA",
                 "Pitcairn":"PN",
                 "Peru":"PE",
                 "Philippines":"PH",
                 "Palau":"PW",
                 "Papua New Guinea":"PG",
                 "Poland":"PL",
                 "Puerto Rico":"PR",
                 "Korea, Democratic People's Republic of":"KP",
                 "Portugal":"PT",
                 "Paraguay":"PY",
                 "Palestine, State of":"PS",
                 "French Polynesia":"PF",
                 "Qatar":"QA",
                 "Romania":"RO",
                 "Russian Federation":"RU",
                 "Rwanda":"RW",
                 "Saudi Arabia":"SA",
                 "Sudan":"SD",
                 "Senegal":"SN",
                 "Singapore":"SG",
                 "South Georgia and the South Sandwich Islands":"GS",
                 "Saint Helena, Ascension and Tristan da Cunha":"SH",
                 "Svalbard and Jan Mayen":"SJ",
                 "Solomon Islands":"SB",
                 "Sierra Leone":"SL",
                 "El Salvador":"SV",
                 "San Marino":"SM",
                 "Somalia":"SO",
                 "Saint Pierre and Miquelon":"PM",
                 "Serbia":"RS",
                 "South Sudan":"SS",
                 "Sao Tome and Principe":"ST",
                 "Suriname":"SR",
                 "Slovakia":"SK",
                 "Slovenia":"SI",
                 "Sweden":"SE",
                 "Swaziland":"SZ",
                 "Sint Maarten (Dutch part)":"SX",
                 "Seychelles":"SC",
                 "Syrian Arab Republic":"SY",
                 "Turks and Caicos Islands":"TC",
                 "Chad":"TD",
                 "Togo":"TG",
                 "Thailand":"TH",
                 "Tajikistan":"TJ",
                 "Tokelau":"TK",
                 "Turkmenistan":"TM",
                 "Timor-Leste":"TL",
                 "Tonga":"TO",
                 "Trinidad and Tobago":"TT",
                 "Tunisia":"TN",
                 "Turkey":"TR",
                 "Tuvalu":"TV",
                 "Taiwan, Province of China":"TW",
                 "Tanzania, United Republic of":"TZ",
                 "Uganda":"UG",
                 "Ukraine":"UA",
                 "United States Minor Outlying Islands":"UM",
                 "Uruguay":"UY",
                 "United States":"US",
                 "Uzbekistan":"UZ",
                 "Holy See (Vatican City State)":"VA",
                 "Saint Vincent and the Grenadines":"VC",
                 "Venezuela, Bolivarian Republic of":"VE",
                 "Virgin Islands, British":"VG",
                 "Virgin Islands, U.S.":"VI",
                 "Viet Nam":"VN",
                 "Vanuatu":"VU",
                 "Wallis and Futuna":"WF",
                 "Samoa":"WS",
                 "Yemen":"YE",
                 "South Africa":"ZA",
                 "Zambia":"ZM",
                 "Zimbabwe":"ZW"}

def display(html):
    """Write output (html) to temp file and open in the default web browser."""

    temp_file_name = 'temp-element.html'
    with open(temp_file_name, 'w') as temp_file:
        temp_file.write(html)
    url = 'file://' + os.path.abspath(temp_file_name)
    webbrowser.open(url)

def get_colour_set(name):
    """Get predefined colours list."""

    return COLOURS.get(name)

def get_heat_scale(name):
    """Get predefined heatmap colour scale list."""

    return HEAT_SCALES.get(name)

def get_country_code(country_name):
    """Get 2 letter country code from name"""

    country_name = country_name.replace(',', '')
    for name, code in COUNTRY_CODES.items():
        cleaned = name.replace(',', '')
        if cleaned.lower() == country_name.lower():
            return code
    return None

def get_calculated_colour_scale(colour_list):
    """Convert colour list to plotly colour scale."""

    colour_scale = []
    list_size = len(colour_list)
    if list_size == 1: #single colour, start from white
        colour_list.insert(0, '#FFFFFF')

    step_size = 1/(len(colour_list) - 1)
    step = 0
    for colour in colour_list:
        colour_scale.append([step * step_size, colour])
        step += 1

    return colour_scale

def hex_to_rgb(hex_colour):
    """Convert hex colour to RGB."""

    if hex_colour is not None and hex_colour.startswith('#'):
        hex_code = hex_colour.lstrip('#')
        return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    return None

def get_luma(rgb_colour):
    """Calculate luma value from RGB input colour."""

    luma = (0.2126 * rgb_colour[0])  + (0.7152 * rgb_colour[1]) + (0.0722 * rgb_colour[2])
    return luma
