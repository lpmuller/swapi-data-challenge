import matplotlib.pyplot as plt
from db_operations import query_db

def get_top_10_characters_by_movie_count():
    sql_query = """
    SELECT name, COUNT(*) as num_films 
    FROM characters 
    CROSS JOIN json_each(characters.films) 
    GROUP BY name 
    ORDER BY num_films DESC, name
    LIMIT 10;
    """
    return query_db(sql_query)

def get_top_10_fastest_starships_by_atmosphering_speed():
    sql_query_starships = """
    SELECT name, MAX(CAST(max_atmosphering_speed as INT)) as max_speed
    FROM starships
    WHERE max_atmosphering_speed != 'n/a'
    GROUP BY name
    ORDER BY max_speed DESC
    LIMIT 10;
    """
    return query_db(sql_query_starships)

def get_top_10_fastest_starships_by_MGLT():
    sql_query = """
    SELECT name, MAX(CAST(MGLT as INT)) as max_MGLT 
    FROM starships 
    WHERE MGLT != 'unknown' AND MGLT != 'n/a'
    GROUP BY name 
    ORDER BY max_MGLT DESC 
    LIMIT 10;
    """
    return query_db(sql_query)

def calculate_planet_score(climate, surface_water, terrain, orbital_period):
    # Pontuação do Clima (Climate Score - CS)
    if any(x in climate.lower() for x in ['arid', 'hot', 'heated']):
        CS = 1
    elif any(x in climate.lower() for x in ['temperate', 'tropical']):
        CS = 0.5
    elif any(x in climate.lower() for x in ['frozen', 'frigid']):
        CS = 0
    else:
        CS = 0.25

    # Pontuação da Água Superficial (Surface Water Score - SWS)    
    try:
        surface_water = float(surface_water)
        SWS = (100 - surface_water)/100
    except ValueError:
        SWS = 0  # Tratamento de valores não numéricos ou desconhecidos

    # Pontuação do Terreno (Terrain Score - TS)
    if any(x in terrain.lower() for x in ['desert', 'volcanoes', 'lava']):
        TS = 1
    elif any(x in terrain.lower() for x in ['barren', 'rocky']):
        TS = 0.7
    elif any(x in terrain.lower() for x in ['forrests', 'jungles']):
        TS = 0.3
    elif any(x in terrain.lower() for x in ['ice', 'snow']):
        TS = 0
    else:
        TS = 0.5

    # Pontuação do Período Orbital (Orbital Period Score - OPS)
    try:
        orbital_period = float(orbital_period)
        if orbital_period <= 360:
            OPS = 1
        elif orbital_period <= 500:
            OPS = 0.5
        elif orbital_period <= 1000:
            OPS = 0.25
        else:
            OPS = 0.1
    except ValueError:
        OPS = 0  # Tratamento de valores não numéricos ou desconhecidos

    # Pontuação Total (Total Score - TS)
    total_score = CS + SWS + TS + OPS
    return total_score


def get_top_10_hottest_planets():
    sql_query = """
    SELECT name, climate, surface_water, terrain, orbital_period
    FROM planets;
    """
    planets = query_db(sql_query)
    
    # Calculando as pontuações para cada planeta
    planets['score'] = planets.apply(lambda x: calculate_planet_score(x['climate'], x['surface_water'], x['terrain'], x['orbital_period']), axis=1)

    # Ordenando os planetas pela pontuação e pegando os top 10
    top_10_hottest_planets = planets.sort_values(by='score', ascending=False).head(10)
    return top_10_hottest_planets

def plot_horizontal_bar_graph(df, x_column, y_column, title, xlabel, ylabel):
    plt.figure(figsize=(10, 8))    
    plt.barh(df[y_column][::-1], df[x_column][::-1])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()