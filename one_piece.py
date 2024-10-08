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
          '12. Alabasta\n' +\
          '13. Jaya\n' +\
          '14. Skypiea\n' +\
          '15. G-8\n' +\
          '16. Long Ring Long Land\n' +\
          '17. Water 7\n' +\
          '18. Enies Lobby\n' +\
          '19. Thriller Bark\n' +\
          '20. Sabaody Archipelago\n' +\
          '21. Amazon Lily\n' +\
          '22. Impel Down\n' +\
          '23. Marineford\n' +\
          '24. Post-War Arc\n' +\
          '25. Return to Sabaody Archipelago\n' +\
          '26. Fishman Island\n' +\
          '27. Punk Hazard\n' +\
          '28. Dressrosa\n' +\
          '29. Zou\n' +\
          '30. Whole Cake Island\n' +\
          '31. Wano Country')

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
        
    elif which_to_describe == str(13):
        
        print('\nThe Jaya arc can be viewed as a prequel to the Skypiea arc. We arrive in Mock Town, a place that denounces')
        print('myths, ironically as the Straw Hats are looking for somebody that has heard of the Sky Island.\n')
        
        print('While searching for answers, Luffy meets a strange man with a similar zest for exploration and making life')
        print('an adventure. He proclaims to Luffy, in the land of dead dreams: \'A man\'s dreams never die!\', after')
        print('Luffy was mocked and jumped for even suggesting that he was looking for the Sky Island.')
        print('Luffy didn\'t realize it in the moment, but this man was Blackbeard, a dangerous pirate.\n')
        print('It is through Blackbeard that we are also briefly shown Fleet Admiral Sengoku, and Warlords')
        print('Kuma and Doflamingo. We are then shown a glimpse of the Five Elders, the people at the very')
        print('top of the World Government.\n')
        
        print('Before Luffy learned how to get to the Sky Island, the Knockup Stream, Luffy was attacked by Bellamy, a')
        print('suboordinate of the aforementioned Warlord Doflamingo. Bellamy gets wiped out in one punch by Luffy,')
        print('and his embrassing encounter exemplifies that Luffy is becoming more infamous and fearsome to the common eye.')
        print('Bellamy\'s connection to Doflamingo sets the stage for a conflict between Doflamingo and Luffy in the') 
        print('Dressrosa arc.\n')
        
    elif which_to_describe == str(14):
        
        print('\nAfter entering the Knockup Stream from Jaya, the Straw Hats arrive at the Sky Island, Skypiea. This island')
        print('adds a whole new dynamic to the geography of the One Piece world. We learn that there are other sky')
        print('islands in existence, expanding the enticing ridiculousness of the world Oda continues to build.\n')
        
        print('After staying for a bit, the crew begins to notice that the citizens heed the influence of their God very')
        print('seriously. If anyone stepped out of line, they were subject to a lightning strike from a seemingly')
        print('omnipotent creature. After further investigation, a man with a lightning Logia fruit, Enel, uses his')
        print('Mantra (later established as Observation Haki) to keep tabs on the whole island.\n')
        
        print('A band of freedom fighters, the tribe of the Shandia, lead the Straw Hats to believe about the existence')
        print('of a city of gold, which they suspect to be the upper area of Skypiea, where Enel resides. They lay siege')
        print('to the area, helping the tribe of Shandia overcome Enel\'s forces, and find the city to be real.')
        print('Luffy uses his rubber properties to defeat Enel, and rings a Golden Bell in order to signify to Skypiea')
        print('that he has won, casting a giant shadow of himself in the sky, allowing it to be seen from Jaya.')
        print('It is in this moment that Luffy restores a sense of wonder to the people of Mock Town, showing a theme')
        print('of Luffy bringing Joy to the world.\n')
        
        print('The emancipation of Skypiea and restoration of Jaya\'s faith by Luffy is an impressive individual')
        print('occurence in the context of the arc, but this arc lays the groundwork for a transformation shown')
        print('almost 1000 episodes later in Wano Country. While celebrating, the tribe of Shandia keys the audience')
        print('into the existence of mysterious War Drums that seem to follow a battle attaining freedom, and in the')
        print('anime, the rhythm sounds similar to the recurring theme song we hear before all of Luffy\'s battles.')
        print('This is our first introduction to the Drums of Liberation.\n')
        
        print('The crew finds a Poneglyph, which once again highlights Robin\'s indispensable importance to the')
        print('crew, as she is one of the only people alive who is able to read them.')
        print('The one they find mentions an Ancient Weapon known as Poseidon. There was a message on the Poneglyph')
        print('left by Gol D. Roger, meaning that the Roger Pirates were truly successful in finding the One Piece,')
        print('and were also able to uncover the truth of the world that the World Government works to hide.\n')
        
    elif which_to_describe == str(15):
        
        print('\nThe G-8 arc, like the Warship Island arc, is anime only and therefore, not canon. After leaving')
        print('Skypiea, the Going Merry lands in the middle of a Marine outpost fortified by walls, leaving') 
        print('them trapped. The crew undergoes a series of shenanigans, not limited to Luffy and Sanji')
        print('impersonating chefs of the Marines, in order to eventually get caught anyways, and make their')
        print('escape using a dial and inflatable octopus.\n')  
        
    elif which_to_describe == str(16):
        
        print('\nLong Ring Long Land feels reminsicent of a filler arc, as it\'s a smaller impact arc')
        print('that was more common to the start of the show, however this arc is placed between two of')
        print('the biggest ones up to this point, Skypiea and Water 7. It is here the crew has to undergo')
        print('trials at the hand of Foxy the pirate, and Sanji and Zoro show that despite their constant')
        print('arguing, they make a formidable duo as they are able to best giants in a game of physical')
        print('skill.\n')
        
        print('This arc also introduces us to the suave Admiral Aokiji, who claims the Marines didn\'t take')
        print('the Straw Hats seriously until their addition of Nico Robin. Aokiji also mentions Luffy\'s')
        print('grandfather as helping him in some way, prompting curiosity within the group. Aokiji, unseriously,')
        print('begins to fight the Straw Hats and easily defeats them, however doesn\'t capture them. After')
        print('realizing he is still far weaker than most, Luffy begins formulating new moves that begin to')
        print('show in the subsequent arcs.\n')
        
        print('It is in this arc the crew begins to discuss the damage sustained by the Going Merry in past arcs,')
        print('especially Skypiea, and make the decision to find a shipwright that they can rely on to keep')
        print('the Merry in shape for the following journey. This search for a new crew member leads them to an')
        print('island called Water 7.\n')
        
    elif which_to_describe == str(17):
        
        print('\nWater 7 is an island that specializes in ship building, as the entire city forms a coexisting')
        print('relationship with the water around them, such as using it to provide energy, regulating transportation')
        print('to boats and rivers instead of cars and roads (a la Venice), and the existence of the most skilled')
        print('shipwrights in history, including the man who constructed Gol D. Roger\'s ship, the Oro Jackson.\n')
        
        print('The Straw Hats are introduced to an eccentric cyborg powered by cola, Franky, who at first seems to brood')
        print('trouble for the crew. After attacking Usopp, Luffy dismantles Franky\'s gang and earns the respect of')
        print('the cyborg. We flash back to see Franky\'s past, learning under the shipwright Tom, who created')
        print('the Oro Jackson. Tom sacrificed his life to protect the blueprints of Pluton, an Ancient')
        print('Weapon that was mentioned in Alabasta, which was passed down through the shipwrights of Water 7')
        print('for centuries. We also see the hunting down of Tom further enforcing that the World Government')
        print('is a dangerous organization, and what the Straw Hats do is more and more justified.\n')
        
        print('Franky being a shipwright declares the Going Merry is in dire shape, and it\'s not likely it')
        print('can be used much longer. Luffy is open to the idea of a new ship, which Usopp takes offense')
        print('to, and considers his willingness to move on from their ship as the equivalent of giving up')
        print('on a friend. The audience can sympathize with Usopp as we see the Merry\'s significance to him')
        print('in Syrup Village, and Usopp decides to leave the crew despite knowing there\'s nothing to be done.')
        print('We then see Usopp challenge Luffy, and lose with ease, signifying his departure from the Straw Hats,')
        print('much to Luffy\'s chagrin.\n')
        
        print('Although Usopp does reunite with the crew, it is not without great care from Zoro, stating')
        print('"We\'re not kids playing pirates", and telling Luffy that if he accepts Usopp back without')
        print('hearing an apology first, Zoro will be the next one to leave. This shows that despite Zoro')
        print('staying fiercely loyal to Luffy, he only does so because of the respect he has for Luffy.')
        print('It is made clear here that if Luffy strays from his path or doesn\'t stick to his beliefs,')
        print('Zoro will no longer be a Straw Hat.\n')        
        
        print('It is no surprise that in the arc following Aokiji\'s explanation of Robin\'s importance to the')
        print('Straw Hat\'s infamy, Robin ends up being the focal point of conflict. We learn she has been in')
        print('league with a World Government agency known as CP9, and she splits from the rest of the crew.')
        print('Her past is also shown a bit more, as she has knowledge of CP9\'s capability of executing a')
        print('Buster Call, a command to summon an island-destroying fleet at the press of a button. It is this')
        print('knowledge of destruction that the World Government is capable of that pushed Robin to abandon the Straw')
        print('Hats, as she believes if she stays with them they will meet an untimely end, hinting that she may have')
        print('seen a similar occurence happen already.\n')
        
        print('Luffy refuses to believe that Robin left on her own accord, and is adamant to get her back')
        print('on the crew. Thus, the recovery mission for Nico Robin begins.\n')
        
    elif which_to_describe == str(18):
        
        print('\nEnies Lobby can be viewed as a continuation of Water 7. The Straw Hats have learned that Robin')
        print('felt she had to abandon them to ensure their own safety while foregoing her own, an unacceptable')
        print('notion to Luffy.\n')
        
        print('We are finally shown Robin\'s past, detailing that she hailed from a land of scholars, Ohara. They')
        print('were a peaceful people, who dedicated themselves to preserving and sharing knowledge through the')
        print('world. It is through the Oharans that Robin learned to read Poneglyphs, as she was trained since')
        print('a very young age. While perfomring studies, the Oharans began to uncover details about the Void')
        print('Century, or a time period before the emergence of the World Government that they work tirelessly')
        print('to hide, signifying a possible better world before the dominance of the World Government was instilled.')
        print('When learning that Ohara has made discoveries of the Void Century, a Buster Call is enacted on Ohara,')
        print('as ships showed up within 30 minutes and left the island in the sea. Robin was the only survivor of this')
        print('genocide, as she was saved by a giant and Aokiji. Her survival and knowledge of the Void Century,')
        print('as well as ability to read Poneglyphs, prompted the Government to place a gargantuan bounty on her,')
        print('earning her the reputation that the audience hears in previous arcs.\n')
    
        
        print('After Robin explains to Luffy why she can\'t live the life she wants to, Luffy orders Usopp, under the')
        print('guise of Sogeking as to not have to confront Luffy yet, to shoot a hole through the World Government')
        print('flag, declaring war on the world and putting a bigger target on his back than Robin ever could.\n')
        
        print('Following this, Robin finally forgives herself and accepts help from the Straw Hats. Every crew member')
        print('shows development in their strength, unleashing new moves, including Luffy\'s Gear 2 and 3. Franky joins the')
        print('crew, and the size of the Straw Hats continues to grow. We see the threat level of the Straw Hats also')
        print('grow exponentially, as Luffy\'s bounty puts him in the territory of the Warlords of the Sea. The Going')
        print('Merry finally reaches it\'s breaking point, as the crew gives it a Vikings funeral. They replace the')
        print('Going Merry with a ship bearing a similar figurehead, the Thousand Sunny.\n') 
        
        print('The audience learning of the Void Century and the existence of an Ancient Kingdom that was overthrown')
        print('and erased by its enemies (seemingly the World Government), means the vague morality surrounding the World')
        print('Government begins to fade. The closer Luffy gets to the top, the more the guise that the Government')
        print('works so hard to keep up begins to crack, as their patterns of oppression and corruption are now the norm')
        print('rather than the exception.\n')
        
    elif which_to_describe == str(19):
        
        print('\nThriller Bark takes place on an abandoned island straight out of a horror movie. Checking every cliche in')
        print('the book, we see zombies, ghosts, ghouls, human-made animals, and even undead skeletons in the form of our')
        print('newest Straw Hat, Brook.\n')
        
        print('Brook is a talking skeleton who we find alone, singing to himself on a ship floating aimlessly around the island.')
        print('It is here we learn about his past, as he was a musician for his previous crew before they were bested by the')
        print('Grand Line, and they all persished. Brook, however, ate the Revive-Revive Fruit, meaning his soul returned to')
        print('his body after he died.\n')
        
        print('After Brook tags along with the crew, the Straw Hats meet a man named Gecko Moria, a Warlord of the Sea who')
        print('possesses the Shadow-Shadow Fruit, allowing the capture of a person\'s shadow and holding their soul for ransom.')
        print('Moria has been building an army to return to the notoriety he once had, with his magnum opus being the body')
        print('of the giant, Oars.\n')
        
        print('We see Kuma show up once more, this time explaining his Paw-Paw Fruit, and using it to remove the pain Luffy endures')
        print('through his fight with Moria and his army, and gives a portion of it to Zoro. Zoro almost dies from this exchange, and')
        print('his loyalty to his captain is solidified as he doesn\'t let anyone else learn or acknowledge what he did.')
        print('Zoro also battles the corpse of Ryuma, a legendary samurai that Moria defiled to add to his army. Zoro')
        print('bests the samurai and earns his sword, Shusui, which adds another legendary sword to his arsenal.\n')
        
        print('After the battle has concluded and the crew has their customary feast to celebrate, Brook explains that the pirates')
        print('Laboon, the whale the Straw Hats first encountered when entering the Grand Line, is waiting for is his crew')
        print('that met their demise before Brook\'s death. He explained how Laboon would follow him to listen to the music')
        print('Brook would play, and Luffy promises to reunite them once more. Brook officially joins the Straw Hats as their')
        print('musician.\n')
        
    elif which_to_describe == str(20):
        
        print('\nSabaody Archipelago is a collection of interconnected islands that signifies the halfway point between the entrance')
        print('of the Grand Line and the location of the One Piece. The area is called the Red Line, due to the large mountain range')
        print('that spans the One Piece world.\n')
        
        print('When entering a bar, Luffy and his crew encounter Silvers Rayleigh, the former right hand man of Gol D. Roger.')
        print('Upon sparking conversation, Luffy refuses to get any help or clues regarding the One Piece, as Rayleigh is a man')
        print('who could divulge every secret they want to know.')
        print('We see Luffy\'s path to King of the Pirates solidified once again, this time through the approval of Rayleigh.')
        print('Luffy\'s refusal to "spoil his adventure" leads Rayleigh to believe Luffy posseses the same disposition as Roger,')
        print('and he is hereby convinced by the rubber man\'s will.\n')
        
        print('We are introduced to other pirates who entered the world around the same time as Luffy, including Trafalgar Law,')
        print('Eustass Kidd, Capone Bege, X Drake, and others who would later be labeled the Worst Generation. These characters')
        print('would go on to garner massive prominence in the world in later arcs.\n')
        
        print('It is shown that the Celestial Dragons, descendants of those who formed the World Government, are a deployable and')
        print('disguisting people. They use slaves to forego tasks like walking, simply riding around on the backs of their')
        print('slaves as they crawl on their hands and knees. Racism is a large motivator for them, as we see Fishmen')
        print('being treated as subhuman, and explaining why Fishmen such as Arlong would have deep rooted hatred for humans.')
        print('Luffy shows his disdain for the Celestial Dragons by punching one in the face after it shot Hacchan, former')
        print('member of the Arlong Pirates, for trying to save a mermaid from being sold into slavery.\n')
        
        print('Luffy\'s arrival at Sabaody Archipelago would alert the World Government after the crew\'s increased notoriety, and')
        print('a new admiral, Kizaru, is showcased with his Glint-Glint Fruit, essentially allowing him to weaponize and turn into')
        print('light. We see a man named Sentomaru as well, who is the operator and creator of Pacifistas, Government-created cyborgs')
        print('to carry out their will. Sentomaru and Kuma arrive at the scene, with Kuma using his Paw-Paw Fruit')
        print('to banish the Straw Hats from the island one by one, seemingly killing them, devastating Luffy as he watches until')
        print('he falls to his knees and uncontrollably begs Kuma to stop.\n')
        
        print('We see a brief moment where Kuma whispers to Rayleigh, signifying that he actually just helped the Straw Hats')
        print('by delivering them to safety on scattered islands, setting the stage for their reunion later on.')
        print('The loyalties of Kuma are even more convoluded after these events, as we know already that Kuma has been')
        print('involved with Luffy\'s dad and Revolutionary leader, Dragon, in some capacity.\n')
        
        print('By appearance to the audience and the rest of the world, the Straw Hat Pirates met their end in Sabaody Archipelago.\n')
        
    elif which_to_describe == str(21):
        
        print('\nEach of the Straw Hats were sent away by Kuma in Sabaody Archipelago. Nami was sent to a Sky Island, Weatheria.')
        print('Franky is sent to Karakuri Island, the birthplace of Vegapunk, who is the world\'s most renown scientist and')
        print('plays a large role in later arcs. Sanji is sent to Momoiro Island, home of the Okamas. Usopp is sent to Boin')
        print('Archipelago, a land of nature where all the plants and animals are greatly exaggerated in size. Brook is sent')
        print('to Namakura Island where he is mistaken for Satan. Nico Robin is sent to Tequila Wolf in the East blue, and')
        print('becomes a slave. Chopper is sent to the Torino Kingdom, and Zoro finds himself on Kuraigana Island with Perona,')
        print('an antagonist in Thriller Bark, and his archnemesis: Mihawk.\n')
        
        print('The arc is named after the land where Luffy was sent, which is Amazon Lily. This island is a place of only women,')
        print('and typically no men are allowed whatsoever. Here Luffy meets Boa Hancock, another Warlord of the Sea, and her Love-Love')
        print('Fruit, which turns anyone who falls in love with her into stone. After trying this on Luffy and failing, she is disarmed')
        print('and begins to trust him. After learning that Luffy assaulted a Celestial Dragon in Sabaody Archipelago, Hancock actually')
        print('falls in love with Luffy.\n')
        
        print('Before gaining her trust, we learn of the nuances of arguably the most important combat skill in this world: Haki. We')
        print('have seen instances of Observation Haki from people like Enel and his Mantra, and Armament Haki in the cases where Luffy')
        print('gets hurt despite being made of rubber. The most important of all is when Luffy is found to have Color of the')
        print('Supreme King, a rare type of Haki that Hancock also has. Not much information is provided on Color of the')
        print('Supreme King, however, context tells us Luffy bearing it will be a major boost in combat.\n')
        
        print('It is in Amazon Lily that Luffy hears of the battle between Blackbeard and Ace, his brother. After learning that Ace')
        print('has been captured by the World Government and is held in the maximum security prison, Impel Down, Luffy sets course')
        print('to save him immediately. Hancock goes with Luffy to help him.\n')
        
    elif which_to_describe == str(22):
        
        print('\nGoing back to the area of Enies Lobby, Luffy visits the biggest prison in the One Piece world in order to')
        print('save Ace. The prison goes thousands of meters underwater, and has multiple levels designed to torment')
        print('the prisoners depending on the severity of their crimes. While traversing the prison, Luffy meets many of his')
        print('old foes, including Buggy, Crocodile, Mr. 3, and some new characters that have been mentioned, such as Jimbe, First')
        print('Son of the Sea, who is also a close friend to Ace. We also meet Ivankov, the second in command to Dragon and the')
        print('Revolutionary Army, as well as the leader of the Okama island Sanji finds himself sent to by Kuma.\n')
        
        print('As Luffy moves through Impel Down, he is poisoned and almost dies at the hands of the warden, Magellan, but is saved by')
        print('Ivankov\'s Hormone-Hormone Fruit. Luffy also almost gets stopped while traversing through the levels on Impel')
        print('Down, but is accompanied and helped repeadetly by Bon Clay. Bon Clay seemingly sacrifices himself so Luffy')
        print('can escape, solidifying him as an ally for life to Luffy.\n')
        
        print('We learn here about Ace\'s loyalty to Whitebeard, and how he is a member of the Whitebeard Pirates. We also learn')
        print('Whitebeard is the protector of Fishman Island, using his flag to deter any pirates who would mess with it. This')
        print('exemplifies the kindness of Whitebeard, as Fishmen are discriminated against by the World Government, and')
        print('we see Whitebeard protecting a people who need it the most.\n')
        
        print('Luffy releases the prisoners in order to cause chaos and hopefully divert attention away from Ace and his execution.')
        print('The prison break releases many of Luffy\'s past and future enemies, and sets the stage for major participants in the')
        print('following arc: Marineford.\n')      
        
    elif which_to_describe == str(23):
        
        print('\nMarineford marks the first major turn of events and transfers of power in the One Piece world. After breaking out')
        print('of Impel Down, the Marines decide to move up Ace\'s execution as to not let Luffy get a chance to save him.')
        print('Ace is put on a stage for the world to see, and the event is broadcasted as well. His post for execution is guarded')
        print('by 3 Admirals: Aokiji, Kizaru, and Akainu, holder of the Magma-Magma Fruit. Luffy and Ace\'s grandpa, Garp, is also present.\n')
        
        print('It is revealed that Ace is actually the son of Gol D. Roger, and followed a childhood of violence due to the condemnation')
        print('of any offspring of the King of the Pirates by the general public. We also learn that Ace respects Whitebeard immensly')
        print('and considers him his true father. We see this exemplfied when Whitebeard himself appears to save Ace. The world also')
        print('learns that Luffy is the son of Dragon and grandson of Garp, furthering his notoriety.\n')
        
        print('The war escalates as Whitebeard arrives with his entire fleet and his world-shattering (literally) Devil Fruit, allowing')
        print('him to crack the very fabric of reality. We learn from Marine dialogue that we\'re lucky Whitebeard has the fruit, as ')
        print('he has the power to destroy the world on a whim. The Marines engage with waves of pirates, causing chaos and allowing for')
        print('Luffy to make his entrance.\n')
        
        print('We see the Blackbeard pirates enter the scene, taking advantage of the chaos and possessing fresh new recruits comprising')
        print('of highly dangerous prison breakouts from Impel Down. The Blackbeard Pirates gang up on Whitebeard, taking advantage')
        print('of him being crippled by a life-threatening disease, and the fact that he was already stabbed from behind. After various')
        print('gunshot, cannonball, and knife wounds, Whitebeard finally dies while staying on his two feet, declaring the One Piece is real')
        print('to stir up chaos in his last moments. The passing of Whitebeard left many islands unprotected, including Fishman Island.\n')
        
        print('Whitebeard\'s death and Ace\'s rescue occur almost simultaneously, and we see the Admiral Akainu take advantage of a distraught')
        print('Ace. With an oppurtunity to escape, Ace hears Akainu taunting his idol, sending him to a fury of rage and consequentially')
        print('ending his life. Holding a dying Ace in his arms, Luffy goes into state of shock, unable to move or react to the environment')
        print('around him. Shortly before dying, Ace mentions Sabo, the third brother of Luffy and Ace, and a character who would be')
        print('a vital character in later arcs.\n')
        
        print('After killing Whitebeard, Blackbeard is revealed to have stolen his Devil Fruit powers, allowing him to use 2 Devil Fruit powers')
        print('at once, previously established in the story to be impossible. Not only does he have 2 fruits, these are 2 of the most')
        print('powerful fruits an individual could have. This would be the main shift of power in the world to result from this arc, as')
        print('Blackbeard and his crew ascends to one of, if not the most, dangerous and influential competitors for the Straw Hats.\n')
        
        print('We learn that Kuma was indeed helping the Straw Hats in Sabaody Archipelago, as Kuma is revealed to be a Revolutionary')
        print('under the command of Dragon, Luffy\'s dad.\n')
        
    elif which_to_describe == str(24):
        
        print('\nWitnessing the Straw Hats suffer defeat at Sabaody Archipelago, Luffy losing and almost dying in Impel Down to Magellan,')
        print('and his failure to successfully save Ace makes one thing clear to the audience: the Straw Hats need to get stronger. With')
        print('the tumultuous events at Marineford, the time period following it is called the \'New Age\'.\n')
        
        print('The balance between Marines, pirates, and Warlords is unstable by this point with the loss of Warlords such as Jimbe')
        print('and Blackbeard, as well as the death of an Emperor of the Sea: Whitebeard. Garp and Sengoku resign from their positions,')
        print('with Aokiji being considered for Fleet Admiral. Many of the pirates at Marineford or who escaped from Impel Down cross')
        print('the Red Line into the New World.\n')
        
        print('Following the death of Ace, we are given flashbacks of Luffy and Ace\'s childhood. Here we learn Luffy and Ace are')
        print('not related by blood in any way, but rather Ace, Luffy, and the third brother briefly mentioned in Marineford, Sabo,')
        print('declare their siblinghood by sharing their dreams and a cup of sake. We see that Sabo presumably died when the 3 were')
        print('children, as he descended from a line of Nobles, containing him to a life of education and conformity. Trying to escape')
        print('from this fate and find his calling at sea, he departs from his hometown and is shot down by the World Government due')
        print('to a concurrent arrival of a World Noble who requested the child be killed.\n')

        print('Luffy, clearly worn down by experiencing so much trauma in such a short time, has a talk with Jimbe, crying and')
        print('declaring he is too weak to save his friends, and doubts his ability to continue his journey to be King of the')
        print('Pirates. Jimbe displays his newfound friendship by calming Luffy down and getting him prepared for the New Age.\n')
        
        print('Luffy devises a plan to meet with the crew again in 2 years, signaling to the Straw Hats by making the news')
        print('and displaying a tattoo: "3D2Y", with the 3D crossed out, meaning to meet again in 2 years instead of 3 days.')
        print('Chopper begins studying medicine in Torino Kingdom. Sanji learns how to walk on air in order to run away')
        print('from the transgender women on Okama Island. Nami begins to learn how to manipulate and weaponize weather')
        print('on Weatheria, a sky island. Brook composes music for the tribe that believes he is Satan. Robin joins Dragon')
        print('and the Revolutionary Army in Baltigo. Franky begins to study Dr. Vegapunk\'s weaponry and technology on')
        print('Karakuri Island, the place of Vegapunk\'s birth. Usopp undergoes survival training under Heracles to survive')
        print('the overgorwn Boin Archipelago. Zoro begins training under Mihawk on Kuraigana Island. Luffy begins to train')
        print('with Rayleigh, the second-hand-man to Gol D. Roger, and learns how to properly use his Haki.\n')
        
        print('The next time we see the Straw Hats, they will all have become more capable. From this point in the story,')
        print('the Straw Hats are a true force to be reckoned with, and are more capable of helping those in need.')
        print('Rather than the Straw Hats being the protected, they are now the protectors.\n')
        
    elif which_to_describe == str(25):
        
        print('\nThe Return to Sabaody Archipelago marks the major "time skip" in this show. This arc shows the reunion of the')
        print('Straw Hats after they took 2 years to hone their skills. While a very short arc, it is important')
        print('to show the development of Luffy, as the events at Sabaody were devastating for him the first time,')
        print('as the Straw Hats were bested by Kuma with ease. We see Luffy fighting an upgraded Pacifista upon his')
        print('return, putting him in a familiar situation. This time, however, the Pacifista is unable to even touch Luffy,')
        print('and Luffy defeats the cyborg in one Haki-coated punch.\n')
        
        print('It is also in this arc we are introduced to new designs for character and a shift in art style from the author,')
        print('Eichiro Oda.\n')
        
    elif which_to_describe == str(26):
        
        print('\nFishman Island takes place in the depths of the New World, a city enclosed by a transparent exterior, and allowing')
        print('for a view of the ocean while also allowing for inhabitants to breathe.\n')
        
        print('We see the abilities the Straw Hats have developed over their 2 year training period. Luffy has gained considerable')
        print('control over the 3 types of Haki, as well as mastery over using his Devil Fruit. Zoro becomes stronger and faster') 
        print('and learns about the existence of Haki after training under the world\'s greatest swordsman: Mihawk.')
        print('Nami has a new weapon that is able to influence the weather to a greater degree, as well as furthering her')
        print('understanding of the weapon as well. Usopp upgraded his slinghsot and uses oversized and deadly plants from')
        print('the Boin Archipelago, as well as making strides in the sense of his bravery. Sanji was able to develop a technique')
        print('shown by CP9, sky walking, and also is aware of the existence of Haki. Chopper develops mastery over his Devil')
        print('Fruit power, able to control his most deadly forms. Robin furthers Devil Fruit powers and learns how to make exact')
        print('clones of herself. Franky adds on to his cyborg body, now able to shoot lazers like Kizaru and Pacifistas, and also')
        print('added Transformers-esque vehicles to the docking bay of the Thousand Sunny. Brook discovers that the true power')
        print('of his Devil Fruit allows him to remove his soul from his body at any time, as well as starting a tour of the Grand')
        print('Line to display his music chops.\n')
        
        print('Robin provides more explanations of Ancient Weapons mentioned in past arcs, noting there are three in existence named')
        print('Poseidon, Pluton, and Uranus. When consulting with the Mermaid Princess, Shirahoshi, Robin learns that Shirahoshi')
        print('is actually the ancient weapon dubbed Poseidon, due to her ability to control the gargantuan Sea Kings roaming the area.')
        print('Shirahoshi requests help from the Straw Hats regarding Hordy Jones, a violent Fishman cut from the same cloth as Arlong.\n')
        
        print('The motivation for Hordy Jones\' brutal ways are shown through the trangressions against Fishmen, and how racism')
        print('develops internalized anger and reactionary characters. The icon of the Sun Pirates, or Fishmen who banded together')
        print('to support each other, Fisher Tiger, has his past shown. A Fishman who tried to befriend humans, he was only repayed')
        print('with discrimination and was enslaved. He was famous for releasing slaves from Marie Geoise, the home of the Celestial')
        print('Dragons, but died because he refused blood transfusion from a human, out of spite. Fisher Tiger is the character')
        print('that spurred Hordy Jones, and even Arlong, to be as ruthless and inconsiderate as they were.\n')
        
        print('Luffy is able to free Shirahoshi and defeat Hordy Jones, releasing his grip on Fishman Island. Luffy also makes strides')
        print('to repair the human bond with Fishman, as he does what Fisher could not and accepts a blood transfusion from Jimbei.')
        print('This act, paired with the selflessness and help provided by the Straw Hats, lowers tensions between humans and Fishmen,')
        print('with the residents of Fishmen Island once again being open to human-Fishman relations, and being more accepting of humans.')
        print('Luffy then asks Jimbe to join the Straw Hats, an offer that is declined but revisited in Whole Cake Island.\n')
        
        print('This is the arc we get the first mention of a monumental character: Joy Boy. Robin is told that Joy Boy built a giant')
        print('ship intended to take the inhabitants of Fishman Island to the surface, however he failed to deliver on the promise and')
        print('left an apology letter on a Poneglyph that the Straw Hats are shown by the royal family. We learn that Luffy can hear the')
        print('voices of the Sea Kings under Shirahoshi\'s control, leading the Sea Kings to tell Luffy that Gol D. Roger was also')
        print('able to "hear the voice of All Things".\n')
        
        print('The first appearance of another Emperor of the Sea, Big Mom, takes place in this arc and sets the stage for')
        print('the Whole Cake Island arc, as Luffy declares war on Big Mom after wanting to place Fishman Island under his')
        print('protection following the death of Whitebeard.\n')
        
    elif which_to_describe == str(27):
        
        print('\nPunk Hazard takes place on an island that was already unstable due to failed experiments by Dr. Vegapunk, which')
        print('we learn involved the creation of artificial beings such as dragons. Disaster struck one more time before')
        print('the Straw Hat\'s arrival, as seen following the Marineford conflict. As Fleet Admiral Sengoku retired following')
        print('the Marine\'s failure, Admirals Aokiji and Akainu fought over his vacated position, leaving half of Punk Hazard')
        print('frozen over and covered in snow, and the other half volcanic and uninhabitable.\n')
        
        print('The Worst Generation is officially monikered, as it refers to a group of pirates entering the sea around the')
        print('same time as Luffy, and it includes a new Warlord of the Sea, Trafalgar Law. Luffy and Law meet in Punk Hazard,')
        print('and they strike up an alliance that lasts for subsequent arcs. We learn about Law\'s Devil Fruit as well, the Op-Op')
        print('Fruit, allowing teleportation and the ability to cut without opening wounds, similar to how Buggy takes himself apart.\n')
        
        print('The main villain of this arc, Caesar Clown, was a competitor of Vegapunk and resorted to the creation of mass-murder')
        print('weapons and human expirementation in hopes to pass his rival. The Straw Hats learn Caesar has been practicing gigantification')
        print('on children in his lab on Punk Hazard, with Law explaining these experiments would be useful to the World')
        print('Government, as they were researching gigantification in order to develop a stronger army. Caesar was also shown to')
        print('create artifical Devil Fruits called SMILES, and they can only be made in Zoan forms.\n')
        
        print('Luffy defeating Caesar meant his ability to create giants was unavailabele, leading to Big Mom, an Emperor of the Sea,')
        print('attempting to steal a captured Caesar from the Straw Hats. Big Mom is also involved in another topic explained')
        print('by Law, the Underworld. He states Donquixote Doflamingo is an extremely powerful Underworld Broker, calling himself')
        print('the Joker, and partakes in illegal trading with several important world figures. We see Doflamingo in the Dressrosa arc.\n')
        
        print('The connection between Devil Fruits and Haki are explored more. We see that Armament Haki allows for anyone to combat')
        print('Logia fruit users, disregarding what element their body is made of, and cutting through all the same. This sets the')
        print('stage for non-Devil Fruit users to be explicably able to best Devil Fruit users, and begins the notion that Haki is the')
        print('most important aspect to a character\'s strength. We also learn that when a Devil Fruit user dies, their fruit regrows in')
        print('the place of a normal fruit somewhere in the world, allowing for someone else to gain the same power again, but two can')
        print('never have it at once.\n')
        
    elif which_to_describe == str(28):
        
        print('\nAfter learning about Doflamingo and his role in the Underground through the discovery of the SMILES operation, the')
        print('Straw Hats head to Dressrosa. Dressrosa is a place reminiscent of the Renaissance era, with an emphasis on arts')
        print('and performance. Besides humans, the audience sees a population of puppets that seemingly coexist with the people.')
        print('On the outside looking in, not much seems to be peculiar about the town.\n')
        
        print('A tournament is held with the intent of drawing Luffy in using the reincarnation of Ace\'s Devil Fruit as the prize.')
        print('We learned in the previous arc, following a Devil Fruit-holder\'s death, the fruit they had takes the place of another')
        print('normal fruit elsewhere in the world. Luffy enters the event with a gray mustache, sunglasses, and changes his alias to Lucy.')
        print('Before partaking in the finale, Luffy learns that his other brother, Sabo, is in fact alive, and is the second-in-command')
        print('under Luffy\'s father, Dragon, in the Revolutionary Army. Sabo tells Luffy he will win and eat the fruit for Ace, and promises')
        print('nobody else will be able to.\n')
        
        print('The audience is shown Law\'s backstory, and why he wanted to form an alliance with Luffy. Doflamingo was the brother of')
        print('Law\'s mentor, Corazon. While bearing similar strength, Corazon was the complete opposite person as Doflamingo. Caring,')
        print('kind, and considerate, Law admired him in his youth. After Law ate the very important Op-Op Fruit as a child, Doflamingo')
        print('set out to kill Law in order to obtain the fruit in its regrowth. Corazon protects Law with his life, dying in the process,')
        print('and instilling a hatred for Doflamingo in Law.\n')
        
        print('The Donquixote and Nefertari families are revealed to be direct descendants of the creators of the World Government, as')
        print('we see Doflamingo was raised by considerate parents, yet retaliation from non-Celestials radicalized the young boy, leading')
        print('him to kill his father after he resigned as a Celestial Dragon, and begin a life dedicated to bringing others misery.\n')
        
        print('The puppet-people that were first seen coexisting with the humans of Dressrosa are revealed to have been humans once')
        print('themselves, with Doflamingo essentially regulating them to slave labor, unable to even go home to their families or')
        print('let others know of their existence. We also learn of the Tontatta Tribe, a subset of the Dwarves species. Their existence')
        print('is hidden to the people of Dressrosa, as they avoided notoriety as to not be exploited by Doflamingo.\n')
        
        print('Moving to the final battle, we learn that Law also carries the "Will of D.", with his full name being Trafalgar D. Law.')
        print('During a flashback to Corazon, we learn those with the Will of D. are described as the "natural enemies of God" by the')
        print('World Government, exemplifying their caution regarding those with the Will of D. We learn Doflamingo has Color of the Supreme')
        print('King as well when him and Luffy clash, emitting a sort of black lightning that can be felt for a wide area. Luffy activates')
        print('a new form developed under Rayleigh during his training, Gear 4th. We also see Zoro use Armament Haki in this arc, as well')
        print('as Usopp activating Observation Haki. As shown by Doflamingo, we learn that Devil Fruits don\'t grant their full power')
        print('to a user right away, allowing for the fruit to be "awakened", leading it to affect things other than the user themselves.')
        print('This is demonstrated as Doflamingo is able to change the environment around him into strings as he struggles to beat')
        print('Luffy\'s new form.\n')
        
        print('Following the defeat of Doflamingo, seperate groups witnessing Luffy\'s victory pledge their allegiance to him, forming the')
        print('Straw Hat Fleet, to which Luffy insists for the members to do whatever they want. Law attempts to end his alliance with Luffy,')
        print('prompting Luffy to refuse and keep Law as his ally. We see a Marine Admiral, Fujitora, being the first Admiral to express')
        print('positive sentiment to Luffy, as he states arguably my favorite dialogue of the series:\n')
        
        print('"You\'re a fool Straw Hat, but an honest one. I suppose I shouldn\'t be surprised everyone wants to take your side. What kind')
        print('of a man are you, I wonder? What\'s the color of your hair, the shape of your eyes? What does your smile look like?')
        print('What a pity, I wish I could use these eyes one last time to see the face of a man like you. I\'m sure it\'s filled to the brim')
        print('with kindness."\n')
        
        print('This quote provides some level of humanization to the Marines, showing that alongside Garp, there are members who find pride')
        print('in doing the honorable thing. This quote perfectly summarizes Luffy and his appeal to me. To view things simply can make you')
        print('lack nuance, but it can also circumvent doubts of one having pure intentions. When the common person shares time with Luffy, they don\'t')
        print('wonder if he is using those he is helping to further his own goals. His irrationality exemplifies the commitment he shows to values')
        print('he carries through the show. On the outside, this irrationality can make Luffy seem volatile and stupid. However, I would argue that')
        print('Luffy\'s actions are perfectly rational, and it is not the volatility of Luffy that brings chaos where he goes, but it\'s the world')
        print('around him reacting to his sincerity that causes chaos. The world is made to conform, made to shape people into an identity that is cohesive')
        print('to everyone else around them so they can maintain order and push the system forward. Luffy\'s "system" is himself, as we see repeadetly')
        print('that Luffy doesn\'t crave power, he craves freedom for himself and for those who show him and the world kindness. This quote by Fujitora,')
        print('to me, is Oda directly talking to the reader, saying that to be sincere, to be yourself, is the best way to share your light with the world.\n')
        
    elif which_to_describe == str(29):
        
        print('\nThe Zou arc serves as a bridge in between Dressrosa and Whole Cake Island, while also setting the stage for the Wano Country arc that follows.')
        print('Zou introduces us to a behemoth of an elephant named Zunesha, who has been walking the world for centuries, tall enough that only the bottom of')
        print('their legs are submerged in the ocean. On the back of Zunesha, we find a town named Zou, thriving as it is protected from the sea by Zunesha, who')
        print('also bathes themselves twice a day, simulating rainfall and bringing resources from the sea up to the people of Zou. The inhabitants of Zou are')
        print('shown to be a tribe called the Mink, humanoid animals mentioned in Sabaody Archipelago.\n')
        
        print('When the Straw Hats arrive, a suboordinate of Kaido, Jack, threatens to murder the Minks and destroy their land if they do not turn over a')
        print('member of their tribe. After not breaking and almost being wiped out, they reveal they have been hiding the samurai, Raizo, the whole time,')
        print('and were fine with being wiped out if it meant protecting their friend. Momonosuke, a child from Wano Country, is revealed to have traveled')
        print('with Gol D. Roger on his ship, as he was the heir to Wano from his father, Kozuki Oden. Oden had sailed with Roger to Laugh Tale.')
        print('Impressed with his new friends, Luffy establishes a Ninja-Mink-Pirate-Samurai Alliance that lasts until Wano Country.\n')
        
        print('In her attempt to capture Caesar Clown, it is shown that Big Mom also captures Sanji. It is revealed that Sanji is the child of a man named')
        print('Vinsmoke Judge, who heads a powerful army known as Germa 66, that is also heavily involved with the Underworld. Although his past isn\'t fully')
        print('disclosed yet, Sanji\'s reaction to the Vinsmoke name catching up to him shows that he has negative associations with them.\n') 
        
        print('Vital information on how to locate the One Piece is revealed. The existence of 4 Road Poneglyphs is detailed, and how the 4 together will give')
        print('the coordinates to Laugh Tale. The Straw Hats find their first Road Poneglyph on Zou. The others are spread out through the world, with one being')
        print('lost, one being in possession of Kaido, and another in the possession of Big Mom. The path to find it gets muddier for the Straw Hats, however,')
        print('as it is described that the remnants of the Whitebeard Pirates were wiped out by Blackbeard, who was now an Emperor of the Sea.\n') 
        
    elif which_to_describe == str(30):
        
        print('\nEntering Whole Cake Island from Zou, the Straw Hats enter the realm of Totto Land, an archipelago spanning 35 small islands.')
        print('The land is made out of treats and food, with the power of Big Mom\'s Soul-Soul Fruit, allowing her to break off a piece')
        print('of her soul and give an inanimate object life. She uses this power with the intentions of making Totto Land a place that')
        print('has at least one of all races of beings in the One Piece world. The beings brought to life by Big Mom are known as Homies.')
        
        print('Moving on from her home\'s geography, we are provided with information about Big Mom herself. She has been married 43 times,')
        print('bearing 46 sons and 39 daughters. Most of her marriages were non-consensual, and her powerful status made men fear to resist')
        print('her yearning to grow her family. We learn that Big Mom got her powers from her time living in an orphanage as a kid.')
        print('It is heavily implied that she was able to attain these powers not from eating the Soul-Soul Fruit directly, but when')
        print('a birthday party was thrown for her by the bearer of the fruit, and the caregiver of the orphanage, Big Mom fell into')
        print('a fit of gluttony, not stopping at eating her gargantuan cake, but eating all other children of the orphanage, as well as')
        print('the caretaker.\n')
        
        print('The main plotline in this arc is a side of inner conflict within Sanji we weren\'t shown before. We are shown the operations')
        print('and past of Sanji\'s birth family, the Vinsmokes. His dad, Vinsmoke Judge, performed experiments on his children, giving')
        print('them superhuman abilities in order to make the most perfect army in the world. However, Sanji failed to show the development')
        print('of these powers, and suffered prolonged abuse as a result. He was beaten up by his superhuman strength-bearing siblings,')
        print('who were shown to be losing their sense of humanity, taking after their father. They beat him to the brink of death often, whether')
        print('it was for showing kindness by feeding starving rats, or if it was for simply existing. All this behavior was further')
        print('vindicated by Judge, who made it clear he had no interest in protecting the life of a failure. After being held in prison by his')
        print('father who was tired of dealing with him, he was able to escape with the help of his only sister, who was alone amongst his siblings')
        print('in showing him kindness, seeing the image of their deceased mother in the young boy. At age 8, Sanji was able to escape and found')
        print('the man who became the father figure he deserved: Zeff.\n')
        
        print('We learn that Sanji\'s bounty describing him as wanted "Only Alive" was at the command of Judge, who wanted to reunite with')
        print('his son to complete a marriage between his family and a member of Big Mom\'s, a ploy to gain more influence. Sanji')
        print('has the life of the Straw Hats held over his head by Big Mom, who wanted to use the marriage in order to murder Sanji and his family.')
        print('In an attempt to make his crew believe he betrayed them rather than having them know he essentially is sacrificing himself')
        print('for them, Sanji attacks Luffy, who does nothing. Luffy doesn\'t beleive Sanji for a second, and declares he will die before')
        print('letting Sanji leave. After a tearful departure, Sanji is set to marry Pudding, the daughter of Big Mom. For the first time')
        print('in the series, Luffy doesn\'t show unwavering optimism in his ability to be King of the Pirates in his speech to Sanji')
        print('by saying: \n')
        
        print('"Without you, I can\'t become King of the Pirates!"\n')
        
        print('This line marks one of the most impactful moments of the show, as Luffy has never acknowledged the fact that he might fail')
        print('in his quest. We\'ve learned being King of the Pirates isn\'t even Luffy\'s ultimate dream, it is simply a vehicle to')
        print('get to his dream. The bond among the crew now transcends the original goals that they set out to sea with, not because')
        print('it\'s not important to them anymore, but the goals of the crew have almost all merged into one glorious amalgamation.')
        print('Rather than individuals who teamed up out of necessity for their dreams, we are reminded they are now a group that lives')
        print('for each other.\n')
        
        print('The true intentions of Pudding and her plan to murder Sanji is learned by the Straw Hats and Sanji. Sanji still decides to go through')
        print('with the wedding to protect his crew, any sign of optimism forfeited as he was actually smitten with Pudding, and didn\'t hate the')
        print('idea of marrying her. Luffy and the crew share no such sentiment, however, and crash the wedding. In the process, Judge learns about')
        print('Big Mom\'s plan to kill Sanji and the Vinsmokes too late, and would have died if not for being saved by Sanji. After')
        print('escaping and saving the Vinsmokes, Sanji makes Judge swear to leave him and Zeff alone for life, disowning him as a father.')
        
        print('Taking on the most powerful of Big Mom\'s children, Katakuri, Luffy advances his strength and mastery of Haki even further.')
        print('He activates two new forms in Gear 4, Tank Man and Snake Man. He also learns that advanced mastery of Observation Haki allows')
        print('the user to see slightly into the future, a skill which Luffy masters during his fight with Katakuri. We also learn that Haki')
        print('strengthens through combat with an opponent of a higher skill.\n')
        
        print('In Whole Cake Island\'s concluding phase, Jimbe finally joins the Straw Hats, an addition that had been postponed since his')
        print('promise with Luffy at Fishman Island. Nami also receives an upgrade in combat, stealing Big Mom\'s personal Homie, a')
        print('thundercloud named Zeus.  We revisit the Mink Tribe, and their duty to go help the samurai of Wano, setting course')
        print('for the Straw Hat\'s next destination.\n')
        
    elif which_to_describe == str(31):
        
        print('\nThe last arc available in this programs database, Wano Country, is the show\'s longest arc, as it is split up into three')
        print('acts, and features the character referred to as the "Strongest Creature in the World", Kaido. Wano Country is a secluded nation,')
        print('and doesn\'t recognize the World Government as its rulers. This allows them to govern themselves and enforce the lifestlye they')
        print('believe in, however this also leaves them without the aid of the Marines in times of military conflict. The population is made of samurais,')
        print('with an emphasis on Japanese clothing and culture incorporated in their way of life.\n')
        
        print('We learn the backstory of Wano and how Kaido came to power, tricking the previous Shogun, Kozuki Oden, to his death while subjugating')
        print('the people of Wano to Oden\'s rival, Orochi. Orochi was more of a figure head for Kaido to exact his will behind, however the power')
        print('that Orochi did have was used to make the citizens of Wano suffer. Orochi\'s clan was subject to scrutiny due to their efforts to rebel,')
        print('and him and his family suffered from discrimination by most people of Wano.\n')
        
        print('Kozuki Oden is shown to have been a kind and passionate leader, exuding a personality similar to Gol D. Roger, who liked the')
        print('samurai so much, he was invited aboard the crew on their journey to Laugh Tale. Oden treated his retainers and citizens with respect,')
        print('being revered until the interference of Orochi and Kaido. The public execution of the Kozuki clan, including Momonosuke and his sister')
        print('Hiyori, prompted Oden\'s wife to use her Devil Fruit powers to send Momonosuke 20 years in the future, to where she describes')
        print('"a new dawn" that will be ushered by men entering Wano. Momonosuke learns of his father\'s journey and will from Yamato, the son of Kaido')
        print('who despises the Emperor and idolizes Oden. Yamato shares Oden\'s logbook with Momonosuke, detailing that Luffy was in fact the man who')
        print('would bring a new dawn to the Land of Wano, revealing that he has the exact same dream as Gol D. Roger. Both Roger and Luffy were made fun')
        print('of by their friends for having such a silly dream, one we still don\'t know of. Yamato was able to find out Luffy\'s dream due to Ace visiting')
        print('Wano and becoming friends with Yamato.\n')        
        
        print('When detailing the journey of Oden with the Roger Pirates, Yamato mentions Joy Boy, a character mentioned in Fishman Island that')
        print('existed before the age of the World Government, and is one of the most important characters involving the mysterious history of the One Piece')
        print('world. It is explained in Oden\'s logbook that Joy Boy left a treasure in the final island, Laugh Tale. Oden then describes the very moment')
        print('the Roger Pirates laid their eyes on the One Piece: laughter. The joyous outburst from the group led to the island\'s name, calling whatever')
        print('Joy Boy left behind a "funny story". Oden then decided he wanted to open the borders of Wano, as to create a massive change in the world, and')
        print('more specifically, to welcome a certain person into the country when the time came.\n')
        
        print('Moving back to present day in Wano, Luffy meets a young girl named Otama, feeding him red bean soup after hearing he was very hungry. After eating,')
        print('Luffy learns that Otama gave him the last of her food despite being on the brink of starving. It is then described to Luffy of what Kaido and')
        print('Orochi\'s rule has done to the Land of Wano. Arms development plants were sprung up all over the country, with the citizens being forced to undergo')
        print('slave labor to produce materials for the rulers. Every source of water was poisoned besides the ones directly in control of Kaido and Orochi, not')
        print('only making water undrinkable, but hunting was not an option either, as the animals would also be drinking from the same water.')
        print('The horrors continue, however, as we learn that Caesar Clown\'s manufacturing of SMILE fruits were at the request of Kaido.')
        print('The SMILE fruits were mostly defective, with the rare case of one working granting the eater a Zoan-type Devil Fruit power.')
        print('The ones that didn\'t bestow a Devil Fruit power left the user unable to express themselves in any way but laughter. Whether')
        print('that person hears an unfunny joke, or watches their parents die, all they can do is laugh. We see that Tama, along with a subset of the population of Wano,')
        print('were fed a batch of SMILEs after begging for food, with Kaido\'s suboordinates knowingly giving them a defective batch. After hearing her backstory, Luffy')
        print('immediately attacked Kaido, but proving to be far too weak, he almost dies and is sent to a labor camp.\n')
        
        print('Upon becoming a prisoner, Luffy learns about Wano\'s interpretation of Haki, as they developed a method called "Ryou". Meaning flow, Ryou involved')
        print('the transfer of Haki within a user\'s body in a precise way to make its use more potent. There are two applications of Ryou, the first being the ability')
        print('to project Haki from the user\'s body. This lets users hit their targets with Haki without touching them, making it more of a projectile. The')
        print('second use is the ability to destroy objects from the inside when grabbing them. The time Luffy spends in this prison serves as a mini training arc,')
        print('as well as showing his ability to piece back together the broken spirits of the Land of Wano, inspiring a breakout of the prison amongst the soldiers.')
        print('With new powers under his belt, Luffy vows to Otama to make the Land of Wano a place where "my friends can eat all the food they want", and to take down Kaido.')
        print('Momonosuke overcomes his fears and declares to Wano that he is the new Shogun, and with the help of Ninja-Pirate-Mink-Samurai Alliance, Wano will be free.\n')    
        
        print('As the raid begins, Luffy moves his fight with Kaido to the roof and the rest of the alliance stay inside the capital of Wano, Onigashima, fighting Kaido\'s')
        print('suboordinates. While the battle is much closer this time, Luffy is bested once more, as the Five Elders were panicked about an outcome of their battle,')
        print('sending one of their most powerful agents to interfere with the fight, causing Luffy to seemingly die mid-clash. The true nature of Luffy\'s Devil Fruit begins')
        print('to unveil itself, as the Five Elders thought it better for Kaido to win and give them trouble rather than deal with Luffy\'s true power. We see Luffy\'s heartbeat')
        print('begin to start again, this time to the rhythm of Drums. The Drums resemble the baseline of Luffy\'s battle theme, and match the rhythm of the War Drums')
        print('we hear as far back as Skypiea.\n')
        
        print('Zunesha, the elephant carrying the town of Zou, is drawn closer to Wano by something. As Luffy\'s heart begins to play its tune, Zunesha exclaims to Momonosuke:\n')
        print('"Momonosuke...I can hear them, I can hear the Drums of Liberation! For the first time in 800 years...Joy Boy... has returned!"\n')
        
        print('As Luffy finally jolts back awake, the Five Elders describe that the Gomu-Gomu Fruit Luffy was believed to have eaten was the object of the World Government\'s')
        print('pursuit for centuries. The actual fruit Luffy had stolen and eaten from Shanks was the Mythical Zoan Human-Human Fruit, Model Nika. The fruit is said')
        print('to have hidden its true nature and purposefully evaded the World Government, giving it the title of a God. More specifically, the fruit embodies')
        print('the Warrior of Liberation, Sun God Nika. While Nika and Joy Boy were two seperate entities, Zunesha seemingly confirms that Joy Boy, or at least the')
        print('spirit of him, lives on in Luffy, further solidifying Luffy\'s status as an important historical character.')
        
        print('With the freedom to bend reality to his will, Luffy is able to best Kaido and liberate the land of Wano through Gear 5, a form that gets stronger')
        print('with the more fun Luffy is having. A battle of titans suddenly turns into an adaptation of Looney Toons in an instant, and the most fearsome creature')
        print('in the world is turned into a joke for the audience. The achievement of this form allows the reliable whimsicality of Luffy to become a symbol,')
        print('and shows that in a world surpressed by the World Government\'s shadow, Luffy will be the new dawn that shines on them as he does to Wano, making')
        print('people laugh while granting them freedom.\n')
                
                
    else:
        
        print('\nNot a valid input.\n')

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
        
        # a quote returner? maybe using the arc sorting tool we can return quotes from a certain arc
        
        # function 7 has made this longer than it should be tbh, might not be much need to add anything else
        
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
