
from logging import PlaceHolder
import streamlit as st
import mysql
import sqlalchemy
import plotly
import plotly.io as pio
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import sqlalchemy
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
from termcolor import colored
import warnings
warnings.filterwarnings('ignore')
st.set_page_config(
     layout="wide",
     
 )
years=[2019,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2020]
players=['MS Dhoni', 'V Kohli', 'DJ Bravo', 'Shakib Al Hasan', 'KL Rahul','F du Plessis','KA Pollard','DA Warner','CH Gayle','AB de Villiers']
@st.cache
def load():
 connect = sqlalchemy.create_engine("mysql+mysqlconnector://root:hihellohi@localhost:3307/DEproject")
 connect2 = sqlalchemy.create_engine("mysql+mysqlconnector://root:hihellohi@localhost:3307/DEproject", pool_recycle=3600, pool_pre_ping = True)
 Matches_data = pd.read_sql("select * from iplmatches", connect)
 ball_by_ball = pd.read_sql("select * from balls", connect2)
 return Matches_data,ball_by_ball
Matches_data,ball_by_ball=load()
def question2():
    run_of_each_player={}
    single_match_data = ball_by_ball[ball_by_ball['id']==335986]
    all_batsman=single_match_data['batsman'].unique()
    for player in all_batsman:
     run_of_each_player[player] = sum(single_match_data[single_match_data['batsman']==player]['batsman_runs'])
    run_of_each_player=sorted(run_of_each_player.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    run_of_each_player=pd.DataFrame(run_of_each_player,columns=["Player_name","runs"])
    
    fig2=px.bar(run_of_each_player,y="Player_name",x="runs",color="Player_name")
    fig2.update_xaxes(tickfont_size=15,title="Runs",title_font=dict(size=20,color="Navy"))
    fig2.update_yaxes(tickfont_size=15,title="Player",title_font=dict(size=20,color="Navy"))
    fig2.update_layout(title="KKR vs DC Match Batsman's Stats",
    title_font=dict(size=24,color="Navy"),
    autosize=False,
    width=1000,
    height=500,)
    st.plotly_chart(fig2)
    st.info("DJ Hussey scored the most number of runs in this match")
    df=pd.read_csv("C:/Users/navya/Desktop/DEproject/questions_csv/question2_dismissal.csv")
    
    fig11=go.Figure(data=[go.Table(columnwidth=[140,140],header=dict(values=["Batsman","Dismissal_Type"]),
    cells=dict(height=32,values=[list(df["batsman"].values),list(df["dismissal"].values)]))])
    fig11.update_layout(autosize=False,width=900,height=700,) 
    fig11.update_traces(cells_font=dict(size=15),header_font=dict(size=15))
    st.plotly_chart(fig11)

def question7_batsman(player):
    data = ball_by_ball[ball_by_ball['batsman'] == player]
  
    temp = data.groupby('bowler')['is_wicket'].agg('sum').reset_index().sort_values(by='is_wicket', ascending = False).reset_index(drop=True).head(10)
    fig7=px.bar(temp,x="is_wicket",y="bowler",
                labels={'bowler':"Bowlers","is_wicket":"Number of times wicket taken"},
                color="bowler",color_discrete_sequence=px.colors.qualitative.Set3)
    fig7.update_xaxes(tickfont_size=15,title="Number of Wickets",title_font=dict(size=20,color="Navy"))
    fig7.update_yaxes(tickfont_size=15,title="Bowlers",title_font=dict(size=20,color="Navy"))
    fig7.update_layout(title=f'Top ten bowlers deadly against {player}',
    title_font=dict(size=24,color="Navy"),
    autosize=False,
    width=1000,
    height=500,)
    st.plotly_chart(fig7)
    most_dismissed=temp.loc[0,"bowler"]
    st.info(f"{player} was most dismissed by {most_dismissed}")
def question3():
    single_match_data = ball_by_ball[ball_by_ball['id']==335986]
    bowlers=single_match_data['bowler'].unique()
    players={}
    for player in bowlers:
     bowler_data=single_match_data[single_match_data['bowler']== player]
     bowler_data=bowler_data[(bowler_data['dismissal_kind'] == 'caught')|(bowler_data['dismissal_kind'] == 'bowled')|(bowler_data['dismissal_kind'] == 'lbw')|(bowler_data['dismissal_kind'] == 'stumped')|(bowler_data['dismissal_kind'] == 'caught and bowled')|(bowler_data['dismissal_kind'] == 'hit wicket')]
     players[player] = sum(bowler_data['is_wicket'])
    players=sorted(players.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    #st.write(players)
    players=pd.DataFrame(players,columns=["Player_name","Wickets"])
    #st.dataframe(players)
    fig3=px.bar(players,x="Wickets",y="Player_name",color="Player_name")
    fig3.update_xaxes(tickfont_size=15,title="Wickets",title_font=dict(size=20,color="Navy"))
    fig3.update_yaxes(tickfont_size=15,title="Player",title_font=dict(size=20,color="Navy"))
    fig3.update_layout(title="KKR vs DC Match Bowlers Stats",
    title_font=dict(size=24,color="Navy"),
    autosize=False,
    width=1000,
    height=500,)
    st.plotly_chart(fig3)
    st.info("M Kartik took the most number of wickets in this match")
def question4(season_select):
    Match_data=Matches_data.copy()
    Match_data['season'] = pd.DatetimeIndex(Match_data['date']).year
    year_wise = Match_data[['id', 'season']]
    sea_2019 = year_wise[(year_wise['season'] == season_select)]
    # sea_2019.head()
    id_list = sea_2019['id'].to_list()
    delivery = ball_by_ball[ball_by_ball['id'].isin(id_list)]
    # delivery.head()
    max_run = delivery.groupby(['batsman'])['batsman_runs'].sum()
    max_run.columns = ['batsman', 'total_runs']
    max_run.sort_values(ascending = False, inplace=True)
# top_batsmen = max_run[0:10]
# top_batsmen.insert(0, 'Rank', value = [i for i in range(1,11)])
    top_batsmen = max_run.head(10)
    #top_batsmen=pd.DataFrame({"Player_name":top_batsmen.index,"Total_runs":top_batsmen.values})
    x_label="Total_runs_"+str(season_select)
    top_batsmen=pd.DataFrame({"Player_name":top_batsmen.index,x_label:top_batsmen.values})
    fig4=px.bar(top_batsmen,y="Player_name",x=x_label,color=x_label)
    top_batsman=top_batsmen.loc[0,"Player_name"]
    fig4.update_xaxes(tickfont_size=15,title=x_label,title_font=dict(size=20,color="Navy"))
    fig4.update_yaxes(tickfont_size=15,title="Player",title_font=dict(size=20,color="Navy"))
    fig4.update_layout(title=f"Top 10 Batsman's in {season_select} season",
    title_font=dict(size=24,color="Navy"),
    autosize=False,
    width=1000,
    height=500,)
    st.plotly_chart(fig4)
    st.info(f"{top_batsman} scored most number of runs in {season_select}")
    
def question5(season_select):
    Match_data=Matches_data.copy()
    Match_data['season'] = pd.DatetimeIndex(Match_data['date']).year
    year_wise = Match_data[['id', 'season']]
    sea_2019 = year_wise[(year_wise['season'] == season_select)]
    # sea_2019.head()
    id_list = sea_2019['id'].to_list()
    delivery = ball_by_ball[ball_by_ball['id'].isin(id_list)]
    x = delivery[['bowler','is_wicket','dismissal_kind']]
    x = x[x['dismissal_kind'] != 'run out']
    x = x[x['dismissal_kind'] != 'obstructing the field']
    max_wicket = x.groupby(['bowler'])['is_wicket'].sum()
    max_wicket.columns = ['bowler', 'wickets taken']
    max_wicket.sort_values(ascending = False, inplace=True)
# top_batsmen = max_run[0:10]
# top_batsmen.insert(0, 'Rank', value = [i for i in range(1,11)])
    top_bowler = max_wicket.head(10)
    xlabel="Total_Wickets_"+str(season_select)
    top_bowlers=pd.DataFrame({"Player_name":top_bowler.index,xlabel:top_bowler.values})
    fig5=px.bar(top_bowlers,y="Player_name",x=xlabel,color=xlabel)
    top_bowler=top_bowlers.loc[0,"Player_name"]
    fig5.update_xaxes(tickfont_size=15,title=xlabel,title_font=dict(size=20,color="Navy"))
    fig5.update_yaxes(tickfont_size=15,title="Player",title_font=dict(size=20,color="Navy"))
    fig5.update_layout(title=f"Top 10 Bowlers in {season_select} season",
    title_font=dict(size=24,color="Navy"),
    autosize=False,
    width=1000,
    height=500,)
    st.plotly_chart(fig5)
    st.info(f"{top_bowler} took the most number of wickets in {season_select}")
def question_6():
    match_win = len(Matches_data[(Matches_data['toss_winner'] == Matches_data['winner'])].index)
    match_lost=Matches_data.shape[0]-match_win
    dic={"Number of Matches":[match_win,match_lost],
    "Match_Result":["Match Won","Match Lost"]}
    temp=pd.DataFrame(dic)

    fig6=px.pie(temp,values="Number of Matches",names="Match_Result",color="Match_Result",
    color_discrete_map={"Match Won":"royalblue","Match Lost":"lightcyan"})
    
    fig6.update_traces(
    hoverinfo="label+percent",
    textinfo="percent+label",
    textfont_size=25
    )
    fig6.update_layout(title="After winning toss, % Victory",title_font=dict(size=27,color="Navy"),
    autosize=False,
    width=900,
    height=590,)
    st.plotly_chart(fig6)
    
    st.info("Winning Toss , increases chance of Victory")

def most_wins_ipl():
    temp = pd.DataFrame(Matches_data["winner"])
    count_wins = temp.value_counts() 
    count_wins=pd.DataFrame(count_wins).reset_index()
    count_wins.columns=["Team","Wins"]
    fig_wins=px.bar(count_wins,x="Wins",y="Team",color="Wins")
    fig_wins.update_xaxes(tickfont_size=15,title="Wins",title_font=dict(size=20,color="Navy"))
    fig_wins.update_yaxes(tickfont_size=15,title="Team",title_font=dict(size=20,color="Navy"))
    fig_wins.update_layout(title="Most Wins in IPL",
    title_font=dict(size=27,color="Navy"),
    autosize=False,
    width=1000,
    height=500,)
    st.plotly_chart(fig_wins)
    st.info("Mumbai Indians won most number of matches")
def most_wins_eliminator():
    temp=pd.DataFrame(Matches_data["winner"][Matches_data["eliminator"]=="Y"])
    count_wins = temp.value_counts() 
    count_wins=pd.DataFrame(count_wins).reset_index()
    count_wins.columns=["Team","Wins_Eliminator"]
    fig_wins_eliminator=px.bar(count_wins,x="Wins_Eliminator",y="Team",color="Wins_Eliminator")
    fig_wins_eliminator.update_xaxes(tickfont_size=15,title="Wins_Eliminator",title_font=dict(size=20,color="Navy"))
    fig_wins_eliminator.update_yaxes(tickfont_size=15,title="Team",title_font=dict(size=20,color="Navy"))
    fig_wins_eliminator.update_layout(title="Most Wins in Eliminator",
    title_font=dict(size=27,color="Navy"),
    autosize=False,
    width=1000,
    height=500,)
    fig_wins_eliminator.update_layout(
    autosize=False,
    width=1000,
    height=500,)
    st.plotly_chart(fig_wins_eliminator)
    st.info("Kings XI Punjab won most number of Eliminator Matches")

def question1(team,plot1):
    
    team_frame=plot1[plot1["team"]==team]
    colors=["cyan","#F3A0F2","#47DBCD","#F5814C","#9D2EC5"]
    team_frame=team_frame.groupby(['stadium',"season"])["wins"].sum().groupby(level=0).cumsum().reset_index()
    years=[2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
    dict_keys=["2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020"]
    n_frame={}
    for y,d in zip(years,dict_keys):
        dataframe=team_frame[team_frame["season"]==y]
        dataframe=dataframe.nlargest(n=5,columns=["wins"])
        dataframe=dataframe.sort_values(by=["season","wins"])
        n_frame[d]=dataframe
    for i in dict_keys:
      n_frame[i]["color_code"]=colors
    fig = go.Figure(
    data=[
        go.Bar(
        x=n_frame['2008']['wins'], y=n_frame['2008']['stadium'],orientation='h',
        text=n_frame['2008']['wins'],
        textfont={'size':18}, textposition='inside', insidetextanchor='middle',
        width=0.9, marker={'color':n_frame['2008']["color_code"]})
    ],
    layout=go.Layout(
        xaxis=dict(range=[0, 60], autorange=False, title=dict(text='wins',font=dict(size=18))),
        yaxis=dict(range=[-0.5, 5.5], autorange=False,tickfont=dict(size=14)),
        title=dict(text='Number of Wins in Stadiums till 2008',font=dict(size=22,color="Navy"),x=0.5,xanchor='center'),
        # Add button
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          
                          method="animate",
                          
                          args=[None]
                          #{"frame": {"duration": 500,"redraw":True},
                          #"transition": {"duration":125,"easing":"linear"
                          #}}]
            )]
        )]
    ),
    frames=[
            go.Frame(
                data=[
                        go.Bar(x=value['wins'], y=value['stadium'],
                        orientation='h',text=value['wins'],
                        marker={'color':value['color_code']})
                    ],
                layout=go.Layout(
                        xaxis=dict(range=[0, 60], autorange=False),
                        yaxis=dict(range=[-0.5,5.5], autorange=False,tickfont=dict(size=14)),
                        title=dict(text='Number of Wins in Stadiums till '+str(value['season'].values[0]),
                        font=dict(size=22,color="Navy"))
                    )
            )
        for key, value in n_frame.items()
    ] 
    )
    fig.update_layout(autosize=False,width=800,height=600,)
    
    st.plotly_chart(fig)
    match_data=Matches_data.copy()
    team_names=match_data['winner'].unique()
    match_data["season"]=pd.DatetimeIndex(match_data["date"]).year
    req_data=pd.DataFrame(match_data[["venue","winner"]])
    new_data=req_data.groupby(by="venue")
    all_teams=list(req_data["winner"].unique())
    my_dic = dict.fromkeys(all_teams)
    del all_teams[10]
    table_frame=pd.DataFrame(columns={"Stadium with Maximum wins","Team_name"})
    table_frame=table_frame[["Team_name","Stadium with Maximum wins"]]
    team_names=[]
    stadiums=[]
    for each_team in all_teams:
     ap = req_data[req_data['winner'] == each_team]
     win_stadium = ap.groupby('venue').count()
     stadium = win_stadium['winner'].idxmax()
     team_names.append(each_team)
     stadiums.append(stadium)
    idx=team_names.index(team)
    st.info(f"{team} won most matches in {stadiums[idx]}")
    fig11=go.Figure(data=[go.Table(columnwidth=[140,140],header=dict(values=["Team_name","Stadium with Maximum wins"]),cells=dict(height=30,values=[team_names,stadiums]))])
    fig11.update_layout(autosize=False,width=900,height=700,) 
    fig11.update_traces(cells_font=dict(size=15),header_font=dict(size=15))
    st.plotly_chart(fig11)

def dash():
 plot1=pd.read_csv("C:/Users/navya/Desktop/DEproject/questions_csv/plot1.csv")
 dash_title='<p style="color:Teal;font-size: 26px;"><b>IPL Dashboard</b></p>'
 st.sidebar.markdown(dash_title,unsafe_allow_html=True)
 option_title='<p style="color:SlateGrey;font-size: 23px;">Which Dashboard?</p>'
 
 option=st.sidebar.selectbox("Which Dashboard?",("Team Stats","Batsman's Stats ","Bowlers Stats"))
 if option=="Team Stats":
        Teamstats='<p style="color:Teal;font-size: 25px;"><b>Team Stats</b></p>'
        st.markdown(Teamstats,unsafe_allow_html=True)
        teams=plot1["team"].unique().tolist()
        team_stats_option=st.sidebar.selectbox("Which Team Stats?",
        ("Team vs Most wins in stadium","Winning toss vs Victory","Most Wins in IPL","Most Wins in Eliminator") )
       
        if team_stats_option == "Team vs Most wins in stadium":
         team_select=st.selectbox("Select the Team",teams)
         question1(team_select,plot1)
        elif team_stats_option=="Winning toss vs Victory":
         question_6()
        elif team_stats_option=="Most Wins in IPL":
         most_wins_ipl()
        elif team_stats_option=="Most Wins in Eliminator":
            most_wins_eliminator()
 elif option=="Batsman's Stats ":

        batsman_stats_option=st.sidebar.selectbox("Which Stats?",
        ("KKR vs DC Match Stats","Most Runs in Seasons","Batsman vs Most Dismissed By") )
        stats='<p style="color:Teal;font-size: 25px;"><b>Batsman Stats </b></p>'
        st.markdown(stats,unsafe_allow_html=True)
        if batsman_stats_option=="KKR vs DC Match Stats":
            question2()
        elif batsman_stats_option=="Most Runs in Seasons":
          season_select=st.selectbox("Select the season",years)
          question4(season_select)
        elif batsman_stats_option=="Batsman vs Most Dismissed By":
            player_select=st.selectbox("Select the Batsman",players)
            question7_batsman(player_select)
 elif option=="Bowlers Stats":
        stats='<p style="color:Teal;font-size: 25px;"><b>Bowlers Stats </b></p>'
        st.markdown(stats,unsafe_allow_html=True)
        bowler_stats_option=st.sidebar.selectbox("Which Stats?",("KKR vs DC Match Stats","Most Wickets in Seasons"))
        if bowler_stats_option=="KKR vs DC Match Stats":
            question3()
        elif bowler_stats_option=="Most Wickets in Seasons":
          season_select=st.selectbox("Select the season",years)
          question5(season_select)
 st.sidebar.button("Logout",on_click=shutdown)
def shutdown():
    for k in st.session_state.keys():
        del st.session_state[k]

  
if "dashh" not in st.session_state:
    st.session_state["dashh"]=False       


if "key" not in st.session_state:
    st.session_state["key"]=True
connect3 = sqlalchemy.create_engine("mysql+mysqlconnector://root:hihellohi@localhost:3307/DEproject")
connection=connect3.raw_connection()
c3=connection.cursor()
def dash_cal():
    st.session_state["dashh"]=True
    st.session_state["key"]=False
def create_usertable():
 c3.execute("create table if not exists usertable(username varchar(20) not null, password varchar(20) not null,primary key(username))")
def add_userdata(username,password):
    flag=False
    try:
     c3.execute("insert into usertable(username,password) values(%s,%s)",(username,password))
    except mysql.connector.IntegrityError:
        st.sidebar.error("Account hasn't created , Choose Some Other Username")
    else:
     flag= True
     connection.commit()
     return flag
def login_user(username,password):
    c3.execute("select * from usertable where username =%s and password =%s",(username,password))
    data=c3.fetchall()
    return data
def view_all_users():
    c3.execute("select * from usertable")
    data=c3.fetchall()
    return data
from streamlit.legacy_caching.caching import maybe_show_cached_st_function_warning
def login():
 main_title="<h3 style='text-align:center ;font-size:24px;color :navy;background-color:#D6DBDE;'><b>IPL DASHBOARD</b></h3>"
 st.sidebar.markdown(main_title,unsafe_allow_html=True)
 st.sidebar.write("")
 st.markdown("<h3 style='text-align:center ;font-size:22px;color :navy;background-color:whitesmoke;'><b>DASHBOARD HIGHLIGHTS</b></h3>",unsafe_allow_html=True)
 st.write(" ")
 st.markdown("**You can see the following Statistics in Dashboard!!**")
 st.markdown("<h3 style='font-size:22px;color :navy;'><b><u>Team Statistics</u></b></h3>",unsafe_allow_html=True)
 st.markdown("**i)You can select a team to see in which stadium, team won maximum matches and a table listing all teams with a stadium name where team won maximum matches.**")
 st.markdown("**ii)Does winning toss increases the chance of winning the match??**🤔**Check then to get the answer.**")
 st.markdown("**iii)Do you know which team won maximum number of IPL matches??If no,See most wins in ipl stats.**")
 st.markdown("**iv) Most Wins in Eliminator matches by teams stats is also there!!**")
 st.markdown("<h3 style='font-size:22px;color :navy;'><b><u>Batsman's Statistics</u></b></h3>",unsafe_allow_html=True)
 st.markdown("**i)You can see KKR vs DC Batsman's Stats where the match was held on 20-04-2008**")
 st.markdown("**ii)Want to know who were top 10 batsman in each season??Then,Check Most Runs in Seasons Stats**")
 st.markdown("**iii)Select a batsman to know with which bolwers he was most dismissed in Batsman vs Most Dismissed by Stats**")
 st.markdown("<h3 style='font-size:22px;color :navy;'><b><u>Bowler's Statistics</u></b></h3>",unsafe_allow_html=True)
 st.markdown("**i)You can see KKR vs DC Bowler's Stats where the match was held on 20-04-2008**")
 st.markdown("**ii)Want to know who were top 10 bowlers in each season??Then,Check Most wickets in Seasons Stats**")
 st.info("👈Go to Login Dropdown to view DashBoard🥳")
 #st.title("Login app")
 menu=["Login","Signup"]
 choice=st.sidebar.selectbox("Login/Signup",menu)
 if choice == "Login":
#st.subheader("login")
     place1=st.sidebar.empty()
     username= place1.text_input(label="Enter User Name")
     place2=st.sidebar.empty()
     password=place2.text_input(label="Enter Your Password",type="password")
     login=st.sidebar.button(label="Login",key=1)

     if login:
        user_name=username
        create_usertable()
        result=login_user(username,password)
        password=place2.text_input(label="Enter Your Password",type="password",key=1,value="")
        username=place1.text_input(label="Enter User Name",value="",key=1)
        #username=st.sidebar.placeholder.text_input()
        if result:
         
         st.sidebar.success(f"Logged in as {user_name} ")
         st.sidebar.button("View DashBoard ",on_click=dash_cal)
        else:
            st.sidebar.warning("Incorrect Username/Password")
 elif choice== "Signup":
#st.subheader("signup")
    place3=st.sidebar.empty()
    place4=st.sidebar.empty()
    new_user=place3.text_input(label="Username")
    new_password=place4.text_input("Password",type="password")
    if st.sidebar.button(label="Signup",key=2):
        create_usertable()
        if(add_userdata(new_user,new_password)):
         new_user=place3.text_input(label="Username",key=2,value="")
         new_password=place4.text_input("Password",type="password",key=2,value="")
         st.sidebar.success("You have successfully created an Account")
         st.sidebar.info("Go to Login/Signup to login")

if st.session_state["key"]:
 login()
if st.session_state["dashh"]:
    dash()