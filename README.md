# YahooMovieRecommendationSystem
透過爬蟲抓取Yahoo電影網站的評論，經過情感分析後，去進行電影推薦  
1.先透過MovieInformationCrawler進行爬蟲，將電影的名稱、評論以及評分抓下來  
2.接著由SentimentAnalysis進行情感分析，將情感分析分數結合電影評分成一個綜合分數，留下綜合分數較高的評論當作正面評論  
3.最後透過RecommendationSystem對正面評論去計算相似度，接著進行電影推薦  
