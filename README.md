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
 
I plan to create a Flask framework app. The website would have two web pages. The home page would have three sections – top Rated, Popular, and Trending. Under each section, a list of movies along with their title, poster, and rating would be displayed. 
The user would be able to click on the title of any movie and he would be redirected to the second webpage that would provide more details about the movie. The home page would also have a Nav bar where the user can simply type the movie he wishes to know more about. He would then be redirected to the second webpage which would display the movie details.
The second webpage would automatically play the trailer of the movie that  was searched for. The user would be able to interact with the video player to fast-forward the trailer or to skip to certain portions of the trailer. The second page would provide the plot of the movie, information regarding the cast, director, genre, and rating. This webpage would also list the reviews for the movie and the OTT platforms where one can stream the movie and would also provide a list of similar movies and recommend the user a few movies based on this search. Clicking on the title of the webpage(’ MovieBuff ’) in the Navbar from the second webpage will redirect you to the home page.
 
 Python packages used:
 1) flask
 2) requests
 3) pickle
 
 In built python packages used:
 1) os
 2) json
 3) datetime
    
