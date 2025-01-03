brewblog
-----

## Introduction

brewblog is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

## Overview

This app has been modified from the original Udacity codebase to meet a more modern standard for development, deployment, dependency management, and project structure.

### Improvements

1. **Docker**

    The project no longer uses python virtual environments on the host machine, but is instead deployed via Docker containers. There are four main parts to the project deployment structure:

    1. db: The Postgres image with a persistent database volume,
    2. app: The brewblog app itself, running python in a container,
    3. search: An elasticsearch server, also with a persistent index volume, and
    4. admin: An adminer instance giving admin access to the postgres database.

    All of this is orchestrated using `docker-compose`.

2. **Poetry**

    Dependencies are installed and managed using `poetry` instead of a `requirements.txt` file.  This may be overkill for such a small project, but reflects a more modern approach to python development.

3. **Database**

    States and Genres are pre-seeded into the database on startup, and used to pre-fill select forms.

    City / State pairs are stored as a relationship in the database, and checked for uniqueness.  When a user adds a city / state pair to an artist or to a venue, the City model is checked for an existing pair, and assigns that `id` to the artist or venue.  If it doesn't find a existing `id`, a new entry is created in the database.  This helps prevent duplicate entries, and makes sorting venues by city and state easier.

    Artists and Venues are paired with genres via a many-to-many relationship, making use of placeholder tables and relationships.  This would make adding genre filtering to a future version of the project trivial.

4. **Blueprints**

    Sections of the project are broken up into Blueprints based on the type of data they deal with.  Artists, errors, shows, and venues have their own directories, with their own routes and forms.

5. **Modern Flask, SQLAlchemy**

    Much of the structure and functional improvement of this app is inspired by the 2024 Edition of the [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world), by Miguel Grinberg.

## Development Setup

1. **Download the project starter code locally**

    ```
    git clone https://github.com/mattgaskey/brewblog
    ```

2. **Install Docker and Docker-Compose if you haven't already**

    [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

3. **From the project directory, run:**

    ```
    docker-compose up --build -d
    ```

4. **Verify on the Browser**

    Navigate to project homepage: [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000)

    Log in to Adminer: [http://127.0.0.1:8080](http://127.0.0.1:8080) or [http://localhost:8080](http://localhost:8080), and log in with credentials:

    ```
    System: PostgreSQL
    Server: db
    Username: postgres
    Password: postgres
    Database: db
    ```

    Verify the Elasticsearch server is running: [http://127.0.0.1:9200](http://127.0.0.1:9200) or [http://localhost:9200](http://localhost:9200)

5. **To stop the project:**

    ```
    docker-compose down
    ```

    Or to stop the project, and delete the persistent data:
    
    ```
    docker-compose down -v
    ```
