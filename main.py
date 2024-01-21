from swapi_requests import load_swapi_data
from db_operations import save_to_db
from data_analysis import get_top_10_characters_by_movie_count,get_top_10_fastest_starships_by_atmosphering_speed,get_top_10_fastest_starships_by_MGLT, get_top_10_hottest_planets, plot_horizontal_bar_graph

def main():
    # Carregar e salvar dados
    characters_df = load_swapi_data('people')
    save_to_db(characters_df, 'characters')

    starships_df = load_swapi_data('starships')
    save_to_db(starships_df, 'starships')

    planets_df = load_swapi_data('planets')
    save_to_db(planets_df, 'planets')

    # Análises 
    # Personagens que aparecem em mais filmes
    top_10_characters = get_top_10_characters_by_movie_count()
    print("Personagens que apareceram em mais filmes:", top_10_characters)
    plot_horizontal_bar_graph(top_10_characters, 'num_films', 'name', 'Top 10 Personagens de Star Wars por Quantidade de Filmes', 'Número de Filmes', 'Personagem')   
    
    # Nave mais rápida
    # Considerando MGLT
    top_10_starships_by_MGLT = get_top_10_fastest_starships_by_MGLT()
    print("Naves mais rápidas de acordo com MGLT:",top_10_starships_by_MGLT)
    plot_horizontal_bar_graph(top_10_starships_by_MGLT, 'max_MGLT', 'name', 'Nave Mais Rápida de Star Wars por MGLT', 'MGLT', 'Nave Espacial')
    # Considerando velocidade atmosférica
    top_10_starships_by_atmosphering_speed = get_top_10_fastest_starships_by_atmosphering_speed()
    print("Naves mais rápidas de acordo com velocidade atmosférica:",top_10_starships_by_atmosphering_speed)
    plot_horizontal_bar_graph(top_10_starships_by_atmosphering_speed, 'max_speed', 'name', 'Nave Mais Rápida de Star Wars por Velocidade Atmosférica', 'Máxima velocidade atmosférica', 'Nave Espacial')
    
    
    #Planeta mais quente
    top_10_hottest_planets = get_top_10_hottest_planets()
    print("Planetas mais quentes:", top_10_hottest_planets)
    plot_horizontal_bar_graph(top_10_hottest_planets,'score','name','Planeta Mais Quente de Star Wars por Score','Score','Planeta')


if __name__ == "__main__":
    main()