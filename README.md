# Vital Title Hub

Vital Title Hub is designed and implemented as my final project for Harvard's [CS50 Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2020/) course. Vital Title Hub is a web application written primarily in Python and JavaScript using the Django framework.

<img width="1294" alt="vital_title_hub" src="https://github.com/user-attachments/assets/2c7eebb5-d166-4c73-9827-410ba7a5f1f6">

[![Image of Title Vital Hub](image.png)](https://youtube.com)

### What is Vital Title Hub?

Using the The Open Movie Database - [OMDb API](https://www.omdbapi.com/), Title Vital Hub a social network providing a space for movie lovers to create lists of favorite movies, like and follow other movie lovers and comment on movies in user lists.

Title Vital Hub allows users to search and view movie and TV show titles; save favorite titles to user lists; comment on bookmarked movies; like user comments and follow other users. Title Vital Hub also provices basic user-handling, allowing visitors to create an account for applicaton as well as log in and out.

Watch a video walkthrough of Title Vital Hub [HERE](https://www.youtube.com/@george-trapp)

### Quickstart

```
# Create new migrations
python3 manage.py makemigration

# Migrate
python3 manage.py migrate

# Start development server 
python3 manage.py runserver

# In browser, navigate to generated URL (typically local host http://127.0.0.1:8000/)
```
To navigate Title Vital Hub, use the app's NavBar. All pages (except the app's index page) requires the user to have an account with the application and be signed in (go to **Register** / **Log In)**. Title Vital Hub's default **Index** page displays a splash screen movie graphic image; The **Search Field** allows users to search titles, view title details, bookmark titles, comment on titles and like comments other users have posted. **Top Rated** displays user's bookmarked lists as well as links to other user lists.  **Profile** displays logged in user's movie list as well as the number of followers users they are following.

## Backend

### File Structure

Title Vital Hub follows a typical [Django file structure](https://django-project-skeleton.readthedocs.io/en/latest/structure.html). Python code corresponding to each of the app's 'views' (both visible and API) is stored in the file `views.py`. The site's various URL patterns can be found in `urls.py`.  The app's in-built database is built on four tables (User, Movie, Follow and Comment) defined in the file `models.py`, with the database saved as `db.sqlite3`.

The website consists of eight HTML pages, most of which extend from a layout file (`layout.html`) using Django's templating language. These files are stored in the `templates` directory. `index.html` (the app's default route), displays a graphic splash page; `search.html` allows users to search titles by a keyword; `details.html` displays full details on a specific title as well as the ability to bookmark a title, comment on a title and like user comments; `profile.html` displays a user's bookmarked list of titles; `top-rated.html` displays top rated titles from Title Vital Hub user lists which are filtered by the highest IMDB Ratings.  

The `static` folder contains two sub-folders: `media`, which stores the app's images, and `js` which stores the app's JavaScript code. Most of the JavaScript files correspond to a single webpage. Title Vital Hub's custom CSS is stored in `style.css`. 

Outside of these core files, the app's dependencies can be found in `requirements.txt` and environment variables in `.env`.

### How Title Vital Hub Works

Title Vital Hub is a web application written in Python, JavaScript, HTML, and CSS. The application contains a SQLite database, with data managed through Python objects ('models'). Title Vital Hub utilizes the Django full-stack framework and Bootstrap front-end framework.

Title Vital Hub makes use of The Open Movie Database - [OMDb API](https://www.omdbapi.com/), for title searches and full details of movie and TV show titles.  The application has 8 'visible' URL routes (i.e. routes which render an HTML page) and 8 'API' routes. Querying Title Vital Hub's APIs and / or updating the app's underlying database, these routes: 
 1. Shows results of movies related to a searched keyword
 2. Checks
 3. Bookmark / unbookmark a question
 4. Add / remove a question from a user's list
 5. Checks followers/following users's on Title Vital Hub
 6. Checks how many Likes are given to a comment on a title

While Python does most of Title Vital Hub's heavy lifting (rendering HTML pages, updating the app's database, processing data, etc.), JavaScript is used to retrieve data (typically in the form of asynchronous `fetch` functions, passing over to backend API functions (described above) for processing) and update HTML pages as required.

## Et al.

### Distinctiveness and Complexity

Built from scratch (i.e. an empty Django template, *not* the programming language!) Title Vital Hub utilizes many of the tools and techniques covered in CS50W. By providing bookmarking and notification functionality by combining a public API and inbuilt database, Title Vital Hub goes beyond a simple API querier, significantly building on Title Vital Hub's own website. 

Created to address challenges in my professional role in Title Vital Hub, and incorporating a number of techniques **not** covered in CS50W, Title Vital Hub is distinct from, and significantly larger and more complex than the course's previous PSETs.

In respect to CS50W's other grading requirements, Title Vital Hub is mobile responsive, utilizes Django (with four associated models), and JavaScript as described above.

### Acknowledgements

- OMDb API - [LINK](https://www.omdbapi.com//)
- CS50’s Web Programming with Python and JavaScript - [LINK](https://cs50.harvard.edu/web/2020/)


### About Me

Hi, I'm George Trapp! I'm a passionate and creative Full Stack Developer with extensive experience in web and software development. I've had the opportunity to work across industries—from health and finance to education. Outside of coding, I have a deep background in music as a cellist, holding a Bachelor of Music from The Juilliard School. 

Let's connect!
 - LinkedIn - [LINK](https://www.linkedin.com/in/georgetrapp/)
 - GitHub - [LINK](https://github.com/gtrapp/)

<hr>
