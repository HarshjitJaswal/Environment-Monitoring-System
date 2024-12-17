from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

def get_data(url):
 
    response = requests.get(url)
    return response.text

def get_element_text(soup, class_name):

    element = soup.find(class_=class_name)
    return element.text if element else "N/A"

def fetch_weather_and_aqi(city):


    wqi_data = {
    "Agartala": {"wqi": 72, "hardness": 140, "turbidity": 3, "pH": 7.3, "nitrates": 12, "chlorides": 18},
    "Aizawl": {"wqi": 68, "hardness": 130, "turbidity": 2, "pH": 7.5, "nitrates": 10, "chlorides": 15},
    "Amravati": {"wqi": 70, "hardness": 120, "turbidity": 3, "pH": 7.2, "nitrates": 10, "chlorides": 15},
    "Bengaluru": {"wqi": 88, "hardness": 180, "turbidity": 4, "pH": 7.3, "nitrates": 15, "chlorides": 20},
    "Bhopal": {"wqi": 82, "hardness": 170, "turbidity": 4, "pH": 7.4, "nitrates": 16, "chlorides": 18},
    "Bhubaneshwar": {"wqi": 76, "hardness": 150, "turbidity": 3, "pH": 7.3, "nitrates": 13, "chlorides": 20},
    "Chandigarh": {"wqi": 68, "hardness": 140, "turbidity": 2, "pH": 7.6, "nitrates": 8, "chlorides": 14},
    "Chennai": {"wqi": 90, "hardness": 250, "turbidity": 6, "pH": 7.0, "nitrates": 35, "chlorides": 45},
    "Dehradun": {"wqi": 62, "hardness": 110, "turbidity": 2, "pH": 7.5, "nitrates": 8, "chlorides": 10},
    "Delhi": {"wqi": 120, "hardness": 300, "turbidity": 8, "pH": 7.0, "nitrates": 45, "chlorides": 60},
    "Dispur": {"wqi": 78, "hardness": 140, "turbidity": 4, "pH": 7.3, "nitrates": 15, "chlorides": 20},
    "Gangtok": {"wqi": 65, "hardness": 90, "turbidity": 1, "pH": 7.7, "nitrates": 5, "chlorides": 8},
    "Gandhinagar": {"wqi": 75, "hardness": 160, "turbidity": 3, "pH": 7.3, "nitrates": 12, "chlorides": 18},
    "Hyderabad": {"wqi": 88, "hardness": 210, "turbidity": 5, "pH": 7.2, "nitrates": 25, "chlorides": 35},
    "Imphal": {"wqi": 64, "hardness": 120, "turbidity": 2, "pH": 7.6, "nitrates": 8, "chlorides": 14},
    "Indore": {"wqi": 85, "hardness": 150, "turbidity": 5, "pH": 7.4, "nitrates": 20, "chlorides": 25},
    "Itanagar": {"wqi": 65, "hardness": 100, "turbidity": 2, "pH": 7.5, "nitrates": 5, "chlorides": 10},
    "Jaipur": {"wqi": 80, "hardness": 190, "turbidity": 5, "pH": 7.2, "nitrates": 18, "chlorides": 28},
    "Kohima": {"wqi": 60, "hardness": 100, "turbidity": 2, "pH": 7.6, "nitrates": 6, "chlorides": 10},
    "Kolkata": {"wqi": 100, "hardness": 220, "turbidity": 6, "pH": 7.1, "nitrates": 30, "chlorides": 40},
    "Lucknow": {"wqi": 92, "hardness": 250, "turbidity": 6, "pH": 7.0, "nitrates": 38, "chlorides": 45},
    "Mumbai": {"wqi": 78, "hardness": 140, "turbidity": 4, "pH": 7.3, "nitrates": 15, "chlorides": 20},
    "Panaji": {"wqi": 50, "hardness": 80, "turbidity": 1, "pH": 7.8, "nitrates": 2, "chlorides": 8},
    "Patna": {"wqi": 110, "hardness": 280, "turbidity": 7, "pH": 6.8, "nitrates": 40, "chlorides": 50},
    "Port Blair": {"wqi": 55, "hardness": 90, "turbidity": 1, "pH": 7.8, "nitrates": 4, "chlorides": 10},
    "Raipur": {"wqi": 95, "hardness": 220, "turbidity": 6, "pH": 7.1, "nitrates": 30, "chlorides": 35},
    "Ranchi": {"wqi": 80, "hardness": 200, "turbidity": 5, "pH": 7.2, "nitrates": 18, "chlorides": 22},
    "Shillong": {"wqi": 62, "hardness": 100, "turbidity": 2, "pH": 7.6, "nitrates": 6, "chlorides": 12},
    "Shimla": {"wqi": 55, "hardness": 100, "turbidity": 1, "pH": 7.8, "nitrates": 5, "chlorides": 8},
    "Thiruvananthapuram": {"wqi": 60, "hardness": 90, "turbidity": 2, "pH": 7.7, "nitrates": 6, "chlorides": 10},
}


    city_urls = {
        "Indore": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/d2127eb893261f5c537714fdcc4bf073db5ad330d0c26ed760f72eb6490b1b5d",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/b6c506855476ef08fa24b0e8b0599537cadb223217fcf3919a51d50cc560b02e"
        },
        "Delhi": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/7df684d64bef23f80b45fb8005de7a411d1fde0976ef68d6957ea74b18b54bad",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/7df684d64bef23f80b45fb8005de7a411d1fde0976ef68d6957ea74b18b54bad"
        },
        "Amravati": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/b68d8f5a2517a846162117f3e770b029202795bb4b4bfe966953ec46560b1c71",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/b68d8f5a2517a846162117f3e770b029202795bb4b4bfe966953ec46560b1c71"
        },
        "Itanagar": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/a65900cafeb56b5dfacc08e6413afb09dfcf3b92ad9274174ef87626c63e21f8",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/a65900cafeb56b5dfacc08e6413afb09dfcf3b92ad9274174ef87626c63e21f8"
        },
        "Dispur": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/295460865f918c444ca0e921ed39eec90c68a5e1f9b75a5735be52550abae134",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/295460865f918c444ca0e921ed39eec90c68a5e1f9b75a5735be52550abae134"
        },
        "Patna": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/dc8b55be016a7c061cad2bff2654fb5d9f29d027b7d4718880d5efa395b319b5",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/dc8b55be016a7c061cad2bff2654fb5d9f29d027b7d4718880d5efa395b319b5"
        },
        "Raipur": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/3c0fe849a34778fb02848a491d2b68dd74786eeab0b0a805f66387eb8ccc81db",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/3c0fe849a34778fb02848a491d2b68dd74786eeab0b0a805f66387eb8ccc81db"
        },
        "Panaji": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/2eb20ffd629cf480682dc7bea396a7add4e4fe4ecbf492dbcf405b508bfe28d9",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/2eb20ffd629cf480682dc7bea396a7add4e4fe4ecbf492dbcf405b508bfe28d9"
        },
        "Gandhinagar": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/65d2079f9985eb80a9fb20c1a6fcea3dfc423d796d475e39e0b787ec3f6e1a4b",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/65d2079f9985eb80a9fb20c1a6fcea3dfc423d796d475e39e0b787ec3f6e1a4b"
        },
        "Chandigarh": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/90fc2f940550fbe04ddd94bbb14b1620de325addf134cb3996bd92e4ed4e7aa6",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/90fc2f940550fbe04ddd94bbb14b1620de325addf134cb3996bd92e4ed4e7aa6"
        },
        "Shimla": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/90fc2f940550fbe04ddd94bbb14b1620de325addf134cb3996bd92e4ed4e7aa6",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/90fc2f940550fbe04ddd94bbb14b1620de325addf134cb3996bd92e4ed4e7aa6"
        },
        "Ranchi": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/1d44035189855ee1c6bad3b809bfd30ab217f79ee5e5777d2dd83bacd468ecf1",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/1d44035189855ee1c6bad3b809bfd30ab217f79ee5e5777d2dd83bacd468ecf1"
        },
        "Bengaluru": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/f5720f935015d866abbc8f4d5beefe74b16a77fe84928669d117dd882d7de136",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/f5720f935015d866abbc8f4d5beefe74b16a77fe84928669d117dd882d7de136"
        },
        "Thiruvananthanampuram": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/08e6e495dfab82c12bed1cdac92fef3a0d53cdf402e0c63088a26a73a189e935",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/08e6e495dfab82c12bed1cdac92fef3a0d53cdf402e0c63088a26a73a189e935"
        },
        "Bhopal": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/05e7b55c678ebb62b396550a1b36efabcd59ef28ba9c94e8ee024d9b4faafc50",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/05e7b55c678ebb62b396550a1b36efabcd59ef28ba9c94e8ee024d9b4faafc50"
        },
        "Mumbai": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/cb022e27867bb250b801b119170ab9889e1bc3b65e50c76798362b7f95d29248",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/cb022e27867bb250b801b119170ab9889e1bc3b65e50c76798362b7f95d29248"
        },
        "Imphal": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/039b5ffa8ca19b1864f62334713f93761faa897ccbdf9af9f0b7420851c02d4c",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/039b5ffa8ca19b1864f62334713f93761faa897ccbdf9af9f0b7420851c02d4c"
        },
        "Shillong": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/a84a4461188ba8fd2b4d527125b092aa12e6afd2c7c0e37ef6e314b8804c4412",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/a84a4461188ba8fd2b4d527125b092aa12e6afd2c7c0e37ef6e314b8804c4412"
        },
        "Aizawl": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/c4ed6ddd891a058ba02482f96ac7f270eb7a93f8fd7ae768a7a4c6f5ff989e90",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/c4ed6ddd891a058ba02482f96ac7f270eb7a93f8fd7ae768a7a4c6f5ff989e90"
        },
        "Kohima": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/aeec7de43b9e5cf31cba3e53acc9fc48b312037d1a2789e6fdacf2010313464e",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/aeec7de43b9e5cf31cba3e53acc9fc48b312037d1a2789e6fdacf2010313464e"
        },
        "Bhubaneshwar": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/adde17ab72947ee24a5d5ec7d6da72005c70951e1fbf7c17bd57758d4d87505a",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/adde17ab72947ee24a5d5ec7d6da72005c70951e1fbf7c17bd57758d4d87505a"
        },
        "Jaipur": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/bb0b93113780827f5d791397c67cd20e9d3c0f18a6656c9bbea44304836c9b75",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/bb0b93113780827f5d791397c67cd20e9d3c0f18a6656c9bbea44304836c9b75"
        },
        "Gangtok": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/d1b325183bc25dbeec0b7f2f87bd62e8abca70651eaf5ff8567681901b01429f",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/d1b325183bc25dbeec0b7f2f87bd62e8abca70651eaf5ff8567681901b01429f"
        },
        "Chennai": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/6c19f3b624bdb24ff5a5a80ec001f2e5e83f111aa6edc1117813938e3eae0c65",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/6c19f3b624bdb24ff5a5a80ec001f2e5e83f111aa6edc1117813938e3eae0c65"
        },
        "Hyderabad": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/53adaee7896cbfa21ca6b883fa16ee82861055b2f0a3c74bc9e8634dbde671e0",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/53adaee7896cbfa21ca6b883fa16ee82861055b2f0a3c74bc9e8634dbde671e0"
        },
        "Agartala": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/aa4694c846411a50679db67af4b3cb1d756601ee68ab3705922918f67ec4bdb7",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/aa4694c846411a50679db67af4b3cb1d756601ee68ab3705922918f67ec4bdb7"
        },
        "Lucknow": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/7a5b020a07be200832bed150335d76c57be3339cb17b30975d1700474c561d15",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/7a5b020a07be200832bed150335d76c57be3339cb17b30975d1700474c561d15"
        },
        "Dehradun": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/fffaeda69422367a6a6f59117c383e4f2ec945cc01a769d48704f1599b02f7e3",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/fffaeda69422367a6a6f59117c383e4f2ec945cc01a769d48704f1599b02f7e3"
        },
        "Kolkata": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/339b7a9f50c03758e4ad945ca0dcfe641a1b2b7a3b0d6e8e920d7a046cd061e7",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/339b7a9f50c03758e4ad945ca0dcfe641a1b2b7a3b0d6e8e920d7a046cd061e7"
        },
        "Port Blair": {
            "weather_url": "https://weather.com/en-IN/weather/today/l/d4baf0985360b46bdd69e782c34fe9528740457dd74abf7b3eb4b84a8fa9d1ea",
            "aqi_url": "https://weather.com/en-IN/forecast/air-quality/l/d4baf0985360b46bdd69e782c34fe9528740457dd74abf7b3eb4b84a8fa9d1ea"
        },
    }

  
    aqi_html = get_data(city_urls[city]["aqi_url"])
    aqi_soup = BeautifulSoup(aqi_html, 'html.parser')
    res_data = get_element_text(aqi_soup, "DonutChart--innerValue--VRvST AirQuality--extendedDialText--ADw3D")
    air_data = aqi_soup.find_all(class_="DonutChart--innerValue--VRvST AirQuality--pollutantDialText--LWsHZ")
    air_data = [data.text for data in air_data] if air_data else ["N/A"] * 6
    
  
    weather_html = get_data(city_urls[city]["weather_url"])
    weather_soup = BeautifulSoup(weather_html, 'html.parser')
    r_data = get_element_text(weather_soup, "CurrentConditions--tempValue--zUBSz")
    w_data = weather_soup.find_all(class_="WeatherDetailsListItem--wxData--lW-7H")
    w_data = [data.text for data in w_data] if w_data else ["N/A"] * 7
    uv_index = float(w_data[5]) if len(w_data) > 5 and w_data[5].replace('.', '', 1).isdigit() else 0
    humidity = int(w_data[2].strip('%')) if len(w_data) > 2 and w_data[2].strip('%').isdigit() else 0
    visibility_text = w_data[6] if len(w_data) > 6 else "N/A"  
    try:
        visibility = float(visibility_text.split()[0]) if "km" in visibility_text else 0
        if visibility_text =="Unlimited":visibility=1000
    except ValueError:
        visibility = 0  
    print(visibility)   
    res = int(res_data) if res_data.isdigit() else 0
    if res <= 50:
        remark = "Good"
        impact = "Minimal impact"
    elif res <= 100:
        remark = "Satisfactory"
        impact = "Minor breathing discomfort to sensitive people"
    elif res <= 200:
        remark = "Moderate"
        impact = "Breathing discomfort to people with lung, asthma, and heart diseases"
    elif res <= 400:
        remark = "Very Poor"
        impact = "Breathing discomfort to most people on prolonged exposure"
    else:
        remark = "Severe"
        impact = "Affects healthy people and seriously impacts those with existing diseases"
    precautions = []
    if res > 100:
        precautions.append("Use an air purifier indoors if possible.")
    if res > 200:
        precautions.append("Wear an N95 mask to protect yourself from air pollution.")
        precautions.append("Limit outdoor activities to avoid health risks.")
    if uv_index > 7:
        precautions.append("Wear sunglasses and reapply sunscreen every 2 hours.")
        precautions.append("Avoid direct sun exposure during peak hours (10 AM - 4 PM).")
    if humidity > 98:
        precautions.append("Carry an umbrella to avoid discomfort from rainfall.")
    if humidity > 80:
        precautions.append("Wear breathable clothing to stay comfortable in high humidity.")
    if visibility < 1:
        precautions.append("Use fog lights while driving and avoid unnecessary travel.")

    precaution_remark = " ".join(precautions) if precautions else "No specific precautions are required."
  
    current_time = time.strftime("%H:%M:%S", time.localtime())

 
    wqi_details = wqi_data.get(city, {})
    return {
        "city": city,
        "temperature": r_data,
        "wind": w_data[1] if len(w_data) > 1 else "N/A",
        "humidity": w_data[2] if len(w_data) > 2 else "N/A",
        "dew_point": w_data[3] if len(w_data) > 3 else "N/A",
        "pressure": w_data[4] if len(w_data) > 4 else "N/A",
        "uv_index": w_data[5] if len(w_data) > 5 else "N/A",
        "visibility": w_data[6] if len(w_data) > 6 else "N/A",
        "moon_phase": w_data[7] if len(w_data) > 7 else "N/A",
        "aqi": res_data,
        "o3": air_data[0] if len(air_data) > 0 else "N/A",
        "no2": air_data[1] if len(air_data) > 1 else "N/A",
        "so2": air_data[2] if len(air_data) > 2 else "N/A",
        "pm10": air_data[3] if len(air_data) > 3 else "N/A",
        "pm2_5": air_data[4] if len(air_data) > 4 else "N/A",
        "co": air_data[5] if len(air_data) > 5 else "N/A",
        "remark": remark,
        "impact": impact,
        "precaution_remark": precaution_remark,
        "wqi": wqi_data.get(city, "N/A"),
        "current_time": current_time,
        **wqi_details,
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_city = "Bhopal" 

    if request.method == 'POST':
        selected_city = request.form['city']

    data = fetch_weather_and_aqi(selected_city)
    return render_template("index.html", data=data, cities=["Agartala", "Aizawl", "Amravati", "Bengaluru", "Bhopal", "Bhubaneshwar", "Chandigarh", "Chennai", "Dehradun", "Delhi", "Dispur", "Gangtok", "Gandhinagar", "Hyderabad", "Imphal", "Indore", "Itanagar", "Jaipur", "Kohima", "Kolkata", "Lucknow", "Mumbai", "Panaji", "Patna", "Port Blair", "Raipur", "Ranchi", "Shillong", "Shimla", "Thiruvananthapuram"]
)
if __name__ == '__main__':
    app.run(debug=True)
