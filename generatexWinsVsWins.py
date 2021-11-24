from espn_api.football import League # need to install this package: https://github.com/cwendt94/espn-api
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cbook import get_sample_data
import seaborn as sns   
from datetime import date

# espn_s2_ = "<espn2 for private league here>"
# swid_ = "swid for private league here>"

leagueId_ = 57118993 # Use your LeagueId here!
year_ = 2021 #Use season year

league = League(league_id=leagueId_, year=year_, debug=False)

# Uncomment below for private league (you will need correct espn_s2 and swid
# values from cookies"
# league = League(league_id=leagueId_, year=year_, espn_s2= espn_s2_, swid=swid_, debug=False)


owners = [team.owner.title() for team in league.teams]
teamsToData = {team: dict({"xWins": 0, "Wins": 0, "Points": 0, "xPoints": 0}) for team in league.teams}

for i in range(1, league.current_week):
    scoreboard = league.scoreboard(i)

    week_scores = []
    for matchup in scoreboard:
        week_scores.append((matchup.away_score, matchup.away_team))
        week_scores.append((matchup.home_score, matchup.home_team))
        if matchup.away_score > matchup.home_score:
            teamsToData[matchup.away_team]['Wins'] += 1
        elif matchup.home_score > matchup.away_score:
            teamsToData[matchup.home_team]['Wins'] += 1
        else:
            teamsToData[matchup.away_team]['Wins'] += .5
            teamsToData[matchup.home_team]['Wins'] += .5

    week_scores.sort(key=lambda x: x[0])


    # Compute PointsFor Rank in a given week
    N = len(week_scores)
    for j in range(len(week_scores)):
        score = week_scores[j]
        teamsToData[score[1]]['xWins'] += j / (N-1)




####### Make the plot ###########
NUM_COLORS = 12

# Various styling
# plt.style.use('ggplot') #https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html
# plt.style.use('fivethirtyeight')
# plt.style.use('default')
plt.style.use('seaborn-darkgrid')

fig = plt.figure()
ax = plt.subplot(111)

ax.set_prop_cycle('color', sns.color_palette("gist_rainbow", NUM_COLORS)) #gist_rainbow, Set3
ax.set_prop_cycle('color', sns.color_palette("Set3", NUM_COLORS)) #gist_rainbow, Set3


minWins = np.inf
minxWins = np.inf

maxWins = 0
maxxWins = 0

for team in teamsToData.keys():
    data = teamsToData[team]
    ax.scatter(data['Wins'], data['xWins'],  label= team.owner.title(), s=50)
    ax.annotate(team.owner.title(), (data['Wins'], data['xWins']))

    minWins = min(minWins, data['Wins'])
    minxWins = min(minxWins, data['xWins'])
    maxWins = max(maxWins, data['Wins'])
    maxxWins = max(maxxWins, data['xWins'])

ax.plot([0, league.current_week-1], [0, league.current_week-1])


# Shrink current axis's height by 10% on the bottom
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.2,
                 box.width, box.height * 0.8])

# Put a legend below current axis
lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
          fancybox=True, shadow=True, ncol=5)

minVal = min(minWins, minxWins)
maxVal = max(maxWins, maxxWins)
plt.xlim([-.25 + minVal, maxVal + .25])
plt.ylim([-.25 + minVal, maxVal + .25])
plt.xlabel("Wins")
plt.ylabel("xWins")
plt.xticks(range(np.floor(minVal).astype(int), np.ceil(maxVal).astype(int)+1))
plt.title("{} xWins vs Wins by Team".format(league.settings.name))
#plt.show()

plt.savefig("{} xWins vs Wins by Team {}.png".format(league.settings.name,
   date.today().strftime("%b-%d-%Y")), bbox_extra_artists=(lgd,), pad_inches=1.0) 
