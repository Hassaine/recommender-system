import dash
import pandas as pd
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#print(currentdir)
parentdir = os.path.dirname(currentdir)
#parentdir = os.path.dirname(parentdir)
#os.chdir(currentdir)
# sys.path.append(parentdir)
sys.path.append(parentdir+"\\evaluation")
sys.path.append(parentdir+"\\dataLoader")
#print(sys.path)

from Evaluator import Evaluator
from MovieLens import MovieLens

def LoadMovieLensData():
    ml = MovieLens()
    print("Loading movie ratings...")
    data = ml.loadMovieLensLatestSmall()
    print("\nComputing movie popularity ranks so we can measure novelty later...")
    rankings = ml.getPopularityRanks()
    return (ml,data, rankings)
# Load up common data set for the recommender algorithms
(ml, evaluationData, rankings) = LoadMovieLensData()
evaluator = Evaluator(evaluationData, rankings,doTopN=False)


external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4',
        'crossorigin': 'anonymous'
    }
]

external_scripts = [
    {
        'src': 'https://use.fontawesome.com/releases/v5.0.13/js/solid.js',
        'integrity': 'sha384-tzzSw1/Vo+0N5UhStP3bvwWPq+uvzCMfrN1fEFe+xBmv1C/AtVX5K0uZtmcHitFZ',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://use.fontawesome.com/releases/v5.0.13/js/fontawesome.js',
        'integrity': 'sha384-6OIrr52G08NpOFSZdxxz1xdNSndlD4vdcf/q2myIUVO0VsqaGHJsB0RaBE01VTOY',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://code.jquery.com/jquery-3.3.1.slim.min.js',
        'integrity': 'sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js',
        'integrity': 'sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js',
        'integrity': 'sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm',
        'crossorigin': 'anonymous'
    },
    {
        "src":"https://cdnjs.cloudflare.com/ajax/libs/malihu-custom-scrollbar-plugin/3.1.5/jquery.mCustomScrollbar.concat.min.js"
    }
]

df_movies = pd.read_csv('../dataSource/moviesLen/movies.csv')
df_rating = pd.read_csv('../dataSource/moviesLen/ratings.csv')
app = dash.Dash(__name__, external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)
server = app.server