"""
Agents Package
==============
Contains all 4 specialized agents for the multi-agent system.
"""

from .agent1_retrieval import ProductRetrievalAgent
from .agent2_Sentiment import SentimentAgent
from .agent3_QA import QAAgent
from .agent4_recommendation import RecommendationAgent

__all__ = [
    'ProductRetrievalAgent',
    'SentimentAgent',
    'QAAgent',
    'RecommendationAgent'
]