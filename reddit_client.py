"""
Reddit API Client Module
Handles interactions with the Reddit API, including authentication and data retrieval
"""

import praw
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from tqdm import tqdm
import time


class RedditClient:
    """Reddit API client class"""
    
    def __init__(self, config):
        """
        Initialize Reddit client
        
        Args:
            config: Configuration object containing API credentials
        """
        self.config = config
        self.reddit = self._authenticate()
        # API rate limit: max 60 requests per minute
        self.rate_limit = 60
        self.requests_made = 0
        self.rate_limit_start = time.time()
    
    def _authenticate(self):
        """
        Authenticate using OAuth2
        
        Returns:
            praw.Reddit: Authenticated Reddit instance
        """
        try:
            reddit = praw.Reddit(
                client_id=self.config.client_id,
                client_secret=self.config.client_secret,
                user_agent=self.config.user_agent
            )
            # Test connection
            reddit.user.me()
            print(f"✓ Successfully connected to Reddit API")
            return reddit
        except Exception as e:
            # If unable to authenticate as user, use read-only mode
            try:
                reddit = praw.Reddit(
                    client_id=self.config.client_id,
                    client_secret=self.config.client_secret,
                    user_agent=self.config.user_agent
                )
                print(f"✓ Connected to Reddit API in read-only mode")
                return reddit
            except Exception as e:
                raise Exception(f"Unable to connect to Reddit API: {str(e)}")
    
    def _check_rate_limit(self):
        """
        Check and respect API rate limits
        Pauses execution if rate limit is exceeded until the rate window resets
        """
        self.requests_made += 1
        
        # Check if rate limit exceeded
        if self.requests_made >= self.rate_limit:
            elapsed = time.time() - self.rate_limit_start
            if elapsed < 60:
                # Wait until 60-second window ends
                wait_time = 60 - elapsed
                print(f"⏳ Rate limit reached, waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
            
            # Reset counter
            self.requests_made = 0
            self.rate_limit_start = time.time()
    
    def search_posts(
        self,
        keyword: str,
        subreddit: str = "all",
        limit: int = 100,
        timeframe: str = "all",
        sort: str = "relevance"
    ) -> List[Dict]:
        """
        Search for posts by keyword
        
        Args:
            keyword: Search keyword
            subreddit: Subreddit to search (default: "all")
            limit: Maximum number of results to return
            timeframe: Time range (all, day, week, month, year)
            sort: Sort method (relevance, hot, top, new, comments)
        
        Returns:
            List of dictionaries containing post data
        """
        print(f"🔍 Searching for keyword: '{keyword}' in r/{subreddit}")
        
        results = []
        subreddit_obj = self.reddit.subreddit(subreddit)
        
        # Execute search
        try:
            search_results = subreddit_obj.search(
                keyword,
                sort=sort,
                time_filter=timeframe,
                limit=limit
            )
            
            # Collect results
            for post in tqdm(search_results, desc="Fetching posts", unit="post"):
                self._check_rate_limit()
                
                post_data = {
                    'id': post.id,
                    'title': post.title,
                    'author': str(post.author) if post.author else '[deleted]',
                    'subreddit': str(post.subreddit),
                    'score': post.score,
                    'upvote_ratio': post.upvote_ratio,
                    'num_comments': post.num_comments,
                    'created_utc': datetime.fromtimestamp(post.created_utc),
                    'url': post.url,
                    'permalink': f"https://reddit.com{post.permalink}",
                    'selftext': post.selftext[:500] if post.selftext else '',  # Limit text length
                }
                results.append(post_data)
            
            print(f"✓ Found {len(results)} posts")
            return results
            
        except Exception as e:
            print(f"✗ Error during search: {str(e)}")
            return []
    
    def get_post_comments(self, post_id: str, limit: int = 100) -> List[Dict]:
        """
        Get comments for a specific post
        
        Args:
            post_id: Post ID
            limit: Number of comments to retrieve
        
        Returns:
            List of dictionaries containing comment data
        """
        comments = []
        
        try:
            submission = self.reddit.submission(id=post_id)
            submission.comments.replace_more(limit=0)  # Remove "more comments" links
            
            for comment in submission.comments.list()[:limit]:
                self._check_rate_limit()
                
                comment_data = {
                    'id': comment.id,
                    'author': str(comment.author) if comment.author else '[deleted]',
                    'body': comment.body[:500],  # Limit text length
                    'score': comment.score,
                    'created_utc': datetime.fromtimestamp(comment.created_utc),
                    'parent_id': comment.parent_id,
                }
                comments.append(comment_data)
            
            return comments
            
        except Exception as e:
            print(f"✗ Error retrieving comments: {str(e)}")
            return []
    
    def get_subreddit_info(self, subreddit_name: str) -> Optional[Dict]:
        """
        Get basic information about a subreddit
        
        Args:
            subreddit_name: Subreddit name
        
        Returns:
            Dictionary containing subreddit information
        """
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            self._check_rate_limit()
            
            return {
                'name': subreddit.display_name,
                'title': subreddit.title,
                'description': subreddit.public_description,
                'subscribers': subreddit.subscribers,
                'created_utc': datetime.fromtimestamp(subreddit.created_utc),
                'url': f"https://reddit.com/r/{subreddit_name}"
            }
            
        except Exception as e:
            print(f"✗ Error retrieving subreddit info: {str(e)}")
            return None
    
    def search_multiple_subreddits(
        self,
        keyword: str,
        subreddits: List[str],
        limit_per_sub: int = 50,
        timeframe: str = "all"
    ) -> Dict[str, List[Dict]]:
        """
        Search for keyword across multiple subreddits
        
        Args:
            keyword: Search keyword
            subreddits: List of subreddit names
            limit_per_sub: Result limit per subreddit
            timeframe: Time range
        
        Returns:
            Dictionary with subreddit names as keys and post lists as values
        """
        results = {}
        
        for subreddit_name in subreddits:
            print(f"\n--- Searching r/{subreddit_name} ---")
            posts = self.search_posts(
                keyword=keyword,
                subreddit=subreddit_name,
                limit=limit_per_sub,
                timeframe=timeframe
            )
            results[subreddit_name] = posts
            time.sleep(1)  # Add small delay between requests
        
        return results
