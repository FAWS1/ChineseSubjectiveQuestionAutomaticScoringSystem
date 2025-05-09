"""评分系统配置"""

# 相似度评分权重配置
SIMILARITY_WEIGHTS = {
    'bert': 0.6,  # BERT相似度权重
    'tfidf': 0.4,  # TF-IDF相似度权重
}

# 相似度分数映射配置
SIMILARITY_SCORE_MAPPING = {
    0.9: 100,  # 相似度>=0.9，得分100
    0.8: 90,   # 相似度>=0.8，得分90
    0.7: 80,   # 相似度>=0.7，得分80
    0.6: 70,   # 相似度>=0.6，得分70
    0.5: 60,   # 相似度>=0.5，得分60
    0.0: 0,    # 相似度<0.5，得分0
}