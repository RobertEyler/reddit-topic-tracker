"""
Data Processing Module
Handles analysis and processing of data retrieved from Reddit
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict
from collections import Counter


class DataProcessor:
    """Data processing class for analyzing Reddit data"""
    
    def __init__(self, posts: List[Dict]):
        """
        Initialize data processor
        
        Args:
            posts: List of post data
        """
        self.posts = posts
        self.df = pd.DataFrame(posts) if posts else pd.DataFrame()
    
    def get_engagement_stats(self) -> Dict:
        """
        Calculate engagement statistics
        
        Returns:
            Dictionary containing various statistical metrics
        """
        if self.df.empty:
            return {
                'total_posts': 0,
                'total_score': 0,
                'total_comments': 0,
                'avg_score': 0,
                'avg_comments': 0,
                'avg_upvote_ratio': 0
            }
        
        stats = {
            'total_posts': len(self.df),
            'total_score': int(self.df['score'].sum()),
            'total_comments': int(self.df['num_comments'].sum()),
            'avg_score': float(self.df['score'].mean()),
            'avg_comments': float(self.df['num_comments'].mean()),
            'avg_upvote_ratio': float(self.df['upvote_ratio'].mean())
        }
        
        return stats
    
    def rank_by_engagement(self, top_n: int = 10) -> pd.DataFrame:
        """
        Rank posts by engagement
        Engagement = score + (num_comments * 2)
        
        Args:
            top_n: Return top N results
        
        Returns:
            Sorted DataFrame
        """
        if self.df.empty:
            return pd.DataFrame()
        
        # Calculate engagement score
        self.df['engagement_score'] = self.df['score'] + (self.df['num_comments'] * 2)
        
        # Sort by engagement
        ranked = self.df.nlargest(top_n, 'engagement_score')
        
        return ranked[['title', 'author', 'subreddit', 'score', 'num_comments', 'engagement_score', 'permalink']]
    
    def get_top_contributors(self, top_n: int = 10) -> List[Dict]:
        """
        Identify users who contribute the most
        
        Args:
            top_n: Return top N users
        
        Returns:
            List of user statistics
        """
        if self.df.empty:
            return []
        
        # Count posts and total score for each author
        author_stats = self.df.groupby('author').agg({
            'id': 'count',
            'score': 'sum',
            'num_comments': 'sum'
        }).rename(columns={'id': 'post_count'})
        
        # Sort and get top N
        top_authors = author_stats.nlargest(top_n, 'post_count')
        
        result = []
        for author, row in top_authors.iterrows():
            result.append({
                'author': author,
                'post_count': int(row['post_count']),
                'total_score': int(row['score']),
                'total_comments': int(row['num_comments'])
            })
        
        return result
    
    def get_subreddit_distribution(self) -> List[Dict]:
        """
        Get distribution of posts across different subreddits
        
        Returns:
            List of subreddit statistics
        """
        if self.df.empty:
            return []
        
        # Count posts in each subreddit
        subreddit_counts = self.df['subreddit'].value_counts()
        
        result = []
        for subreddit, count in subreddit_counts.items():
            subreddit_data = self.df[self.df['subreddit'] == subreddit]
            result.append({
                'subreddit': subreddit,
                'post_count': int(count),
                'avg_score': float(subreddit_data['score'].mean()),
                'avg_comments': float(subreddit_data['num_comments'].mean())
            })
        
        return result
    
    def analyze_trends(self, interval: str = 'day') -> pd.DataFrame:
        """
        Analyze how topic trends change over time
        
        Args:
            interval: Time interval (day, week, month)
        
        Returns:
            Time series DataFrame
        """
        if self.df.empty:
            return pd.DataFrame()
        
        # Ensure created_utc is datetime type
        self.df['created_utc'] = pd.to_datetime(self.df['created_utc'])
        
        # Set grouping frequency based on interval
        freq_map = {
            'day': 'D',
            'week': 'W',
            'month': 'M'
        }
        freq = freq_map.get(interval, 'D')
        
        # Group by time
        self.df['date'] = self.df['created_utc'].dt.floor(freq)
        
        trends = self.df.groupby('date').agg({
            'id': 'count',
            'score': 'sum',
            'num_comments': 'sum'
        }).rename(columns={
            'id': 'post_count',
            'score': 'total_score',
            'num_comments': 'total_comments'
        })
        
        return trends
    
    def get_time_distribution(self) -> Dict:
        """
        Analyze temporal distribution of posts
        
        Returns:
            Dictionary containing time distribution statistics
        """
        if self.df.empty:
            return {}
        
        # Ensure created_utc is datetime type
        self.df['created_utc'] = pd.to_datetime(self.df['created_utc'])
        
        # Group by hour
        self.df['hour'] = self.df['created_utc'].dt.hour
        hour_distribution = self.df['hour'].value_counts().sort_index()
        
        # Group by weekday
        self.df['weekday'] = self.df['created_utc'].dt.day_name()
        weekday_distribution = self.df['weekday'].value_counts()
        
        return {
            'by_hour': hour_distribution.to_dict(),
            'by_weekday': weekday_distribution.to_dict()
        }
    
    def search_in_content(self, keyword: str) -> pd.DataFrame:
        """
        Search for keyword in post titles and content
        
        Args:
            keyword: Search keyword
        
        Returns:
            DataFrame of matching posts
        """
        if self.df.empty:
            return pd.DataFrame()
        
        # Search in titles and content (case insensitive)
        mask = (
            self.df['title'].str.contains(keyword, case=False, na=False) |
            self.df['selftext'].str.contains(keyword, case=False, na=False)
        )
        
        return self.df[mask]
    
    def get_summary(self) -> str:
        """
        Generate data summary report
        
        Returns:
            Formatted summary string
        """
        if self.df.empty:
            return "No data available"
        
        stats = self.get_engagement_stats()
        subreddit_dist = self.get_subreddit_distribution()
        top_contributors = self.get_top_contributors(5)
        
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║                   Data Analysis Summary                      ║
╠══════════════════════════════════════════════════════════════╣
║ Total Posts: {stats['total_posts']:>11}                                     ║
║ Total Score: {stats['total_score']:>11}                                     ║
║ Total Comments: {stats['total_comments']:>8}                                     ║
║ Average Score: {stats['avg_score']:>9.2f}                                     ║
║ Average Comments: {stats['avg_comments']:>6.2f}                                     ║
║ Average Upvote Ratio: {stats['avg_upvote_ratio']:>4.2%}                                     ║
╠══════════════════════════════════════════════════════════════╣
║ Subreddit Distribution (Top 5):                             ║
"""
        
        for i, sub in enumerate(subreddit_dist[:5], 1):
            summary += f"║ {i}. r/{sub['subreddit']:<20} - {sub['post_count']:>3} posts              ║\n"
        
        summary += "╠══════════════════════════════════════════════════════════════╣\n"
        summary += "║ Top Contributors (Top 5):                                    ║\n"
        
        for i, user in enumerate(top_contributors[:5], 1):
            summary += f"║ {i}. u/{user['author']:<20} - {user['post_count']:>3} posts              ║\n"
        
        summary += "╚══════════════════════════════════════════════════════════════╝"
        
        return summary
