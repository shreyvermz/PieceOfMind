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
          '6. Loguetown\n' +\
          '7. Warship Island\n' +\
          '8. Reverse Mountain\n' +\
          '9. Whiskey Peak\n' +\
          '10. Little Garden\n' +\
          '11. Drum Island\n' +\
          '12. Alabasta')

    which_to_describe = input('Choose the arc to receive a summary on: ')

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
        print('the focus of a specific Navy Admiral, Smoker, who witnessed the death of Gol D. Roger, and was baffled by the similarities he shared with Luffy.')
        print('It is in Loguetown where the audience is fully convinced Luffy will be King of the Pirates, as those who would want nothing less')
        print('are recognizing the danger he poses, as he could become a symbol for pirates as Roger once did.\n')
        
        print('Escaping death in the place where the previous King of Pirates was unable to shows us that Luffy is truly ready. We know the')
        print('One Piece is somewhere in the Grand Line, but now the crew truly starts the adventure and head to the entrance.\n')
        
    elif which_to_describe == str(7):
        
        print('\nWarship Island is an anime exclusive arc, meaning it was not included in the manga and is not a part of the')
        print('canon timeline. As the Straw Hats begin to make their jounrey to the Grand Line entrance, they encounter a young')
        print('child who was seperated from a Marine base. When on the way to deliver her back to her rightful home, the Straw Hats')
        print('encounter a dead zone in the sea where the currents lose their power. In this area, known as the Calm Belt, we run')
        print('into Sea Kings once more, which we were first introduced to in Romance Dawn when Shanks lost his arm for Luffy.\n')
        
        print('While this arc doesn\'t provide much plot resolution, the introduction of the Sea Kings as common')
        print('and easily encounterable creatures not only sets the precedent for what is to come in the Grand Line, but')
        print('what the entire world of One Piece is capable of.\n')
        
    elif which_to_describe == str(8):
        
        print('\nThe Reverse Mountain Arc marks the journey shifting from the East Blue to the Grand Line')
        print('Reverse Mountain being the entrance to the Grand Line, the crew is baffled to find that the mountain requires the ship')
        print('to go upstream the mountain, with seemingly no way to get there as the sea currents are completely still. When a pack')
        print('of Sea Kings (giant sea monsters we saw Shanks save Luffy from) tries to indulge in the Going Merry, their movement')
        print('shoots the ship up the mountain and to the Grand Line.\n')
        
        print('As the ship descends, the crew finds themselves plummeting into the mouth of a gargantuan whale, Laboon.')
        print('Upon entering, they find a retired old man living in the whale\'s belly, Crocus, who claimed to be a part')
        print('of the Roger Pirates. After some dialgoue, Crocus leads the Straw Hats out of Laboon, learning that he has been waiting')
        print('for a crew of pirates who he traveled with to return, as they couldn\'t take him to the perilous Grand Line.')
        print('Luffy recognizes Laboon\'s need for encouragement, and deems himself Laboon\'s rival, and orders him to wait for him')
        print('so they can have one last battle.\n')
        
        print('While not seeming important, I believe this arc contains one of the most brilliant plot points in the series, as')
        print('Laboon\'s relation to the crew is not left alone until their reunion. He is referenced once more in Thriller Bark,')
        print('and the synopsis for that arc will contain more info on Laboon\'s character return.\n')
        
    elif which_to_describe == str(9):
        
        print('\nWhiskey Peak is a succint arc, yet is used to set the tone for the first major journey in the')
        print('Grand Line: Alabasta. The crew also realizes after entering the Grand Line, their compasses no longer work.')
        print('In search of food, rest, and information, the crew stops on the closest island to them: Whiskey Peak.')
        print('When entering the island of Whiskey Peak, the Straw Hats are greeted by seemingly hospitable')
        print('citizens, and they indulge in drinks and food all night. The night turns when the citizens reveal')
        print('themselves as members of an organization called Baroque Works, and rob the pirates after') 
        print('they all go to sleep. Zoro retaliates by defeating over 100 of the bounty hunters posing')
        print('as citizens, including one Nefertari Vivi.\n')
        
        print('Luffy, enraged that Zoro would attack someone who fed him, engages in combat with his henchman, resulting in a short')
        print('and one-time brawl between the captain and right-hand man.\n')
        
        print('I would argue the true significance of this arc is it setting the tone for the things that Luffy finds important.')
        print('It doesn\'t matter to him that his new friends stole from him, he got his food. The theme that Luffy')
        print('helps anyone who shows him kindness in the form of food is exemplified throughout the show, but this being')
        print('the only time in the entire show Luffy actually gets mad at Zoro, it gives the audience plentiful insight into')
        print('the captain of the Staw Hats. Luffy being reinforced as a character who has an almost impossibly concise')
        print('moral compass, alongside simple and innocent motivations, further establishes the audience\'s trust in him.\n')
        
    elif which_to_describe == str(10):
    
        print('\nLittle Garden is an island the Straw Hats encounter after enlisting Vivi, who they found in Whiskey Peak, on their')
        print('ship. Here they find two giants from an Island called Elbaf, Dorry and Brogy, who have been locked in battle for')
        print('decades over reasons they can\'t remember. The crew split up upon reaching, as Zoro, Nami, and Usopp encounter')
        print('a man named Mr. 3 from Baroque Works, discovering Mr. 0 sent Mr. 3 to kill them, bearing a devil fruit that can')
        print('turn the crew to wax. Realizing his wax can be melted, the Straw Hats defeat him, earning more of Vivi\'s trust.\n')
        
        print('Meanwhile Sanji, taking solace in Mr. 3\'s house while he is fighting other crew members, intercepts a call from Mr. 0,')
        print('the head of Baroque Works. Sanji is taken as Mr. 3, and he is told to meet Mr. 0 in Alabasta through an Eternal Pose,')
        print('a compass that tracks the movement of waves and can be used accurately within the Grand Line. Before')
        print('departing, Zoro and Sanji begin their long-lasting feud via an argument about dinosaur meat. Dorry and Brogy')
        print('put their differences aside and bid the Straw Hats farewell, killing a Sea King blocking their exit.\n')
        
        print('While the crew now has the means to get to Alabasta, they set sail until Nami falls ill. Needing support for her and')
        print('anticipating to uncover something with Baroque Works, the crew deems they need a doctor before they go any further.\n')
        
    elif which_to_describe == str(11):
        
        print('\nIn need of a doctor for Nami and their journey ahead, the crew stops in a winter wonderland: Drum Island.')
        print('It is here they meet a talking reindeer named Chopper, along with his mentor Dr. Kureha. It is through')
        print('Kureha that we first hear of the Will of D., as she makes the connection between Gol D. Roger and Monkey')
        print('D. Luffy, the first time anyone does so in the whole series.\n') 
        
        print('We see Chopper being able to talk as a reindeer is a segue into the types of Devil Fruits, with different')
        print('types affecting the user and their abilities in different ways. Chopper\'s type, a Zoan, allows him to change')
        print('into a different animal, while Luffy\'s type, Paramecia, allows him to alter his body parts to another matter.\n')
        
        print('We then learn Chopper learned his medical skills from a doctor named Hiriluk, who died after Chopper tried')
        print('to save him, causing him to dedicate his life to continue his work of growing cherry blossoms on their island.')
        print('Chopper finds Hiriuk\'s legacy endangered by a man named Wapol, who seeks to take over the castle Hiriluk left')  
        print('behind. Luffy steps in as Wapol attempts to symboically erase Hiriluk, taking a canonball to the chest to')
        print('prevent the flag bearing a cherry blossom from being destroyed, earning Chopper\'s loyalty.\n')
        
        print('Other implications introduced in this arc include common noble behavior to be oppressive, demeaning, and')
        print('entitled: the complete opposite of the only noble we know, Nefertari Vivi.\n')
        
        print('We also catch wind of the Blackbeard Pirates, with their viciousness and lack of mercy being key identifiers.')
        print('We are foreshadowed a conflict between Blackbeard and Portgas D. Ace, the brother of Luffy.\n')
        
    elif which_to_describe == str(12):
        
        print('\nAlabasta is the biggest arc up to this point, and is the convergence point for the previous arcs since the')
        print('Straw Hats made their entrance into the Grand Line. It is here they discover that Mr. 0 of Baroque Works is')
        print('Crocodile, a Warlord of the sea. \'Warlord\' indicates he is a pirate with clearance from the World Government,')
        print('as long as he does their bidding.\n')
        
        print('Vivi and her father are the rightful rulers of Alabasta, a desert town that has gone dry from a lack of rain.')
        print('Crocodile keeps the population docile by promising prosperity if they give him allegiance, all the while')
        print('being the reason the town has no water in the first place.\n')
        
        print('We are introduced to the third type of Devil Fruit and how it works in battle, as we see Crocodile has the')
        print('Sand-Sand Fruit, allowing him to transform any part of his body to sand at will. This is the shared trait')
        print('of every Devil Fruit of this type: the Logia.\n') 
        
        print('Nico Robin is touted as a villain for most of this arc, however she is the one of the most important characters')
        print('of the whole show, with more to her being left unsaid thorugh a peek at her traumatizing backstory. She')
        print('is the first to mention the Poneglyphs, introducing them to the equation in the quest for the One Piece.')
        print('She also brings up the Will of D., leading the audience to believe Luffy has more and more merit to be')
        print('King of the Pirates.\n')
        
        print('Crocodile\'s fight with Luffy signified the beginning of the World Government taking the Straw Hats as a')
        print('serious threat. The infamy of Crocodile shocked the higher ups when the outcome of the fight was learned.')
        print('This fight also foreshadows the struggles Luffy will have in the New World in two ways: the first being')
        print('the level of difficulty that it took for Luffy to win. He was almost killed twice, and had to weaponize')
        print('water to get through to Crocodile\'s sand Logia fruit. Another instance would be Crocodile saying')
        print('the world will break Luffy\'s will when he approaches the New World, a prophecy that bears merit')
        print('in the Marineford and Sabaody Archipelago arcs.\n')
        
        print('Lastly, we get a better impression on the troubling hold the World Governnent has on the world around')
        print('them. First they take dishonorable action internally by disregarding Luffy\'s act of heroism, telling the')
        print('Marine soldiers that Admiral Smoker was the reason Crocodile lost, and giving Smoker a promotion.')
        print('Then, we see them altering the media reception of Alabasta, crediting the fall of Crocodile to another')
        print('Warlord, Doflamingo, in order to hide the truth from the general public. Finally, the very fact that')
        print('the World Government has a system that enables Warlords to exist is a clear sign of their moral hypocrisy.')
        print('The audience at this point begins to question the Marines calling themselves the \'righteous\'.\n')
        
                
    else:
        
        print('Not a valid input.\n')

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
        # show rankings but we go by arc   
        elif choice == str(4):
            
            display_rankings_in_arc()
        # show titles of arcs, simple getter
        elif choice == str(5):
            
            display_arc_titles()
         # show how many episodes per chapter on average   
        elif choice == str(6):
            
            chapter_to_episode_ratio()
        # no valid input    
        # typed out text description written by muah
        elif choice == str(7):
            
            give_arc_description()
            
        else:
            sys.exit('Not a valid input')
#########################################################################################      
menu()
