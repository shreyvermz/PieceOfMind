# Piece Of Mind (in progress!)
### An interactive menu that pulls information about One Piece arcs and individual episodes from public databases.

## Description
Few shows consistently display brilliance and constant improvement as notably as the anime written by Eichiro Oda: **One Piece**. The anime is an adaptation of the manga, or a Japanese
comic book. This manga is drawn out by Oda, and **Toei Animations** is the studio that adapts and animates the books in order to be digested in an alternate
form of media. Toei Animations often adds extra flair to the manga panels, and provides their own interpretation of how they perceived the manga, giving them some sense
of autonomy and control over the story they typically wouldn't have. 

One Piece has been published since 1997, and new manga chapters as well as anime episodes are released every Saturday.
These chapters are split into **arcs**, a self-contained narrative within a larger story. For example, the ultimate goal for these main characters never change, but each individual arc
gives Oda an oppurtunity to provide the readers/watchers with a brand new environment and dilemmas to help shape our characters, while keeping them true to the concrete values 
of a **Shonen** (a genre of Japanese comics and animated films aimed primarily at a young male audience, typically characterized by action-filled plots) protagonist.

This program incorporates an interactive menu using these 2 databases, prompting the user with options to analyze and digest the data until they decide to quit
out of the program. It's functions, as of this moment, are:
    
    1. Display Arc Information
    2. Display Individual Episode Information
    3. Display Top 50 According to IMDb
    4. Display Highest Rated Epsiodes in Specific Arc
    5. Display Arc Titles
    6. Display Chapter to Episode Ratio

## Method and Motivation
This project was completed using **Python** and the **Pandas** library contained within it to pull information from 2 databases. The first database was a list of the individual episodes,
containing their number, title, plot, and rating. The other database pertained more to the arcs within the show, and gave their names, number of episodes/chapters it spanned, and what 
respective portions of the manga and anime an arc took up. I had recently done my first project with Pandas, however my first project included some subjectivity from me as the creator.
While it was good practice with the new library under my belt, it felt "unofficial" due to the scoring system being self-constructed. In order to make a project that had some sense of
"merit" that I was searching for, I thought to look for a topic that had a more accepted ranking system, and immediately settled on TV/movie reviews, since those are the most commonly
ranked aspects of life. 

This brought me to think of a show to draw ratings from, and my mind went to my favorite of all time: One Piece.

## Analysis Guide
### Display Arc Information
This function is essentially a quick view into the detailed statistics regarding arcs contained in their corresponding database. It first asks the users if they
would simply like every arc and its information listed, or if they would like to view a specific arc. If the user decides to look at a specific arc, they are prompted
once more in case a list with every arc name is needed (can never be too careful with typos!), and the information in the database in condensed into an easily-digestable 
sentence.

### Display Individual Episode Information
The second function prompts the user to input the number of the episode they would like to analyze, with any episode between **1-1077** being permitted as the input. After this input,
the ratings, title, and plot are pulled from the database. Alternatively, we also employ a function called **how_many_more** to return the amount of episodes rated higher, as 
well as their corresponding titles. 

A sentence is given back to the user, displaying the rating, title, and the arc the epsiode belongs to using a **return_arc** getter function. We then list the amount of episodes
rated higher. The user is given the option if they would also like the titles of the episodes rated higher, as delivering it without demand imposes unnecessary clutter on the output.
Following this choice, the user has the option to return the plot associated with the episode number they inputted.

### Display Top 50 According to IMDb
This function is essentially just a getter function, and cannot be manipulated to produce a different output by the user. As a constant function, this doesn't contain much logic,
but it satisfies what is very likely the most important inquiry a user interested in this program may have. A show this big often gets analytically stretched out, meaning the current state
of the show is almost incomparable to how it began. This function disregards arcs, relative episodes, and any user input, just giving the unaltered rankings as they stand on IMDb.

### Display Highest Rated Episodes In a Specific Arc
This function features a series of if-elif statements that all produce a custom query that returns the rankings of episodes within an arc. The reason a custom query is needed because
a seperate database is being accessed after we get the arc to view from the user, and we accomplish it with snippets of replicating code of the structure:

code(if get_arc == 'Romance Dawn':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] < 4)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('ROMANCE DAWN: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))

The arc names are not saved in the IMDb ratings database, therefore we had to curate custom queries where the arc range is manually accounted for.

### Display Arc Titles
This is a clone of the portion of **Display Arc Information** where the user is given the choice to view a list with all the arcs. A simple getter so the user has access to the correctly
spelled names.

### Display Chapter to Episode Ratio
This function firstly gathers the total number of chapters and episodes contained in the database as a whole, and returns an average conversion of how many episodes Toei
Animation put out for every corresponding chapter. In a perfectly efficient world, there would be an episode or less for each chapter in the manga.

The second poriton of this function takes an inputted arc from the user, and returns the chapter-to-episode ratio for that specific case.
The overall average will stay unchanging, but users can see which arcs were more susceptible to dragging out the source material. The more episodes there are per chapter,
the more Toei Animations probably relied on unnecessarily long and extended episode renditions. This could have been implemented for any number of reasons, but the most common
is that One Piece is a **weekly** anime. Unlike many that deliver a season every year or 2, One Piece has a quota to release an episode a week.
This demand for quicker delivery may sometimes leave the studio chasing from behind, having to stretch budget and chapters for especially demanding arcs. 

### Quit
The last input option for the user is 0, which terminates the while loop the user is trapped in and quits the recurring menu. 
