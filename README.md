# SI_507_project

Instructions to Run the code:
1) Create a file named secret.py
2) Create API keys for the following APIs:
    i)   OMDb API - https://www.omdbapi.com/apikey.aspx
    ii)  TMDb API - https://www.themoviedb.org/documentation/api
    iii) Youtube API - https://developers.google.com/youtube/v3/getting-started
3) Add the keys to the secret.py as follows:
   '''
   TMDb_api_key = '<API key>'
   OMDb_api_key = '<API key>'
   Youtube_api_key = '<API key>'
   '''
 4) Once thats done, Open the terminal and run the file main.py. Launch the url - http://127.0.0.1:5000 in the browser to view the website.
    
 Brief description of the project:
 
The website would have two web pages. The home page would have three sections – top Rated, Popular, and Trending. Under each section, a list of movies along with their title, poster, and rating would be displayed. 
The user would be able to click on the title of any movie and he would be redirected to the second webpage that would provide more details about the movie. The home page would also have a Nav bar where the user can simply type the movie he wishes to know more about. He would then be redirected to the second webpage which would display the movie details.
The second webpage would automatically play the trailer of the movie that  was searched for. The user would be able to interact with the video player to fast-forward the trailer or to skip to certain portions of the trailer. The second page would provide the plot of the movie, information regarding the cast, director, genre, and rating. This webpage would also list the reviews for the movie and the OTT platforms where one can stream the movie and would also provide a list of similar movies and recommend the user a few movies based on this search. Clicking on the title of the webpage(’ MovieBuff ’) in the Navbar from the second webpage will redirect you to the home page.
 
How data is organized into data structure:
I created a Node Class and a Tree Class. The Tree class has methods to traverse the tree, to find a specific 
node and to convert the tree to JSON. Below is the code snippet for the same

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
            
 Using these classes and the functions - 'generate_top_related_tree', 'generate_movie_tree'. The data in the JSON format is converted to a tree.
 
 Python packages used:
 1) flask
 2) requests
 3) pickle
 
 In built python packages used:
 1) os
 2) json
 3) datetime
    
