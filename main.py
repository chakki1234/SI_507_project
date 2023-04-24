from flask import Flask
from flask import render_template
import requests
import secret
import pickle
import os
import datetime
import json

app = Flask(__name__)
app.debug = True

now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day

# Classes and Helper functions ---------------------------------------------
class Node:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, child):
        self.children.append(child)

class Tree:
    def __init__(self):
        self.root = None
        self.json_dict = {}

    def add_root(self, root_node):
        self.root = root_node

    def traverse_tree(self, node):
        print(node.data)
        for child in node.children:
            self.traverse_tree(child)

    def find(self, node, to_find):
        if node.data == to_find:
            return node.children
        else:
            for child in node.children:
                result = self.find(child, to_find)
                if result:
                    return result
        return None
                
    def to_dict(self, node):
        for child in node.children:
            if child.data != 'OTT':
                self.json_dict[f'{child.data}'] = [] 
                for child_of_child in child.children:
                    self.json_dict[f'{child.data}'].append(child_of_child.data)
            else:
                self.json_dict[f'{child.data}'] = {}
                for child_of_child in child.children:
                    self.json_dict[f'{child.data}'][f'{child_of_child.data}'] = []
                    for child_child_child in child_of_child.children:
                        self.json_dict[f'{child.data}'][f'{child_of_child.data}'].append(child_child_child.data)
        with open("data.json", "w") as file:
            json.dump(self.json_dict, file, indent=4)

def generate_top_related_tree(title, movie_list_raw_data):
    # creating nodes and tree
    Root_node = Node(title)
    for movie in movie_list_raw_data:
        if 'title' in movie:
            name = movie['title']
        else:
            name = movie['name']
        Root_node.add_child(Node([ name, movie['poster_path'], movie['vote_average'] ]))
    
    # creating a tree
    temp_tree = Tree()
    temp_tree.add_root(Root_node)
    return temp_tree

def generate_movie_tree(OMDb_data, youtube_data, reviews_raw_data, watch_provider_raw_data, similar_movie_raw_data, movie_recommendation_raw_data):
    #preprocessing the data
    flatrate_data, buy_data, rent_data = [], [], []
    for val in watch_provider_raw_data['results'].values():
        if 'flatrate' in val:
            for temp1 in val['flatrate']:
                flatrate_data.append(temp1['provider_name'])

        if 'buy' in val:
            for temp2 in val['buy']:
                buy_data.append(temp2['provider_name'])

        if 'rent' in val:
            for temp3 in val['rent']:
                rent_data.append(temp3['provider_name'])


    reviews_data = [[movie_result['author'], movie_result['content']] for movie_result in reviews_raw_data['results']]

    similar_movie_data = []
    for movie in similar_movie_raw_data:
        if 'title' in movie:
            name = movie['title']
        else:
            name = movie['name']
        similar_movie_data.append([ name, movie['poster_path'], movie['vote_average'] ])
    
    recommended_movie_data = []
    for movie in movie_recommendation_raw_data:
        if 'title' in movie:
            name = movie['title']
        else:
            name = movie['name']
        recommended_movie_data.append([ name, movie['poster_path'], movie['vote_average'] ])


    #Creating the nodes
    Root_node = Node('Movie')

    Title_node = Node('Title')
    Title_node.add_child(Node(OMDb_data['Title']))

    Genre_node = Node('Genre')
    Genre_node.add_child(Node(OMDb_data['Genre']))

    Poster_node = Node('Poster')
    Poster_node.add_child(Node(OMDb_data['Poster']))

    Director_Actor_node = Node('Director_Actor')
    Director_Actor_node.add_child(Node([OMDb_data['Director'], OMDb_data['Actors']]))

    Rating_node = Node('Rating')
    Rating_node.add_child(Node(OMDb_data['imdbRating']))

    year_lang_plot_node = Node('year_lang_plot_node')
    year_lang_plot_node.add_child(Node([OMDb_data['Year'], OMDb_data['Language'], OMDb_data['Plot']]))

    youtube_node = Node('youtube')
    youtube_node.add_child(Node(youtube_data['items'][0]['id']['videoId']))

    Reviews_node = Node('Reviews')
    if len(reviews_data) != 0:
        for review in reviews_data:
            Reviews_node.add_child(Node(review))
    else:
        Reviews_node.add_child(Node('No'))

    Similar_movie_node = Node('Similar_movies')
    if len(similar_movie_data) != 0:
        for movie in similar_movie_data:
            Similar_movie_node.add_child(Node(movie))
    else:
        Similar_movie_node.add_child(Node('No'))

    Recommended_movie_node = Node('Recommended_movies')
    if len(recommended_movie_data) != 0: 
        for movie in recommended_movie_data:
            Recommended_movie_node.add_child(Node(movie))
    else:
        Recommended_movie_node.add_child(Node('No'))

    OTT_node = Node('OTT')
    Flatrate_node = Node('Flatrate')
    Buy_node = Node('Buy')
    Rent_node = Node('Rent')
    OTT_node.add_child(Flatrate_node)
    OTT_node.add_child(Buy_node)
    OTT_node.add_child(Rent_node)
    
    if len(list(set(flatrate_data))) != 0:
        for OTT_platform in list(set(flatrate_data)):
            Flatrate_node.add_child(Node(OTT_platform))
    else:
        Flatrate_node.add_child(Node('No'))

    if len(list(set(buy_data))) != 0:
        for OTT_platform in list(set(buy_data)):
            Buy_node.add_child(Node(OTT_platform))
    else:
        Buy_node.add_child(Node('No'))

    if len(list(set(rent_data))):
        for OTT_platform in list(set(rent_data)):
            Rent_node.add_child(Node(OTT_platform))   
    else:
         Rent_node.add_child(Node('No'))

    # Connecting the nodes
    Root_node.add_child(Title_node)
    Root_node.add_child(youtube_node)
    Root_node.add_child(Genre_node)
    Root_node.add_child(Poster_node)
    Root_node.add_child(Director_Actor_node)
    Root_node.add_child(Rating_node)
    Root_node.add_child(year_lang_plot_node)
    Root_node.add_child(Reviews_node)
    Root_node.add_child(Similar_movie_node)
    Root_node.add_child(Recommended_movie_node)
    Root_node.add_child(OTT_node)

    #creating the tree
    movie_tree = Tree()
    movie_tree.add_root(Root_node)

    return movie_tree


# HTML pages ----------------------------------------------------------------
@app.route("/")
def index():
    return render_template('home.html')

@app.route("/<movie_name>")
def movie(movie_name):
    return render_template('movie.html', name=movie_name)

@app.route("/theatre")
def theatre():
    return render_template('theatre.html')
# APIS -------------------------------------------------------------------------

@app.route("/top_rated_api_request")
def rated():
    if os.path.exists(f'./main_pg_results/top_rated{day}-{month}-{year}.pickle'):
        with open(f'./main_pg_results/top_rated{day}-{month}-{year}.pickle', 'rb') as f:
            movie_tree = pickle.load(f)
    else:
        response = requests.get(f"https://api.themoviedb.org/3/movie/top_rated?api_key={secret.TMDb_api_key}&language=en-US&page=1")
        data = response.json()
        movie_tree = generate_top_related_tree('top_rated', data['results'])

        with open(f'./main_pg_results/top_rated{day}-{month}-{year}.pickle', 'wb') as f:
            pickle.dump(movie_tree, f)
    
    return [movie_child_node.data for movie_child_node in movie_tree.find(movie_tree.root, 'top_rated')]


@app.route("/top_popular_api_request")
def popular():
    if os.path.exists(f'./main_pg_results/top_popular{day}-{month}-{year}.pickle'):
        with open(f'./main_pg_results/top_popular{day}-{month}-{year}.pickle', 'rb') as f:
            movie_tree = pickle.load(f)
    else:
        response = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={secret.TMDb_api_key}&language=en-US&page=1")
        data = response.json()
        movie_tree = generate_top_related_tree('top_popular', data['results'])

        with open(f'./main_pg_results/top_popular{day}-{month}-{year}.pickle', 'wb') as f:
            pickle.dump(movie_tree, f)

    return [movie_child_node.data for movie_child_node in movie_tree.find(movie_tree.root, 'top_popular')]

@app.route("/top_trending_api_request")
def trending():
    if os.path.exists(f'./main_pg_results/top_trending{day}-{month}-{year}.pickle'):
        with open(f'./main_pg_results/top_trending{day}-{month}-{year}.pickle', 'rb') as f:
            movie_tree = pickle.load(f)
    else:
        response = requests.get(f"https://api.themoviedb.org/3/trending/all/day?api_key={secret.TMDb_api_key}")
        data = response.json()
        movie_tree = generate_top_related_tree('top_trending', data['results'])

        with open(f'./main_pg_results/top_trending{day}-{month}-{year}.pickle', 'wb') as f:
            pickle.dump(movie_tree, f)
    
    return [movie_child_node.data for movie_child_node in movie_tree.find(movie_tree.root, 'top_trending')]


@app.route("/movie_specific/<mname>")
def movie_page(mname):

    filename = f'{mname}.pickle'
    if os.path.exists(f'./searches/{filename}'):
        with open(f'./searches/{filename}', 'rb') as f:
            movie_tree = pickle.load(f)
    else:
        # omdb data
        OMDb_data = requests.get(f"http://www.omdbapi.com/?t={mname}&plot=full&apikey={secret.OMDb_api_key}").json()

        #youtube data
        youtube_data = requests.get(f"https://www.googleapis.com/youtube/v3/search?key={secret.Youtube_api_key}&q={mname}%20movie%20trailer&type=video").json()

        #to get TMDb movie ID
        try:
            if 'imdbID' in OMDb_data:
                TMDb_id = requests.get(f"https://api.themoviedb.org/3/find/{OMDb_data['imdbID']}?api_key={secret.TMDb_api_key}&language=en-US&external_source=imdb_id").json()['movie_results'][0]['id']
            else: 
                return 'No'
        except:
            return 'Some error with the API. Looks like the API removed the details of this movie.'

        # reviews
        review_raw_data = requests.get(f"https://api.themoviedb.org/3/movie/{TMDb_id}/reviews?api_key={secret.TMDb_api_key}&language=en-US&page=1").json()
        
        # watch providers
        watch_provider_raw_data = requests.get(f"https://api.themoviedb.org/3/movie/{TMDb_id}/watch/providers?api_key={secret.TMDb_api_key}").json()

        # similar movies
        similar_movie_raw_data = requests.get(f"https://api.themoviedb.org/3/movie/{TMDb_id}/similar?api_key={secret.TMDb_api_key}").json()['results']

        # movie reommendations
        movie_recommendation_raw_data = requests.get(f"https://api.themoviedb.org/3/movie/{TMDb_id}/recommendations?api_key={secret.TMDb_api_key}").json()['results']
        
        movie_tree = generate_movie_tree(OMDb_data, youtube_data, review_raw_data, watch_provider_raw_data, similar_movie_raw_data, movie_recommendation_raw_data)

        ## To generate the sample json data file
        # movie_tree.to_dict(movie_tree.root)

        with open(f'./searches/{mname}.pickle', 'wb') as f:
            pickle.dump(movie_tree, f)

    return_dict = {
        'Title': movie_tree.find(movie_tree.root, 'Title')[0].data,
        'year_lang_plot_node': movie_tree.find(movie_tree.root, 'year_lang_plot_node')[0].data,
        'Genre': movie_tree.find(movie_tree.root, 'Genre')[0].data,
        'Director_Actor': movie_tree.find(movie_tree.root, 'Director_Actor')[0].data,
        'Rating': movie_tree.find(movie_tree.root, 'Rating')[0].data,
        'Poster': movie_tree.find(movie_tree.root, 'Poster')[0].data,
        'youtube': movie_tree.find(movie_tree.root, 'youtube')[0].data,
    }

    # Checking (error handling)
    if movie_tree.find(movie_tree.root, 'Reviews')[0].data == 'No':
        return_dict['Reviews'] = []
    else:
        return_dict['Reviews'] = [review_node.data for review_node in movie_tree.find(movie_tree.root, 'Reviews')]

    if movie_tree.find(movie_tree.root, 'Similar_movies')[0].data == 'No':
        return_dict['Similar_movies'] = []
    else:
        return_dict['Similar_movies'] = [movie_node.data for movie_node in movie_tree.find(movie_tree.root, 'Similar_movies')]

    if movie_tree.find(movie_tree.root, 'Recommended_movies')[0].data == 'No':
        return_dict['Recommended_movies'] = []
    else:
        return_dict['Recommended_movies'] = [ movie_node.data for movie_node in movie_tree.find(movie_tree.root, 'Recommended_movies')]
    
    if movie_tree.find(movie_tree.root, 'Flatrate')[0].data == 'No':
        return_dict['Flatrate'] = []
    else:
        return_dict['Flatrate'] = [ott_platform_node.data for ott_platform_node in movie_tree.find(movie_tree.root, 'Flatrate')]
    
    if movie_tree.find(movie_tree.root, 'Buy')[0].data == 'No':
        return_dict['Buy'] = []
    else:
        return_dict['Buy'] = [ott_platform_node.data for ott_platform_node in movie_tree.find(movie_tree.root, 'Buy')]

    if movie_tree.find(movie_tree.root, 'Rent')[0].data == 'No':
        return_dict['Rent'] = []
    else:
        return_dict['Rent'] = [ott_platform_node.data for ott_platform_node in movie_tree.find(movie_tree.root, 'Rent')]

    return  return_dict

     

# ----------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run()