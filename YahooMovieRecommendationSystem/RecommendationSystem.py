from sentence_transformers import SentenceTransformer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_table('PositiveReview.txt',header=0,sep=' ')
model = SentenceTransformer('paraphrase-xlm-r-multilingual-v1')
comments = data['comment'].tolist()
sentence_embeddings = model.encode(comments)
similarity = cosine_similarity(sentence_embeddings)

data['index'] = [i for i in range(0,len(data))]

def get_title(index):
    return data[data.index == index]["name"].values[0]
def get_index(name):
    return data[data.name == name]["index"].values[0]

name=[]
notOver = True
while(notOver):
    user_movie = input("輸入你所喜愛的電影進行推薦: ")
    recommendations = sorted(list(enumerate(similarity[get_index(user_movie)])), key = lambda x:x[1], reverse = True)
    print("根據你所輸入的電影" + " " + user_movie + " " + "所進行推薦的電影是以下三部: ")
    for i in range(len(data)):
        if get_title(recommendations[i][0]) not in name:
            name.append(get_title(recommendations[i][0]))
    print(name[1],name[2],name[3],sep='\n')
    name.clear()
    decision = input("輸入英文字O繼續進行推薦，輸入英文字X離開推薦系統\n")
    if decision== "X":
        print("感謝您使用電影推薦系統")
        notOver = False