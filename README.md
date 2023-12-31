# Sportle
#### Video Demo:  <URL https://youtu.be/70CCrFRV8Kg>
#### Description:
Sportle is a web game based off "Wordle" the viral game from a few years back. Instead of guessing a word Sportle has you guessing a random sports team.

To play this game users must register; if they attempt to play the game without registering or login in then they will just be redirected to the log in page.

Once they register the main page will change to only show the play button.

note: the main page does not have the navbar to replicate how "Wordle" has its main page, this is not a mistake.

How to play:
You have 6 guesses. The user will select the team's name from a dropdown select menu that will have all teams present in the database, this was done like this so the user does not input a team that does not exist or if it is misspelled. Each guess will check if the team guessed lands under one of the following 5 categories: Sport, which is the kind of sport played by the team, Region, which would be from which continent the team resides, Country, which is the country the team resides, League, which is the league the team plays in primarily (for example: the Miami Dolphins are NFL, the Miami Heat are NBA and Real Madrid would be La Liga), and then finally the actual team. Each category has boxes under it which will turn green if correct or red if incorrect.

If a user guesses the correct sports team the python script will update all statuses for the player which are Games Played, Games won, Win percentage, Current Streak, and Max Streak. All of these will be incremented by one execpt win percentage which will just calculate the percentage based off the games played and the games won and the max streak will check if the current streak is greater than the previous max streak, if it is then the max streak will be updated to the current streak's amount.

If a user misses all guesses then the game is over and the users stats will also be updated. Games played will be incremented by 1, games won will stay the same, win percentage will be updated, the Current streak will be set back to 0 and the max streak will stay as is.

The databse has two tables: the User table and the Teams table. The user table will be updated as stated above depending on a games result or if a new user is created. When a user is created the password will be hashed and then all other columns: Games played ("played"), games won ("wins"), win Percentage ("winPerc"), current Streak ("currStreak"), and max streak ("maxStreak") will be set to 0 as that is their default and this will let the values be updated.
The teams table holds all the information for the sports teams: The name ("teamName"), the region ("continent"), the country ("country"), the league ("league"), and the sport played ("sport"). This information cannot be updated throught the website and will remain the same.

note for the teams: Not all teams are present in the database. The teams present are those present in the following leagues: LaLiga, Premier League, MLS, NHL, NFL, and NBA.
