import pandas as pd
import numpy as np
import warnings
import sys
# arcs up till wano
# interactive menu that can give in depth info 
# user provided queries? can search through database based on inputted variables
# can provide a key that the user can access
# maybe loop that keeps going till user terminates the program? 
# downloaded another database that holds the ratings of the episodes
# can find arc's average epsiode rating
# max and min rated episode for each arc
warnings.filterwarnings('ignore')
# know reads work
episode_ratings = pd.read_csv('onepiece_IMDb_episodes_list_1077.csv')
arcs = pd.read_csv('OnePieceArcs.csv')
###############################################################################
def display_arcs(): # displays arc information, lets you 
                    # choose amount of arcs you can have displayed
    method_shown = input('Would you like info on a specific arc? Input \'Yes\' or \'No\': ')
    # show info from specific arc, simple query
    if str(method_shown) == 'Yes':
        # maybe need to add some error handling or a key to see the arc names 
        show_arc_names_choice = input('Before inputting the arc you want to look at, would you like a list of the arc names? Enter \'Yes\' or \'No\': ')
        if show_arc_names_choice == 'Yes':
            display_arc_titles()
        else:
           pass 
        
        input_arc = input('Please enter the name of the arc you\'d like to view followed by the word \'Arc\'.  ' +\
                          'An example input would be \'Whole Cake Island Arc\': ')
        
        total_chapters = arcs.loc[(arcs['Arc'] == str(input_arc)), 'TotalChapters'].values
        percent_of_manga = arcs.loc[(arcs['Arc'] == str(input_arc)), 'Manga%'].values
        total_episodes = arcs.loc[(arcs['Arc'] == str(input_arc)), 'TotalEpisodes'].values
        total_minutes = arcs.loc[(arcs['Arc'] == str(input_arc)), 'TotalMinutes(avg 24)'].values
        percent_of_anime = arcs.loc[(arcs['Arc'] == str(input_arc)), 'Anime%'].values
        start_epsiode = arcs.loc[(arcs['Arc'] == str(input_arc)), 'Start onEpisode'].values
        
        print('\nIn the ' + str(input_arc) + ', there are a total of ' + str(total_chapters) + ' chapters in the manga. ' +\
            'This arc account for ' + str(percent_of_manga) + ' of the manga. \nIt spans a total of ' + str(total_episodes) + ' episodes in ' +\
            'the anime, starting on epsiode ' + str(start_epsiode) + '.' + ' The total screentime is ' + str(total_minutes) + ' minutes. \nFinally, the ' + str(input_arc) + ' accounts for ' +\
            str(percent_of_anime) + ' of the anime.\n')
     #    
    else: 
    
        amount_shown = input('How many arcs would you like to see? Enter \'ALL\' to list the entire database: ')
    
        if amount_shown == 'ALL':
        
            print(arcs)
        # numerical amount 
        elif type(int(amount_shown)) == int:
     # 52 total, if less show that much, if more show all of them
            if int(amount_shown) < 52:
            
                print(arcs.head(int(amount_shown)))
            
            else:
            
                print(arcs)
        # not a number or a string saying 'ALL'    
        
##############################################################################

def display_ratings(): # gets epsiode number, prints rating 
                       # gives option to look at plot after we see the rating
                       # maybe give another option before looking at the plot to see where it ranks in the arc 
                       # mimick some of the how_many_averaged more function from previous project
                       # Can have it compare epsiode rating among the arc its in but also in the whole series
                       # to do it based on arc we'd need an index to map where each arc ends and begins 
    # get the episode to look at
    ratings_shown = input('What episode number would you like to see the rating of? (up to 1077): ')
    # get rating, title, plot, and how many are rated higher
    rating_to_return = episode_ratings.loc[(episode_ratings['Episode Number'] == int(ratings_shown)), 'Average Rating'].values
    episode_title = episode_ratings.loc[(episode_ratings['Episode Number'] == int(ratings_shown)), 'Title'].values
    episode_plot =  episode_ratings.loc[(episode_ratings['Episode Number'] == int(ratings_shown)), 'Plot'].values
    # holds amount rated higher and their titles
    how_many_better, descriptions = how_many_more(float(rating_to_return))
    
    # returning some info
    print('Episode ' + str(ratings_shown) + ', titled ' + str(episode_title) + ' has an average rating of ' + str(rating_to_return) + ' on IMDb. ' +\
          'This episode is found in the ' + return_arc(int(ratings_shown)))
    # show ones higher
    print('There are ' + str(how_many_better) + ' episodes rated higher throughout the show.')
    # give option to print out titles
    see_higher = input('Would you like to see the names of the episodes rated higher? Enter \'Yes\' or \'No\': ')
    # if they choose to see higher rated
    if see_higher == 'Yes':
        
        print('The higher rated episode titles are: ') 
        print(descriptions)
    # keep going if anything but yes   
    else:
        
        pass
    
    summary_choice = input('Would you like a plot summary for this episode? Please enter \'Yes\' or \'No\': ')
    
    if str(summary_choice) == 'Yes':
        
        print(episode_plot)
        
    else:
       # no return value for the function 
        return
        
#################################################################################
def display_episodes_ranked():
    
    # print('Would you like to see')
    
    rankings = episode_ratings.sort_values(['Average Rating'], ascending = [False])
    
    print(rankings.head(50))
###################################################################################
def chapter_to_episode_ratio():
    
    # get total for page and episodes first
    page_holder = arcs['TotalChapters'].values.sum()
    
    # print(page_holder)
    
    episode_holder = arcs['TotalEpisodes'].values.sum()
    
    # print(episode_holder)
    # still need to see if this is the best tool for comparison, we'll know after specific arc info
    print('For every chapter of the manga, on average there is ' + str(round(episode_holder/page_holder, 2)) + ' episodes in the anime.') 
    
    arc_selector = input('Choose which arc you would like to see the chapter to episode information for.\n' +\
                         'Keep in mind, follow the arc name with \'Arc\' to match with our database: ')
    # get specific chapters
    custom_chapter_analysis = arcs.loc[(arcs['Arc'] == str(arc_selector)), 'TotalChapters'].values.sum()
    # get specific episodes
    custom_episode_analysis = arcs.loc[(arcs['Arc'] == str(arc_selector)), 'TotalEpisodes'].values.sum()
    
    
    print('For the ' + str(arc_selector) + ' , there is an average of ' + str(round(custom_episode_analysis/custom_chapter_analysis, 2)) + ' episodes ' +\
         ('per chapter in the manga.'))

#############################################################################################
def display_rankings_in_arc(): # seperate arcs into their own categories
                               # seperate query for each time we look at a new arc
                               
    
    print('\nNOTE: Some shorter arcs have been included in bigger ones to maintain simplicity.\n ' +\
          'For example, \'Buggy Side Story Arc\' will be included in \'Loguetown\'.\n')
    
    get_arc = input('Input the name of the arc to see the rankings for: ')
    
    if get_arc == 'Romance Dawn':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] < 4)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('ROMANCE DAWN: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
        
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#  
    elif get_arc == 'Orange Town':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 4) & 
                                              (episode_ratings['Episode Number'] < 9)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('ORANGE TOWN: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'Syrup Village':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 9) & 
                                              (episode_ratings['Episode Number'] < 19)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('SYRUP VILLAGE: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#  
    elif get_arc == 'Baratie':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 19) & 
                                              (episode_ratings['Episode Number'] < 31)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('BARATIE: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
     #///////////////////////////////////////////////////////////////////////////////////////////////////////#  
    elif get_arc == 'Arlong Park':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 31) & 
                                              (episode_ratings['Episode Number'] < 46)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('ARLONG PARK: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))       
     #///////////////////////////////////////////////////////////////////////////////////////////////////////#         
    elif get_arc == 'Loguetown':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 46) & 
                                              (episode_ratings['Episode Number'] < 54)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('LOGUETOWN: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'Warship Island':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 54) & 
                                              (episode_ratings['Episode Number'] < 62)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('WARSHIP ISLAND: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
     #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'Reverse Mountain':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 62) & 
                                              (episode_ratings['Episode Number'] < 64)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('REVERSE MOUNTAIN: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'Whiskey Peak':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 64) & 
                                              (episode_ratings['Episode Number'] < 68)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('WHISKEY PEAK: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'Little Garden':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 68) & 
                                              (episode_ratings['Episode Number'] < 78)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('LITTLE GARDEN: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'Drum Island':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 78) & 
                                              (episode_ratings['Episode Number'] < 92)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('DRUM ISLAND: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
       #///////////////////////////////////////////////////////////////////////////////////////////////////////#       
    elif get_arc == 'Alabasta':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 92) & 
                                              (episode_ratings['Episode Number'] < 136)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('ALABASTA: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'Goat Island':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 136) & 
                                              (episode_ratings['Episode Number'] < 139)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('GOAT ISLAND: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'Rulula Island':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 139) & 
                                              (episode_ratings['Episode Number'] < 144)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('RULULA ISLAND: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
     #///////////////////////////////////////////////////////////////////////////////////////////////////////#         
    elif get_arc == 'Jaya':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 144) & 
                                              (episode_ratings['Episode Number'] < 153)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('JAYA: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'Skypiea':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 153) & 
                                              (episode_ratings['Episode Number'] < 196)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('SKYPIEA: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'G-8':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 196) & 
                                              (episode_ratings['Episode Number'] < 207)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('G-8: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'Long Ring Long Land':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 207) & 
                                              (episode_ratings['Episode Number'] < 220)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('LONG RING LONG LAND: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'Water 7':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 220) & 
                                              (episode_ratings['Episode Number'] < 264)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('WATER 7: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'Enies Lobby':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 264) & 
                                              (episode_ratings['Episode Number'] < 313)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('ENIES LOBBY: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'Thriller Bark':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 313) & 
                                              (episode_ratings['Episode Number'] < 382)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('THRILLER BARK: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'Sabaody Archipelago':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 382) & 
                                              (episode_ratings['Episode Number'] < 406)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('SABAODY ARCHIPELAGO: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
     #///////////////////////////////////////////////////////////////////////////////////////////////////////#         
    elif get_arc == 'Amazon Lily':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 406) & 
                                              (episode_ratings['Episode Number'] < 422)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('AMAZON LILY: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
     #///////////////////////////////////////////////////////////////////////////////////////////////////////#         
    elif get_arc == 'Impel Down':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 422) & 
                                              (episode_ratings['Episode Number'] < 457)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('IMPEL DOWN: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
     #///////////////////////////////////////////////////////////////////////////////////////////////////////#         
    elif get_arc == 'Marineford':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 457) & 
                                              (episode_ratings['Episode Number'] < 517)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('MARINEFORD: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'Return to Sabaody Archipelago':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 517) & 
                                              (episode_ratings['Episode Number'] < 523)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('RETURN TO SABAODY ARCHIPELAGO: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'Fishman Island':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 523) & 
                                              (episode_ratings['Episode Number'] < 575)] 
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('FISHMAN ISLAND: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'Punk Hazard':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 575) & 
                                              (episode_ratings['Episode Number'] < 629)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('PUNK HAZARD: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
       #///////////////////////////////////////////////////////////////////////////////////////////////////////#       
    elif get_arc == 'Dressrosa':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 629) & 
                                              (episode_ratings['Episode Number'] < 747)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('DRESSROSA: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
       #///////////////////////////////////////////////////////////////////////////////////////////////////////#       
    elif get_arc == 'Zou':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 747) & 
                                              (episode_ratings['Episode Number'] < 783)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('ZOU: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    elif get_arc == 'Whole Cake Island':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 783) & 
                                              (episode_ratings['Episode Number'] < 878)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('WHOLE CAKE ISLAND: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
       #///////////////////////////////////////////////////////////////////////////////////////////////////////#       
    elif get_arc == 'Levely':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 878) & 
                                              (episode_ratings['Episode Number'] < 890)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('LEVELY: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
       #///////////////////////////////////////////////////////////////////////////////////////////////////////#       
    elif get_arc == 'Wano Country':
        
        ranged_rankings = episode_ratings.loc[(episode_ratings['Episode Number'] >= 890) & 
                                              (episode_ratings['Episode Number'] < 1077)]  
        ranged_rankings = ranged_rankings.sort_values(['Average Rating'], ascending = False)
        
        print('WANO COUNTRY: ')
        for i, row in ranged_rankings.iterrows():
            
            print('Episode: ' + str(row['Episode Number']) + ' | Titled: ' + str(row['Title']) + ' | Rating: ' + str(row['Average Rating']))
      #///////////////////////////////////////////////////////////////////////////////////////////////////////#        
    else:
        closing_statement = '\nNot a valid arc. Try Displaying Arc Titles and enter the arc as is without \'Arc\' identifier. \n' +\
                            'For example, if listed as \'Dressrosa Arc\' simply input Dressrosa.\n'
                            
        print(closing_statement)
        
        
 ################################################################################################################################################   
def return_arc(episode_number): # index to map episode to arc names
                                # i wouldnt consider all these individual arcs, but i cant change it otherwise I wont be able to access database information cleanly 
    
    if episode_number < 4:
        return 'Romance Dawn Arc'
    elif 4 <= episode_number < 9:
        return 'Orange Town Arc'
    elif 9 <= episode_number < 19:
        return 'Syrup Village Arc'
    elif 19 <= episode_number < 31:
        return 'Baratie Arc'
    elif 31 <= episode_number < 46:
        return 'Arlong Park Arc'
    elif 46 <= episode_number < 48:
        return 'Buggy Side Story Arc'
    elif 48 <= episode_number < 54:
        return 'Loguetown Arc'
    elif 54 <= episode_number < 62:
        return 'Warship Island Arc'
    elif 62 <= episode_number < 64:
        return 'Reverse Mountain Arc'
    elif 64 <= episode_number < 68:
        return 'Whiskey Peak Arc'
    elif 68 <= episode_number < 70:
        return 'Koby and Helmeppo Arc'
    elif 70 <= episode_number < 78:
        return 'Little Garden Arc'
    elif 78 <= episode_number < 92:
        return 'Drum Island Arc'
    elif 92 <= episode_number < 131:
        return 'Alabasta Arc'
    elif 131 <= episode_number < 136:
        return 'Post-Alabasta Arc'
    elif 136 <= episode_number < 139:
        return 'Goat Island Arc'
    elif 139 <= episode_number < 144:
        return 'Rulula Island Arc'
    elif 144 <= episode_number < 153:
        return 'Jaya Arc'
    elif 153 <= episode_number < 196:
        return 'Skypiea Arc'
    elif 196 <= episode_number < 207:
        return 'G-8 Arc'
    elif 207 <= episode_number < 220:
        return 'Long Ring Long Land Arc'
    elif 220 <= episode_number < 225:
        return 'Ocean\'s Dream Arc'
    elif 225 <= episode_number < 229:
        return 'Foxy\'s Return Arc'
    elif 229 <= episode_number < 264:
        return 'Water 7 Arc'
    elif 264 <= episode_number < 313:
        return 'Enies Lobby Arc'
    elif 313 <= episode_number < 326:
        return 'Post-Enies Lobby Arc'
    elif 326 <= episode_number < 337:
        return 'Ice Hunter Arc'
    elif 337 <= episode_number < 382:
        return 'Thriller Bark Arc'
    elif 382 <= episode_number < 385:
        return 'Spa Island Arc'
    elif 385 <= episode_number < 406:
        return 'Sabaody Archipelago Arc'
    elif 406 <= episode_number < 408:
        return 'Special Historical Arc'
    elif 408 <= episode_number < 422:
        return 'Amazon Lily Arc'
    elif 422 <= episode_number < 457:
        return 'Impel Down Arc'
    elif 457 <= episode_number < 490:
        return 'Marineford Arc'
    elif 490 <= episode_number < 517:
        return 'Post-War Arc'
    elif 517 <= episode_number < 523:
        return 'Return to Sabaody Arc'
    elif 523 <= episode_number < 575:
        return 'Fishman Island Arc'
    elif 575 <= episode_number < 579:
        return 'Z\'s Ambition Arc'
    elif 579 <= episode_number < 626:
        return 'Punk Hazard Arc'
    elif 626 <= episode_number < 629:
        return 'Caesar Retrieval Arc'
    elif 629 <= episode_number < 747:
        return 'Dressrosa Arc'    
    elif 747 <= episode_number < 751:
        return 'Silver Mine Arc'
    elif 751 <= episode_number < 780:
        return 'Zou Arc'
    elif 780 <= episode_number < 783:
        return 'Marine Rookie Arc'
    elif 783 <= episode_number < 878:
        return 'Whole Cake Island Arc'
    elif 878 <= episode_number < 890:
        return 'Levely Arc'
    elif 890 <= episode_number < 895:
        return 'Wano Country Arc: Act 1'
    elif 895 <= episode_number < 918:
        return 'Cidre Guild Arc'
    elif 918 <= episode_number < 959:
        return 'Wano Country Arc: Act 2'
    elif 959 <= episode_number <= 1077:
        return 'Wano Country Arc: Act 3'
    # if episode is outside of our range
    else:
        return 'Episode doesn\'t map to arc in database.'
##################################################################################
def give_arc_description():
    
    print('1. Romance Dawn\n' +\
          '2. Orange Town\n' +\
          '3. Syrup Village\n' +\
          '4. Baratie\n' +\
          '5. Arlong Park\n' +\
          '6. Loguetown')

    which_to_describe = input('Choose the arc to receive a summary: ')

    if which_to_describe == str(1):
        
        print('\nRomance Dawn is where the journey begins. We are introduced to an exuberant, carefree, and joyous') 
        print('young man known as Monkey D. Luffy, the man who claims he will be King of the Pirates. His aloof approach') 
        print('to an otherwise serious and deadly world lands him with a loyal henchman, Roronoa Zoro.') 
        print('They embark on their journey as the Straw Hat Pirates, Luffy with his eyes set on King of the Pirates, and Zoro on being the greatest swordsman.\n') 
        print('The audience is introduced to the one unifying item between criminals and the government: the One Piece.') 
        print('The existence of it is only confirmed by the word of one man to wield such a treasure, as well as being the') 
        print('most wanted man in history, and the only one to ever be King of the Pirates: Gol D. Roger. The pirates yearn') 
        print('to possess such a mystical treasure, and the World Government, the most powerful force in the world, will') 
        print('stop at nothing to ensure the One Piece does not fall into the hands of the ones they deem criminals.\n')
        print('Luffy and Zoro run into trouble in a Marine base, and find themselves at the mercy of a Marine officer.')
        print('The Marines are touted as the rightoeous, yet this official takes advantage of the World Government\'s')
        print('authoritity to impose his unjust will on citizens and even his subordinate Marine officers.\n')
        
    elif which_to_describe == str(2):
        
        print('\nOrange Town takes us away from the military base island and introduces Luffy to Nami, another key component to his adventure.')
        print('We don\'t know much of Nami\'s background yet, besides being a thief, but she approaches Luffy and seems to give him her allegiance.')
        print('She then sells out the overly-trusting Luffy to Buggy the Clown, another Devil Fruit user, who gives Luffy yet another obstacle to pass.')
        print('Buggy is shown to be an important clown, however, as he and Luffy\'s guardian angel, Shanks, are shown')
        print('to have been on the crew of the Roger Pirates, or the crew who found the One Piece.\n')
        print('While they were young and didn\'t boast any significant contributions, it shows the importance of Shanks as a character and how Luffy connects to the world aroud him.\n')
        
    elif which_to_describe == str(3):
        
        print('\nSyrup Village is where we meet our crew\'s sniper Usopp, although when we\'re first introduced to him, he is the leader')
        print('of the fearsome Usopp Pirates, a crew consisting of him and three fiercely loyal children from his village.\n')
        print('We then meet Usopp\'s best friend, Kaya who is bedridden and perpetually sick. Luffy is introducd to Kaya, when they realize')
        print('she is intentionally being kept sick by her butler, Klahadore, the ex-leader of the Black Cat Pirates. With eyes on')
        print('Kaya\'s family fortune, Klahadore has much to gain from Kaya being unable to inherit her shipbuilding business. It is up')
        print('to Luffy and the crew to save her from the unknown clutches of the only family she has left.\n')
        print('After successfully freeing Kaya from her sickness, she gifts the crew the Going Merry, named after her butler who stayed loyal.')
        print('Usopp shares his dream of overcoming his fears and being a fierce warrior of the seas, joining Luffy, Zoro, and Nami on their journey.\n')
        
    elif which_to_describe == str(4):
        
        print('\nAfter adding Usopp to the Straw Hats, the crew ends up at a ship that is branded as a restaurant called the Baratie, providing')
        print('haven for all seafarers. Upon visitng, the Straw Hats encounter a cook named Sanji, the underling of the restaurant owner Zeff,')
        print('who took Sanji in as a kid and trained him for most of his life. Luffy respects Sanji and wants him to join his crew')
        print('as the cook, to which Sanji initially declines.\n') 
        print('A pirate named Don Krieg lays siege to the Baratie, hoping to claim the ship')
        print('for his pirating indulgences. While Luffy fights Krieg, Zoro encounters a swordsman named Mihawk.\n')
        print('We are now introduced to Zoro\'s goal, as Mihawk is the current strongest swordsman in the sea, and Zoro will have to beat him to')
        print('achieve his dream.\n') 
        print('Nami splits from the Straw Hats amidst the chaos to satisfy her greater goal, which the audience isn\'t aware of yet.')
        print('Sanji joins the party, and being a ferocious fighter. slides into his role alongside Zoro as the Wings of the King of the Pirates.\n')
        
    elif which_to_describe == str(5):
        
        print('\nThe Straw Hats gained a cook at the Baratie, but lost a navigator in the process. Nami has fled from the Straw Hat Pirates, betraying them')
        print('one more time before setting off to the headquarters of the pirate crew she shows true allegiance to, Arlong Park.\n')
        print('Luffy, being as simple minded as he is, simply refuses to give up on Nami. They follow her to Arlong Park, to discover the people')
        print('of her hometown being exploited and mistreated by a group of Fishmen led by Arlong. The town is shaken down for their money and resources,')
        print('and death is threatened in the absence of compliance.\n')
        print('We see Nami\'s backstory, and learn that she is obssessed with money to buy her village\'s freedom. After learning of this,')
        print('Luffy calls on his crew to help him overthrow the Arlong Pirates, imparting Nami with his treasured Straw Hat as a reminder of his support.\n')
        print('It is in this arc we see the conventionally stupid and absent-minded Luffy being extremely capable of emotional intelligence')
        print('and grounding his crew, which is exemplified more and more as the show goes on. Nami rejoins the Straw Hats and Arlong Park is destroyed.\n')
        
    elif which_to_describe == str(6):
        
        print('\nAfter being captured by Buggy, Luffy is brought to Loguetown, where Roger was executed. It is here that we see how Luffy reacts when truly')
        print('faced with death. As he realizes there is no way out, and the guillotine is about to drop on his neck, Luffy closes his eyes, smiles his heart out,')
        print('and tells his crew\n')
        print('"Sorry guys! I\'m dead!"\n')
        print('Luffy is then pardoned from death after being saved by a mysterious benefactor who can seemingly control lightning. The smile on Luffy\'s face is')
        print('the focus of a specific Navy Admiral, Smoker, who witnessed the death of Gol. D. Roger, and was baffled by the similarities he shared with Luffy.')
        print('It is in Loguetown where the audience is fully convinced Luffy will be King of the Pirates, as those who would want nothing less')
        print('are recognizing the danger he poses, as he could become a symbol for pirates as Roger once did.\n')
        print('Escaping death in the place where the previous King of Pirates was unable to shows us that Luffy is truly ready. We know the')
        print('One Piece is somewhere in the Grand Line, but now the crew truly starts the adventure and head to the entrance.\n')

##################################################################################    
def how_many_more(rating):
    
    more = episode_ratings.loc[(episode_ratings['Average Rating'] > rating), 'Title'].count()
    
    episodes_better = episode_ratings.loc[(episode_ratings['Average Rating'] > rating), 'Title'].values
    
    return more, episodes_better
####################################################################################
def display_arc_titles():
    
    for i, row in arcs.iterrows():
            
            print(arcs['Arc'][i])       
################################################################################
def menu():
    # holds truth value for while statement
    quit_holder = False
    
    print('Welcome to Piece of Mind! Choose a number from the menu to use the ' +\
          'corresponding function!')
    # until the user inputs 0
    while quit_holder != True:
        
        print('0. Quit the program')
        
        print('1. Display Arc Information')
        
        print('2. Display Individual Episode Info')
        
        print('3. Display Top 50 Episodes According to IMDb Ratings')
        
        print('4. Display highest rated episodes in certain arc')
        
        print('5. Display Arc Titles')
        
        print('6. Display Chapter to Episode Ratio')
        
        print('7. Give Arc Description (work in progress)')
        
        choice = input('Choose a number to use a function: ')
        # quitting the program
        if choice == str(0):
            
            print('Goodbye Nakama!')
            
            quit_holder = True
        # displaying arcs    
        elif choice == str(1):
            
            display_arcs()
        # displaying individual episode rating, may be able to integrate it for bigger functions and make it a getter   
        elif choice == str(2):
            
            display_ratings()
        # show all the episodes in the show ranked by average rating
        elif choice == str(3):
            
            display_episodes_ranked()
            
        elif choice == str(4):
            
            display_rankings_in_arc()
        
        elif choice == str(5):
            
            display_arc_titles()
            
        elif choice == str(6):
            
            chapter_to_episode_ratio()
        # no valid input    
        
        elif choice == str(7):
            
            give_arc_description()
            
        else:
            sys.exit('Not a valid input')
#########################################################################################      
menu()
