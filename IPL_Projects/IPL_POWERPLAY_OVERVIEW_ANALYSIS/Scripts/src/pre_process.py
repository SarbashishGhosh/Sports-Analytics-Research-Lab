import pandas as pd
import matplotlib.pyplot as plt
from data_loader import deliveries,matches

def create_pp_model(deliveries,matches):
    powerplay_data=deliveries[deliveries['over']<=6].copy()
    powerplay_data.head()
    powerplay_data['total_runs']=powerplay_data['batsman_runs']+powerplay_data['extra_runs']
    powerplay_data.shape
    powerplay_data['over'].unique()
    
    runs_per_over=powerplay_data.groupby('over')['total_runs'].mean()

  ##Visualization of Wickets and runs 
  
    runs_per_over.plot(kind='bar')
    plt.title("Average Runs Per Over in Poweplay")
    plt.xlabel("Over")
    plt.ylabel("Runs")
    plt.show()

    wickets=powerplay_data[powerplay_data['is_wicket']==1]
    wickets_per_over=wickets.groupby('over').size()
    wickets_per_over.plot(kind='bar')
    plt.title("Wickets per Over in Powerplay")
    plt.xlabel("Over")
    plt.ylabel("No. Of Wickets Per Over")
    plt.show()

    pp_over=powerplay_data.groupby(['match_id','inning','over']).agg({
    'total_runs':'sum',
    'is_wicket':'sum'
}).reset_index()

    pp_over.head()
    pp_over=pp_over.merge(matches[['id','venue','team1','team2']],
    left_on='match_id',right_on='id')
    pp_over.head()

    ## venue
    pp_over['venue']=pp_over['venue'].str.replace(',.*',' ',regex=True)
    pp_over['venue_original']=pp_over['venue']

    ### Batting team
    pp_over['batting_team']=pp_over.apply(
    lambda row:row['team2'] if row['inning']==1 else row['team1'],
    axis=1
)
    ### Bowling team
    pp_over['bowling_team']=pp_over.apply(
    lambda row:row['team1'] if row['inning']==1 else row['team2'],
    axis=1
)
    ## overs
    pp_over['over_phase']=pp_over['over'].apply(
    lambda x:'early' if x<=2  else('middle' if x<=4 else'late')


)

    ##Encoding
    
    pp_model=pd.get_dummies(pp_over,columns=['venue','batting_team','bowling_team','over_phase'],drop_first=True)

    return pp_model




