from flask import Flask, render_template, request
import pickle
import numpy as np

# Define encoding mappings for categorical columns
type_of_payments_mapping = {'CREDIT': 0, 'DEBIT': 1, 'INTERNET BANKING': 2}

						 
customer_city_mapping = {'Aguadilla': 0, 'Alameda': 1, 'Albany': 2, 'Albuquerque': 3, 'Algonquin': 4, 'Alhambra': 5,
                         'Allentown': 6, 'Alpharetta': 7, 'Amarillo': 8, 'Anaheim': 9, 'Ann Arbor': 10, 'Annandale': 11,
						 'Annapolis': 12, 'Antioch': 13, 'Apex': 14, 'Apopka': 15, 'Arecibo': 16, 'Arlington': 17,
						 'Arlington Heights': 18, 'Asheboro': 19, 'Astoria': 20, 'Atlanta': 21, 'Augusta': 22, 'Aurora': 23,
						 'Austin': 24, 'Azusa': 25, 'Bakersfield': 26, 'Baldwin Park': 27, 'Ballwin': 28, 'Baltimore': 29,
						 'Bartlett': 30, 'Bay Shore': 31, 'Bayamon': 32, 'Bayonne': 33, 'Baytown': 34, 'Beaverton': 35,
						 'Bell Gardens': 36, 'Bellflower': 37, 'Bellingham': 38, 'Beloit': 39, 'Bend': 40, 'Bensalem': 41,
						 'Berwyn': 42, 'Billings': 43, 'Birmingham': 44, 'Bismarck': 45, 'Blacksburg': 46, 'Bloomfield': 47,
						 'Bolingbrook': 48, 'Bountiful': 49, 'Bowling Green': 50, 'Brandon': 51, 'Brentwood': 52, 'Bridgeton': 53,
						 'Brighton': 54, 'Bristol': 55, 'Brockton': 56, 'Broken Arrow': 57, 'Bronx': 58, 'Brooklyn': 59,
						 'Broomfield': 60, 'Brownsville': 61, 'Buena Park': 62, 'Buffalo': 63, 'Burnsville': 64, 'Caguas': 65,
						 'Campbell': 66, 'Canoga Park': 67, 'Canovanas': 68, 'Canton': 69, 'Canyon Country': 70, 'Carlisle': 71,
						 'Carlsbad': 72, 'Carmichael': 73, 'Carol Stream': 74, 'Carolina': 75, 'Carrollton': 76, 'Carson': 77, 'Cary': 78,
						 'Catonsville': 79, 'Cayey': 80, 'Cerritos': 81, 'Chambersburg': 82, 'Chandler': 83, 'Chapel Hill': 84,
						 'Charlotte': 85, 'Chesapeake': 86, 'Chicago': 87, 'Chicago Heights': 88, 'Chillicothe': 89, 'Chino': 90,
						 'Chino Hills': 91, 'Chula Vista': 92, 'Cicero': 93, 'Cincinnati': 94, 'Citrus Heights': 95, 'Clarksville': 96,
						 'Clearfield': 97, 'Clementon': 98, 'Cleveland': 99, 'Clovis': 100, 'College Station': 101, 'Colorado Springs': 102,
						 'Colton': 103, 'Columbia': 104, 'Columbus': 105, 'Compton': 106, 'Conway': 107, 'Cordova': 108, 'Corona': 109,
						 'Costa Mesa': 110, 'Crown Point': 111, 'Crystal Lake': 112, 'Cumberland': 113, 'Cupertino': 114, 'Cypress': 115,
						 'Dallas': 116, 'Daly City': 117, 'Danbury': 118, 'Davis': 119, 'Dayton': 120, 'Dearborn': 121, 'Decatur': 122,
						 'Del Rio': 123, 'Denton': 124, 'Denver': 125, 'Des Plaines': 126, 'Detroit': 127, 'Diamond Bar': 128,
						 'Dorchester Center': 129, 'Douglasville': 130, 'Doylestown': 131, 'Dubuque': 132, 'Duluth': 133, 'Dundalk': 134,
						 'Eagle Pass': 135, 'East Brunswick': 136, 'East Lansing': 137, 'Edinburg': 138, 'Edison': 139, 'El Cajon': 140,
						 'El Centro': 141, 'El Monte': 142, 'El Paso': 143, 'Elgin': 144, 'Elk Grove': 145, 'Elmhurst': 146, 'Elyria': 147,
						 'Encinitas': 148, 'Endicott': 149, 'Enfield': 150, 'Englewood': 151, 'Escondido': 152, 'Eugene': 153, 'Everett': 154,
						 'Ewa Beach': 155, 'Fairfield': 156, 'Far Rockaway': 157, 'Fargo': 158, 'Fayetteville': 159, 'Federal Way': 160, 'Findlay': 161,
						 'Florissant': 162, 'Flushing': 163, 'Folsom': 164, 'Fond Du Lac': 165, 'Fontana': 166, 'Forest Hills': 167,
						 'Fort Lauderdale': 168, 'Fort Washington': 169, 'Fort Worth': 170, 'Fountain Valley': 171, 'Frankfort': 172, 'Freehold': 173,
						 'Freeport': 174, 'Fremont': 175, 'Fresno': 176, 'Fullerton': 177, 'Gaithersburg': 178, 'Garden Grove': 179, 'Gardena': 180,
						 'Garland': 181, 'Germantown': 182, 'Gilroy': 183, 'Glen Burnie': 184, 'Glendale': 185, 'Glenview': 186, 'Goleta': 187, 'Goose Creek': 188,
						 'Granada Hills': 189, 'Grand Prairie': 190, 'Granite City': 191, 'Greeley': 192, 'Greensboro': 193, 'Greensburg': 194,
						 'Greenville': 195, 'Grove City': 196, 'Guayama': 197, 'Guaynabo': 198, 'Gwynn Oak': 199, 'Hacienda Heights': 200, 'Hagerstown': 201,
						 'Hamilton': 202, 'Hampton': 203, 'Hamtramck': 204, 'Hanford': 205, 'Hanover': 206, 'Harlingen': 207, 'Harvey': 208,
						 'Hawthorne': 209, 'Hayward': 210, 'Hempstead': 211, 'Henderson': 212, 'Hendersonville': 213, 'Henrico': 214, 'Hesperia': 215,
						 'Hialeah': 216, 'Hickory': 217, 'Highland': 218, 'Highland Park': 219, 'Hilliard': 220, 'Holland': 221, 'Hollister': 222, 'Hollywood': 223,
						 'Honolulu': 224, 'Houston': 225, 'Howell': 226, 'Humacao': 227, 'Huntington Beach': 228, 'Huntington Park': 229, 'Huntington Station': 230,
						 'Hyattsville': 231, 'Indianapolis': 232, 'Indio': 233, 'Irving': 234, 'Irvington': 235, 'Irwin': 236, 'Ithaca': 237, 'Jackson': 238,
						 'Jackson Heights': 239, 'Jacksonville': 240, 'Jamaica': 241, 'Jersey City': 242, 'Joliet': 243, 'Jonesboro': 244, 'Juana Diaz': 245,
						 'Kailua': 246, 'Kaneohe': 247, 'Katy': 248, 'Kenner': 249, 'Kent': 250, 'Knoxville': 251, 'La Crosse': 252, 'La Habra': 253, 'La Mesa': 254,
						 'La Mirada': 255, 'La Puente': 256, 'Laguna Hills': 257, 'Laguna Niguel': 258, 'Lake Forest': 259, 'Lakewood': 260, 'Lancaster': 261,
						 'Lansdale': 262, 'Laredo': 263, 'Las Cruces': 264, 'Las Vegas': 265, 'Lawrence': 266, 'Lawrenceville': 267, 'Lawton': 268, 'Lenoir': 269,
						 'Levittown': 270, 'Lewisville': 271, 'Lilburn': 272, 'Lindenhurst': 273, 'Lithonia': 274, 'Littleton': 275, 'Livermore': 276, 'Lockport': 277,
						 'Lodi': 278, 'Lombard': 279, 'Lompoc': 280, 'Long Beach': 281, 'Longmont': 282, 'Longview': 283, 'Los Angeles': 284, 'Louisville': 285,
						 'Loveland': 286, 'Lutz': 287, 'Lynn': 288, 'Lynnwood': 289, 'Lynwood': 290, 'Madera': 291, 'Madison': 292, 'Malden': 293, 'Manati': 294,
						 'Manchester': 295, 'Marietta': 296, 'Marion': 297, 'Marrero': 298, 'Martinez': 299, 'Martinsburg': 300, 'Massapequa': 301, 'Massillon': 302,
						 'Mayaguez': 303, 'Mcallen': 304, 'Mchenry': 305, 'Mechanicsburg': 306, 'Medford': 307, 'Medina': 308, 'Memphis': 309, 'Mentor': 310,
						 'Merced': 311, 'Meridian': 312, 'Mesa': 313, 'Mesquite': 314, 'Metairie': 315, 'Methuen': 316, 'Miami': 317, 'Michigan City': 318,
						 'Middletown': 319, 'Milford': 320, 'Mililani': 321, 'Milpitas': 322, 'Milwaukee': 323, 'Mission': 324, 'Mission Viejo': 325, 'Modesto': 326,
						 'Moline': 327, 'Montebello': 328, 'Moreno Valley': 329, 'Morganton': 330, 'Morristown': 331, 'Morrisville': 332, 'Mount Pleasant': 333,
						 'Mount Prospect': 334, 'Murfreesboro': 335, 'Muskegon': 336, 'Napa': 337, 'Nashville': 338, 'National City': 339, 'New Albany': 340,
						 'New Bedford': 341, 'New Braunfels': 342, 'New Brunswick': 343, 'New Castle': 344, 'New Haven': 345, 'New Orleans': 346, 'New York': 347,
						 'Newark': 348, 'Newburgh': 349, 'Norcross': 350, 'Norfolk': 351, 'Normal': 352, 'North Bergen': 353, 'North Hills': 354,
						 'North Hollywood': 355, 'North Las Vegas': 356, 'North Richland Hills': 357, 'North Tonawanda': 358, 'Norwalk': 359, 'O Fallon': 360,
						 'Oak Lawn': 361, 'Oakland': 362, 'Oceanside': 363, 'Ogden': 364, 'Olathe': 365, 'Ontario': 366, 'Opa Locka': 367, 'Opelousas': 368,
						 'Orange Park': 369, 'Oregon City': 370, 'Orlando': 371, 'Oviedo': 372, 'Oxnard': 373, 'Pacoima': 374, 'Painesville': 375, 'Palatine': 376,
						 'Palmdale': 377, 'Palo Alto': 378, 'Panorama City': 379, 'Paramount': 380, 'Parkville': 381, 'Pasadena': 382, 'Passaic': 383,
						 'Pawtucket': 384, 'Peabody': 385, 'Pekin': 386, 'Peoria': 387, 'Perth Amboy': 388, 'Pharr': 389, 'Philadelphia': 390, 'Phoenix': 391,
						 'Pico Rivera': 392, 'Piscataway': 393, 'Pittsburg': 394, 'Pittsfield': 395, 'Placentia': 396, 'Plainfield': 397, 'Plano': 398,
						 'Plymouth': 399, 'Pomona': 400, 'Pompano Beach': 401, 'Ponce': 402, 'Porterville': 403, 'Portland': 404, 'Potomac': 405, 'Poway': 406, 
						 'Powder Springs': 407, 'Princeton': 408, 'Provo': 409, 'Quincy': 410, 'Raleigh': 411, 'Rancho Cordova': 412, 'Rancho Cucamonga': 413,
						 'Redmond': 414, 'Rego Park': 415, 'Reno': 416, 'Reseda': 417, 'Revere': 418, 'Reynoldsburg': 419, 'Rialto': 420, 'Richardson': 421,
						 'Richmond': 422, 'Ridgewood': 423, 'Rio Grande': 424, 'Rio Rancho': 425, 'Riverside': 426, 'Rochester': 427, 'Rock Hill': 428, 'Rome': 429,
						 'Roseburg': 430, 'Rosemead': 431, 'Roseville': 432, 'Roswell': 433, 'Round Rock': 434, 'Rowland Heights': 435, 'Sacramento': 436,
						 'Saginaw': 437, 'Saint Charles': 438, 'Saint Louis': 439, 'Saint Paul': 440, 'Saint Peters': 441, 'Salem': 442, 'Salina': 443, 'Salinas': 444,
						 'Salt Lake City': 445, 'San Antonio': 446, 'San Benito': 447, 'San Bernardino': 448, 'San Diego': 449, 'San Francisco': 450, 'San Jose': 451,
						 'San Juan': 452, 'San Marcos': 453, 'San Pablo': 454, 'San Pedro': 455, 'San Ramon': 456, 'San Sebastian': 457, 'Sandusky': 458,
						 'Sanford': 459, 'Santa Ana': 460, 'Santa Clara': 461, 'Santa Cruz': 462, 'Santa Fe': 463, 'Santa Maria': 464, 'Santee': 465, 
						 'Scottsdale': 466, 'Seattle': 467, 'Sheboygan': 468, 'Silver Spring': 469, 'Simi Valley': 470, 'Smyrna': 471, 'South El Monte': 472, 
						 'South Gate': 473, 'South Ozone Park': 474, 'South Richmond Hill': 475, 'South San Francisco': 476, 'Spokane': 477, 'Spring': 478, 
						 'Spring Valley': 479, 'Springfield': 480, 'Stafford': 481, 'Stamford': 482, 'Staten Island': 483, 'Stockbridge': 484, 'Stockton': 485, 
						 'Stone Mountain': 486, 'Strongsville': 487, 'Sugar Land': 488, 'Summerville': 489, 'Sumner': 490, 'Sun Valley': 491, 'Sunnyvale': 492, 
						 'Sylmar': 493, 'Tallahassee': 494, 'Tampa': 495, 'Taunton': 496, 'Taylor': 497, 'Temecula': 498, 'Tempe': 499, 'Tinley Park': 500, 
						 'Toa Alta': 501, 'Toa Baja': 502, 'Toms River': 503, 'Tonawanda': 504, 'Tracy': 505, 'Troy': 506, 'Trujillo Alto': 507, 'Tucson': 508, 
						 'Tulare': 509, 'Tustin': 510, 'Union': 511, 'Union City': 512, 'Upland': 513, 'Vacaville': 514, 'Vallejo': 515, 'Valrico': 516, 
						 'Van Nuys': 517, 'Vega Baja': 518, 'Ventura': 519, 'Victorville': 520, 'Virginia Beach': 521, 'Visalia': 522, 'Vista': 523, 'Waipahu': 524,
						 'Walnut': 525, 'Warren': 526, 'Washington': 527, 'Watsonville': 528, 'Waukegan': 529, 'Wayne': 530, 'Webster': 531, 'Weslaco': 532,
						 'West Chester': 533, 'West Covina': 534, 'West Haven': 535, 'West Jordan': 536, 'West Lafayette': 537, 'West New York': 538,
						 'West Orange': 539, 'Westerville': 540, 'Westland': 541, 'Westminster': 542, 'Wheaton': 543, 'Wheeling': 544, 'Wichita': 545,
						 'Wilkes Barre': 546, 'Williamsport': 547, 'Wilmington': 548, 'Winnetka': 549, 'Winter Park': 550, 'Woodbridge': 551, 'Woodside': 552, 
						 'Woonsocket': 553, 'Wyandotte': 554, 'Wyoming': 555, 'Yauco': 556, 'Yonkers': 557, 'York': 558, 'Ypsilanti': 559, 'Yuma': 560, 
						 'Zanesville': 561}


order_country_mapping = {'Afghanistan': 0, 'Albania': 1, 'Algeria': 2, 'Angola': 3, 'Argentina': 4, 'Armenia': 5, 'Australia': 6, 'Austria': 7,
                         'Azerbaijan': 8, 'Bangladesh': 9, 'Barbados': 10, 'Belarus': 11, 'Belgium': 12, 'Belice': 13, 'Benin': 14, 'Bhutan': 15,
						 'Bolivia': 16, 'Bosnia and Herzegovina': 17, 'Botswana': 18, 'Brazil': 19, 'Bulgaria': 20, 'Burkina Faso': 21, 'Burundi': 22,
						 'Cambodia': 23, 'Cameroon': 24, 'Canada': 25, 'Central African Republic': 26, 'Chad': 27, 'Chile': 28, 'China': 29, 'Chipre': 30,
						 'Colombia': 31, 'Costa Rica': 32, 'Croatia': 33, 'Cuba': 34, 'Czech Republic': 35, 'Democratic Republic of the Congo': 36,
						 'Denmark': 37, 'Djibouti': 38, 'Dominican Republic': 39, 'Ecuador': 40, 'Egypt': 41, 'El Salvador': 42, 'Equatorial Guinea': 43,
						 'Eritrea': 44, 'Estonia': 45, 'Eswatini': 46, 'Ethiopia': 47, 'Finland': 48, 'France': 49, 'French Guiana': 50, 'Gabon': 51,
						 'Georgia': 52, 'Germany': 53, 'Ghana': 54, 'Grecia': 55, 'Guadeloupe': 56, 'Guatemala': 57, 'Guinea': 58, 'Guinea-Bissau': 59,
						 'Guyana': 60, 'Haiti': 61, 'Honduras': 62, 'Hong Kong': 63, 'Hungary': 64, 'India': 65, 'Indonesia': 66, 'Iran': 67, 'Iraq': 68,
						 'Ireland': 69, 'Israel': 70, 'Italy': 71, 'Ivory Coast': 72, 'Jamaica': 73, 'Japan': 74, 'Jordan': 75, 'Kazakhstan': 76, 'Kenya': 77,
						 'Kuwait': 78, 'Kyrgyzstan': 79, 'Laos': 80, 'Lebanon': 81, 'Lesotho': 82, 'Liberia': 83, 'Libya': 84, 'Lithuania': 85, 'Luxembourg': 86,
						 'Madagascar': 87, 'Malaysia': 88, 'Mali': 89, 'Martinique': 90, 'Mauritania': 91, 'Mexico': 92, 'Moldova': 93, 'Mongolia': 94,
						 'Montenegro': 95, 'Morocco': 96, 'Mozambique': 97, 'Myanmar': 98, 'Namibia': 99, 'Nepal': 100, 'Netherlands': 101, 'New Zealand': 102,
						 'Nicaragua': 103, 'Niger': 104, 'Nigeria': 105, 'North Macedonia': 106, 'Norway': 107, 'Oman': 108, 'Pakistan': 109, 'Panama': 110, 
						 'Papua New Guinea': 111, 'Paraguay': 112, 'Peru': 113, 'Philippines': 114, 'Poland': 115, 'Portugal': 116, 'Qatar': 117, 
						 'Republic of the Congo': 118, 'Romania': 119, 'Russia': 120, 'Rwanda': 121, 'Saudi Arabia': 122, 'Senegal': 123, 'Serbia': 124, 
						 'Sierra Leone': 125, 'Singapore': 126, 'Slovakia': 127, 'Slovenia': 128, 'Somalia': 129, 'South Africa': 130, 'South Korea': 131, 
						 'South Sudan': 132, 'Spain': 133, 'Sri Lanka': 134, 'Sudan': 135, 'Surinam': 136, 'Sweden': 137, 'Switzerland': 138, 'Syria': 139, 
						 'Taiwan': 140, 'Tajikistan': 141, 'Tanzania': 142, 'Thailand': 143, 'The Gambia': 144, 'Togo': 145, 'Trinidad and Tobago': 146, 
						 'Tunisia': 147, 'Turkey': 148, 'Turkmenistan': 149, 'Uganda': 150, 'Ukraine': 151, 'United Arab Emirates': 152, 'United Kingdom': 153,
						 'United States': 154, 'Uruguay': 155, 'Uzbekistan': 156, 'Venezuela': 157, 'Vietnam': 158, 'Western Sahara': 159, 'Yemen': 160, 
						 'Zambia': 161, 'Zimbabwe': 162}
						 
						 
order_status_mapping =  {'ON_HOLD': 0, 'PAYMENT_REVIEW': 1, 'PENDING_MANUFACTURING': 2, 'PENDING_PAYMENT': 3, 'PROCESSING': 4, 'SUSPECTED_FRAUD': 5}
						 
product_name_mapping =  {"Diamondback Women's Serene Classic Comfort Bi": 0, 
                         'Field & Stream Sportsman 16 Gun Fire Safe': 1,
						 "Nike Men's CJ Elite 2 TD Football Cleat": 2,
						 "Nike Men's Dri-FIT Victory Golf Polo": 3,
						 "Nike Men's Free 5.0+ Running Shoe": 4,
						 "O'Brien Men's Neoprene Life Vest": 5,
						 'Others': 6,
						 'Pelican Sunstream 100 Kayak': 7,
						 'Perfect Fitness Perfect Rip Deck': 8,
						 "Under Armour Girls Toddler Spine Surge Runni": 9}
						 
shipping_mode_mapping = {'First Class': 0, 'Same Day': 1, 'Second Class': 2, 'Standard Class': 3}


app = Flask(__name__)

# Load the pickled machine learning model
model = pickle.load(open('ml_model.pkl','rb'))


@app.route('/')
def index():
    return render_template('index.html', customer_city_mapping=customer_city_mapping)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user input data from the form
        type_of_payments_text = (request.form['type_of_payments'])
        type_of_payments = type_of_payments_mapping.get(type_of_payments_text)
              
        customer_city_text = (request.form['customer_city'])
        customer_city = customer_city_mapping.get(customer_city_text)
        
        order_country_text = (request.form['order_country'])
        order_country = order_country_mapping.get(order_country_text)
        
        order_status_text = (request.form['order_status'])
        order_status = order_status_mapping.get(order_status_text)
        
        product_name_text = (request.form['product_name'])
        product_name = order_status_mapping.get(product_name_text)
        
        shipping_mode_text = (request.form['shipping_mode'])
        shipping_mode = shipping_mode_mapping.get(shipping_mode_text)
        
        days_for_shipment = int(request.form['days_for_shipment'])
        order_day = int(request.form['order_day'])
        order_month = int(request.form['order_month'])
        shipping_day = int(request.form['shipping_day'])
        shipping_month = int(request.form['shipping_month'])

        # Create a feature vector from the user input
        input_data = [type_of_payments, days_for_shipment, customer_city, order_country, order_status, product_name,
                      shipping_mode, order_day, order_month, shipping_day, shipping_month]

        # Make a prediction using the loaded model
        result = model.predict(np.array([input_data]).reshape(1, 11))

        # Return the prediction as text
        if result[0] == 1:
         result = 'Delivery will be Late'
        else:
         result = 'Delivery will be Ontime'
         
        return render_template('index.html',result=result)

    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)


