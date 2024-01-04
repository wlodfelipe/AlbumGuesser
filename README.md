# Album Guesser
#### Video Demo:  https://youtu.be/ORaESmBqHIs
**CS50 Final Project**

## Overview

Album Guesser is a web application developed as a non-profit academic project. The objective of the game is to guess the name, artist's name and release year of a given album based on its cover image. Users earn points for correct guesses, and the game continues with the appearance of a new randomly selected album.

## How to Play

1. Read the game rules on the home page.
2. Choose a difficulty level (Easy, Hard, or Unlimited).
3. Guess the name of the album based on the presented cover image.
4. Earn points for each correct guess.
5. View your final score after completing the game.

## Built with

- Python
- Flask
- Jinja2
- SQLite3
- JavaScript
- HTML
- CSS

## Difficulty Levels

### Easy Mode
- 60 seconds to accumulate points.
- Randomly selected from a pool of 100 albums.

### Hard Mode
- 60 seconds to accumulate points.
- Randomly selected from a pool of 5000 albums.

### Unlimited Mode
- No time limit.
- Accumulate points indefinitely.
- Randomly selected from a pool of 5000 albums.
- Receive information about the the previous album.

## File Structure

- **app.py:** Contains Flask routes and logic for the game.
- **helpers.py:** Defines functions used in app.py for album retrieval and other tasks.
- **csvtodb.py:** Converts a CSV file into a SQLite database (used once for initial data setup).

## Routes

- **/ (Root):** Home page with general information about the application.
- **/AlbumGuesser:** Main game route with easy and hard modes.
- **/check_session:** API endpoint to check the status of the user's session.
- **/results/:score:** Display the user's final score after completing a game.
- **/unlimited:** Unlimited mode route for a more relaxed experience.

## Contact
- [LinkedIn](https://www.linkedin.com/in/felipe-luiz-wlodkowski-953255273/)

## Acknowledgments

- Powered by Last.fm API.
- Footer contains a link to the original Last.fm site.
