import requests
import json
import threading
import time
import os
import flag
import math
from datetime import datetime
from flask import Flask, render_template, request
import pycountry

app = Flask(__name__)
data_file = "dataransom.json"
data = []

country_flags = {
    "AF": '🇦🇫',
    "AX": '🇦🇽',
    "AL": '🇦🇱',
    "DZ": '🇩🇿',
    "AS": '🇦🇸',
    "AD": '🇦🇩',
    "AO": '🇦🇴',
    "AI": '🇦🇮',
    "AQ": '🇦🇶',
    "AG": '🇦🇬',
    "AR": '🇦🇷',
    "AM": '🇦🇲',
    "AW": '🇦🇼',
    "AU": '🇦🇺',
    "AT": '🇦🇹',
    "AZ": '🇦🇿',
    "BS": '🇧🇸',
    "BH": '🇧🇭',
    "BD": '🇧🇩',
    "BB": '🇧🇧',
    "BY": '🇧🇾',
    "BE": '🇧🇪',
    "BZ": '🇧🇿',
    "BJ": '🇧🇯',
    "BM": '🇧🇲',
    "BT": '🇧🇹',
    "BO": '🇧🇴',
    "BA": '🇧🇦',
    "BW": '🇧🇼',
    "BR": '🇧🇷',
    "IO": '🇮🇴',
    "VG": '🇻🇬',
    "BN": '🇧🇳',
    "BG": '🇧🇬',
    "BF": '🇧🇫',
    "BI": '🇧🇮',
    "KH": '🇰🇭',
    "CM": '🇨🇲',
    "CA": '🇨🇦',
    "CV": '🇨🇻',
    "BQ": '🇧🇶',
    "KY": '🇰🇾',
    "CF": '🇨🇫',
    "TD": '🇹🇩',
    "CL": '🇨🇱',
    "CN": '🇨🇳',
    "CX": '🇨🇽',
    "CC": '🇨🇨',
    "CO": '🇨🇴',
    "KM": '🇰🇲',
    "CG": '🇨🇬',
    "CK": '🇨🇰',
    "CR": '🇨🇷',
    "HR": '🇭🇷',
    "CU": '🇨🇺',
    "CW": '🇨🇼',
    "CY": '🇨🇾',
    "CZ": '🇨🇿',
    "CD": '🇨🇩',
    "DK": '🇩🇰',
    "DJ": '🇩🇯',
    "DM": '🇩🇲',
    "DO": '🇩🇴',
    "EC": '🇪🇨',
    "EG": '🇪🇬',
    "SV": '🇸🇻',
    "GQ": '🇬🇶',
    "ER": '🇪🇷',
    "EE": '🇪🇪',
    "ET": '🇪🇹',
    "FK": '🇫🇰',
    "FO": '🇫🇴',
    "FM": '🇫🇲',
    "FJ": '🇫🇯',
    "FI": '🇫🇮',
    "FR": '🇫🇷',
    "GF": '🇬🇫',
    "PF": '🇵🇫',
    "TF": '🇹🇫',
    "GA": '🇬🇦',
    "GM": '🇬🇲',
    "GE": '🇬🇪',
    "DE": '🇩🇪',
    "GH": '🇬🇭',
    "GI": '🇬🇮',
    "GR": '🇬🇷',
    "GL": '🇬🇱',
    "GD": '🇬🇩',
    "GP": '🇬🇵',
    "GU": '🇬🇺',
    "GT": '🇬🇹',
    "GN": '🇬🇳',
    "GW": '🇬🇼',
    "GY": '🇬🇾',
    "HT": '🇭🇹',
    "HN": '🇭🇳',
    "HK": '🇭🇰',
    "HU": '🇭🇺',
    "IS": '🇮🇸',
    "IN": '🇮🇳',
    "ID": '🇮🇩',
    "IR": '🇮🇷',
    "IQ": '🇮🇶',
    "IE": '🇮🇪',
    "IM": '🇮🇲',
    "IL": '🇮🇱',
    "IT": '🇮🇹',
    "CI": '🇨🇮',
    "JM": '🇯🇲',
    "JP": '🇯🇵',
    "JE": '🇯🇪',
    "JO": '🇯🇴',
    "KZ": '🇰🇿',
    "KE": '🇰🇪',
    "KI": '🇰🇮',
    "XK": '🇽🇰',
    "KW": '🇰🇼',
    "KG": '🇰🇬',
    "LA": '🇱🇦',
    "LV": '🇱🇻',
    "LB": '🇱🇧',
    "LS": '🇱🇸',
    "LR": '🇱🇷',
    "LY": '🇱🇾',
    "LI": '🇱🇮',
    "LT": '🇱🇹',
    "LU": '🇱🇺',
    "MO": '🇲🇴',
    "MK": '🇲🇰',
    "MG": '🇲🇬',
    "MW": '🇲🇼',
    "MY": '🇲🇾',
    "MV": '🇲🇻',
    "ML": '🇲🇱',
    "MT": '🇲🇹',
    "MH": '🇲🇭',
    "MQ": '🇲🇶',
    "MR": '🇲🇷',
    "MU": '🇲🇺',
    "YT": '🇾🇹',
    "MX": '🇲🇽',
    "MD": '🇲🇩',
    "MC": '🇲🇨',
    "MN": '🇲🇳',
    "ME": '🇲🇪',
    "MS": '🇲🇸',
    "MA": '🇲🇦',
    "MZ": '🇲🇿',
    "MM": '🇲🇲',
    "NA": '🇳🇦',
    "NR": '🇳🇷',
    "NP": '🇳🇵',
    "NL": '🇳🇱',
    "NC": '🇳🇨',
    "NZ": '🇳🇿',
    "NI": '🇳🇮',
    "NE": '🇳🇪',
    "NG": '🇳🇬',
    "NU": '🇳🇺',
    "NF": '🇳🇫',
    "KP": '🇰🇵',
    "MP": '🇲🇵',
    "NO": '🇳🇴',
    "OM": '🇴🇲',
    "PK": '🇵🇰',
    "PW": '🇵🇼',
    "PS": '🇵🇸',
    "PA": '🇵🇦',
    "PG": '🇵🇬',
    "PY": '🇵🇾',
    "PE": '🇵🇪',
    "PH": '🇵🇭',
    "PN": '🇵🇳',
    "PL": '🇵🇱',
    "PT": '🇵🇹',
    "PR": '🇵🇷',
    "QA": '🇶🇦',
    "RE": '🇷🇪',
    "RO": '🇷🇴',
    "RU": '🇷🇺',
    "RW": '🇷🇼',
    "SH": '🇸🇭',
    "KN": '🇰🇳',
    "LC": '🇱🇨',
    "PM": '🇵🇲',
    "VC": '🇻🇨',
    "WS": '🇼🇸',
    "SM": '🇸🇲',
    "ST": '🇸🇹',
    "SA": '🇸🇦',
    "SN": '🇸🇳',
    "RS": '🇷🇸',
    "SC": '🇸🇨',
    "SL": '🇸🇱',
    "SG": '🇸🇬',
    "SX": '🇸🇽',
    "SK": '🇸🇰',
    "SI": '🇸🇮',
    "SB": '🇸🇧',
    "SO": '🇸🇴',
    "ZA": '🇿🇦',
    "GS": '🇬🇸',
    "KR": '🇰🇷',
    "SS": '🇸🇸',
    "ES": '🇪🇸',
    "LK": '🇱🇰',
    "SD": '🇸🇩',
    "SR": '🇸🇷',
    "SJ": '🇸🇯',
    "SZ": '🇸🇿',
    "SE": '🇸🇪',
    "CH": '🇨🇭',
    "SY": '🇸🇾',
    "TW": '🇹🇼',
    "TJ": '🇹🇯',
    "TZ": '🇹🇿',
    "TH": '🇹🇭',
    "TL": '🇹🇱',
    "TG": '🇹🇬',
    "TK": '🇹🇰',
    "TO": '🇹🇴',
    "TT": '🇹🇹',
    "TN": '🇹🇳',
    "TR": '🇹🇷',
    "TM": '🇹🇲',
    "TC": '🇹🇨',
    "TV": '🇹🇻',
    "UG": '🇺🇬',
    "UA": '🇺🇦',
    "AE": '🇦🇪',
    "GB": '🇬🇧',
    "US": '🇺🇸',
    "UM": '🇺🇲',
    "VI": '🇻🇮',
    "UY": '🇺🇾',
    "UZ": '🇺🇿',
    "VU": '🇻🇺',
    "VA": '🇻🇦',
    "VE": '🇻🇪',
    "VN": '🇻🇳',
    "WF": '🇼🇫',
    "EH": '🇪🇭',
    "YE": '🇾🇪',
    "ZM": '🇿🇲',
    "ZW": '🇿🇼',
}

def update_groups_json():
    # Descargar el archivo JSON desde la URL
    try:
        response = requests.get("https://data.ransomware.live/groups.json")
        response.raise_for_status()  # Asegurarse de que la solicitud fue exitosa
        new_data = response.json()
    except requests.RequestException as e:
        print(f"Error al descargar el JSON: {e}")
        return 

    # Cargar los datos desde dataransom.json
    try:
        with open("dataransom.json", "r", encoding='utf-8') as f:
            sources_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        sources_data = []

    # Crear un diccionario para mapear group_name a una lista de posts
    group_posts = {}
    for item in sources_data:
        group_name = item.get('group_name', '').lower()
        if group_name:
            post = {
                'name': item.get('post_title', ''),
                'discovered': item.get('discovered', ''),
                'country': item.get('country', ''),
                'description': item.get('description', '')
            }
            group_posts.setdefault(group_name, []).append(post)

    # Leer el archivo groups.json si existe, de lo contrario usar una lista vacía
    if os.path.exists('groups.json'):
        with open('groups.json', 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    # Crear un diccionario de grupos existentes para facilitar la actualización
    existing_groups = {entry['name'].lower(): entry for entry in existing_data}

    # Procesar los nuevos datos y actualizar o añadir grupos
    for item in new_data:
        name = item.get('name', '')
        lower_name = name.lower()
        locations = item.get('locations', [])

        # Obtener ubicaciones existentes o inicializar una lista vacía
        existing_locations = existing_groups.get(lower_name, {}).get('locations', [])

        # Crear un conjunto de enlaces existentes para evitar duplicados
        existing_links = {loc['Source Links'] for loc in existing_locations}

        # Filtrar y preparar las nuevas ubicaciones
        new_locations = [
            {'Source Links': loc.get('fqdn', '')}
            for loc in locations
            if loc.get('fqdn', '') and loc.get('fqdn', '') not in existing_links
        ]

        # Combinar ubicaciones existentes con nuevas
        combined_locations = existing_locations + new_locations

        # Obtener posts para este grupo
        posts = group_posts.get(lower_name, [])

        # Si el grupo ya existe, combinar los posts existentes con los nuevos
        existing_posts = existing_groups.get(lower_name, {}).get('posts', [])
        combined_posts = existing_posts + posts

        # Eliminar duplicados en posts basados en 'post_title'
        unique_posts = {post['name']: post for post in combined_posts}.values()

        # Actualizar o crear el grupo en existing_groups
        existing_groups[lower_name] = {
            'name': name,
            'locations': combined_locations,
            'targets': list(unique_posts)
        }

    # Convertir el diccionario de grupos en una lista
    updated_data = list(existing_groups.values())

    # Guardar los datos actualizados en groups.json
    with open('groups.json', 'w', encoding='utf-8') as file:
        json.dump(updated_data, file, indent=4, ensure_ascii=False)
    print("Archivo groups.json actualizado exitosamente.")



def fetch_and_update_data():
    """Fetch new data from the API and update the local file with the latest 200 entries."""
    global data

    try:
        response = requests.get("https://data.ransomware.live/posts.json")
        response.raise_for_status()
        new_data = response.json()

        # Load existing data
        if os.path.exists(data_file):
            with open(data_file, "r") as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        # Crear un diccionario de registros existentes con la clave única como llave
        existing_records = {
            (
                item.get("post_url") or '',
                item.get("post_title") or '',
                item.get("group_name") or ''
            ): item
            for item in existing_data
        }

        # Procesar nuevas entradas
        for item in new_data:
            key = (
                item.get("post_url") or '',
                item.get("post_title") or '',
                item.get("group_name") or ''
            )

            if key in existing_records:
                # Actualizar el registro existente con los nuevos datos
                existing_record = existing_records[key]
                # Actualizar todos los campos del registro existente con los nuevos valores
                for field, value in item.items():
                    existing_record[field] = value
            else:
                # Asignar un nuevo ID y agregar la nueva entrada
                item["id"] = len(existing_data) + 1
                existing_data.append(item)
                existing_records[key] = item  # Agregar al diccionario de registros existentes

        # Guardar los datos actualizados
        with open(data_file, "w") as f:
            json.dump(existing_data, f, indent=4)
        print(f"Data updated. Total entries: {len(existing_data)}.")

        data = existing_data
        
        # Update the latest 200 entries file
        latest_data = sorted(data, key=lambda x: datetime.strptime(x["discovered"], "%Y-%m-%d %H:%M:%S.%f"), reverse=True)[:200]
        with open("latest_200.json", "w") as f:
            json.dump(latest_data, f, indent=4)

    except Exception as e:
        print(f"An error occurred: {e}")


def schedule_data_fetching():
    while True:
        fetch_and_update_data()
        update_groups_json()
        time.sleep(3600)  # Fetch data every hour


def get_country_name(country_code):
    country = pycountry.countries.get(alpha_2=country_code.upper())
    return country.name if country else country_code

@app.route('/')
def index():
    global data
    try:
        with open("latest_200.json", "r") as f:
            data = json.load(f)
            # Convertir las cadenas de fecha a objetos datetime para ordenarlas
            for item in data:
                item["discovered"] = datetime.strptime(item["discovered"], "%Y-%m-%d %H:%M:%S.%f")
            data = sorted(data, key=lambda x: x["discovered"], reverse=True)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # Convertir los códigos de país a emojis de bandera
    for item in data:
        country_code = item.get("country")
        if country_code:
            item["country_flag"] = country_flags.get(country_code, '')  # Usa el diccionario para obtener la bandera
        else:
            item["country_flag"] = ''



    group_filter = request.args.get('group-filter', '')
    country_filter = request.args.get('country-filter', '')
    discovered_order = request.args.get('discovered-order', 'desc')  # por defecto descendente

    # Filtrar los datos
    filtered_data = data
    if group_filter:
        filtered_data = [item for item in filtered_data if item['group_name'] == group_filter]
    if country_filter:
        filtered_data = [item for item in filtered_data if item['country'] == country_filter]

    # Ordenar los datos
    if discovered_order == 'asc':
        filtered_data.sort(key=lambda x: x['discovered'])
    else:
        filtered_data.sort(key=lambda x: x['discovered'], reverse=True)

    # Obtener listas únicas de grupos y países para los dropdowns
    groups = sorted(set(item['group_name'] for item in data))
    countries = sorted(set(item['country'] for item in data))

    return render_template("index.html", data=filtered_data, groups=groups, countries=countries, get_country_name=get_country_name)


@app.route('/all-victims')
def all_victims():
    global data
    try:
        with open("dataransom.json", "r") as f:
            data = json.load(f)
            # Convertir las cadenas de fecha a objetos datetime para ordenarlas
            for item in data:
                item["discovered"] = datetime.strptime(item["discovered"], "%Y-%m-%d %H:%M:%S.%f")
            data = sorted(data, key=lambda x: x["discovered"], reverse=True)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # Convertir los códigos de país a emojis de bandera
    for item in data:
        country_code = item.get("country")
        if country_code:
            item["country_flag"] = country_flags.get(country_code, '')  # Usa el diccionario para obtener la bandera
        else:
            item["country_flag"] = ''


    group_filter = request.args.get('group-filter', '')
    country_filter = request.args.get('country-filter', '')
    discovered_order = request.args.get('discovered-order', 'desc')  # por defecto descendente

    # Filtrar los datos
    filtered_data = data
    if group_filter:
        filtered_data = [item for item in filtered_data if item['group_name'] == group_filter]
    if country_filter:
        filtered_data = [item for item in filtered_data if item['country'] == country_filter]

    # Ordenar los datos
    if discovered_order == 'asc':
        filtered_data.sort(key=lambda x: x['discovered'])
    else:
        filtered_data.sort(key=lambda x: x['discovered'], reverse=True)

    # Paginación
    page = request.args.get('page', 1, type=int)
    per_page = 500  # Número máximo de elementos por página
    total_items = len(filtered_data)
    total_pages = math.ceil(total_items / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    page_data = filtered_data[start:end]

    # Obtener listas únicas de grupos y países para los dropdowns
    groups = sorted(set(item['group_name'] for item in data))
    countries = sorted(set(item['country'] for item in data))

    return render_template("all_victims.html", data=page_data, page=page, total_pages=total_pages, groups=groups, countries=countries, get_country_name=get_country_name, 
        max=max, min=min, range=range)

# Nueva ruta para mostrar la lista de grupos
@app.route('/groups')
def groups():
    try:
        with open("groups.json", "r") as f:
            groups_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        groups_data = []

    # Pasar solo los nombres de los grupos a la plantilla
    return render_template("groups.html", groups=groups_data)


# Nueva ruta para mostrar la lista de grupos
@app.route('/Breaches')
def Breaches():

    return render_template("Breaches.html")

# Nueva ruta para mostrar la lista de grupos
@app.route('/disclaimer')
def Disclaimer():

    return render_template("Disclaimer.html")

# Nueva ruta para mostrar la lista de grupos
@app.route('/leads')
def Leads():

    return render_template("Leads.html")

# Nueva ruta para mostrar la lista de grupos
@app.route('/stealer')
def StealerPaquets():

    return render_template("StealerPaquets.html")

    
# Nueva ruta para mostrar los detalles de un grupo específico
@app.route('/groups/<group_name>')
def group_detail(group_name):
    try:
        with open("groups.json", "r") as f:
            groups_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        groups_data = []

    # Encontrar el grupo con el nombre dado
    group = next((g for g in groups_data if g["name"].lower() == group_name.lower()), None)

    if not group:
        return "Group not found", 404

        # Convertir los códigos de país a emojis de bandera
    for item in group.get("targets", []):
        
        item['discovered'] = datetime.strptime(item['discovered'], '%Y-%m-%d %H:%M:%S.%f')   

        country_code = item["country"]
        if country_code:
            item["country_flag"] = country_flags.get(country_code, '')  # Usa el diccionario para obtener la bandera
        else:
            item["country_flag"] = ''

    
    country_filter = request.args.get('country-filter', '')
    discovered_order = request.args.get('discovered-order', 'desc')  # por defecto descendente

    # Filtrar los datos
    filtered_data = group.get("targets", [])
    if country_filter:
        filtered_data = [item for item in filtered_data if item['country'] == country_filter]

    # Ordenar los datos
    if discovered_order == 'asc':
        filtered_data.sort(key=lambda x: x['discovered'])
    else:
        filtered_data.sort(key=lambda x: x['discovered'], reverse=True)

    countries = sorted(set(item['country'] for item in group.get("targets", [])))

    # Pasar el grupo encontrado a la plantilla
    return render_template("group_detail.html", group=group, data=filtered_data, get_country_name=get_country_name, countries=countries)

@app.route('/your_view_function')
def your_view_function():
    group_filter = request.args.get('group-filter', '')
    country_filter = request.args.get('country-filter', '')
    discovered_order = request.args.get('discovered-order', 'desc')  # por defecto descendente

    # Filtrar los datos
    filtered_data = data
    if group_filter:
        filtered_data = [item for item in filtered_data if item['group_name'] == group_filter]
    if country_filter:
        filtered_data = [item for item in filtered_data if item['country'] == country_filter]

    # Ordenar los datos
    if discovered_order == 'asc':
        filtered_data.sort(key=lambda x: x['discovered'])
    else:
        filtered_data.sort(key=lambda x: x['discovered'], reverse=True)

    # Obtener listas únicas de grupos y países para los dropdowns
    groups = sorted(set(item['group_name'] for item in data))
    countries = sorted(set(item['country'] for item in data))

    return render_template('your_template.html', data=filtered_data, groups=groups, countries=countries)



if __name__ == '__main__':
    # Start the data fetching in a separate thread
    threading.Thread(target=schedule_data_fetching, daemon=True).start()
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)

