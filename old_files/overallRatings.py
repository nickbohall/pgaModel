#from other files
import playerMapping
import tourneyList
import pgaScrape
import pgaMajors
import courseMapping

#Want to be able to put in event, course, & get back player list with SG stats, course history, event history

#INPUTS
tourney = 'us-open'
course = 'Muirfield Village Golf Club'

players = playerMapping.master
tourneys = tourneyList.tourneyListformatted
courses = courseMapping.courseNames()
playerStats = pgaScrape.master
tourneyStats = pgaMajors.tourneyStats(tourney)
courseStats = courseMapping.oneCourse(course, playing = False, minRounds = 1)

# print(playerStats)
# print(tourneyStats)
# print(players)

SGtourneyStats = playerStats.merge(tourneyStats, how = 'left', on = 'player number')
SGtourneyStats = SGtourneyStats[['full name_x', 'TOT average', 'posAvg']]
cols_to_norm = ['TOT average', 'posAvg']
SGtourneyStats[cols_to_norm] = SGtourneyStats[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
SGtourneyStats['combinedAvg'] = SGtourneyStats[cols_to_norm].mean(axis=1, skipna=True)
SGtourneyStats = SGtourneyStats[SGtourneyStats['posAvg'].notna()].sort_values(by = ['combinedAvg'], ascending = False)

print(SGtourneyStats.head(50))
print(tourneyStats.head(50))

#NEED TO CHANGE CUT TO NOT NAN, NO ONE IS GETTING PUNISHED FOR BEING CUT