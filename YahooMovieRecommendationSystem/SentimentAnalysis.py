from snownlp import SnowNLP as snlp
import pandas as pd

data = 'movie_comments_data.txt'
movie_comment = pd.read_table(data,header=None,sep=' ')
movie_comment.columns = ['movie_name','comments','score']

comment = []
for i in movie_comment['comments']:
    comment.append(i)

comment_sentiment = []
for i in range(len(movie_comment)):
    sentence = movie_comment['comments'][i]
    SentimentScore = snlp(sentence).sentiments
    comment_sentiment.append(round(SentimentScore,3))

CommentDataFrame = pd.DataFrame(comment,columns=['comments'])
ScoreDataFrame = pd.DataFrame(comment_sentiment,columns=['sentiment'])
MergeData = CommentDataFrame.merge(ScoreDataFrame,how='inner', left_index=True, right_index=True)
name = []
for i in range(len(movie_comment)):
    name.append(movie_comment['movie_name'][i])
NameDataFrame = pd.DataFrame(name,columns=['name'])
movie_sentiment = NameDataFrame.merge(MergeData,how='inner', left_index=True, right_index=True)

avgscore = []
for i in range(len(movie_comment)):
    sentimentscore = movie_comment['score'][i]
    sum = sentimentscore*0.2+movie_sentiment['sentiment'][i]
    avgscore.append(sum)
TotalScoreDataFrame = pd.DataFrame(avgscore,columns=['totalscore'])
AllMovieData = movie_sentiment.merge(TotalScoreDataFrame,how='inner',left_index=True,right_index=True)

PositiveReview = []
PositiveMovieName = []
for i in range(len(AllMovieData['totalscore'])):
    if (AllMovieData['totalscore'][i] > 1.4):
        PositiveReview.append(AllMovieData['comments'][i])
        PositiveMovieName.append(AllMovieData['name'][i])
PositiveReviewDataFrame = pd.DataFrame(PositiveReview,columns=['comment'])
PositiveMovieNameDataFrame = pd.DataFrame(PositiveMovieName,columns=['name'])
PositiveMovieData = PositiveMovieNameDataFrame.merge(PositiveReviewDataFrame,how='inner',left_index=True,right_index=True)

PositiveMovieData.to_csv('PositiveReview.txt', sep = ' ', index = False, encoding = 'utf-8')
