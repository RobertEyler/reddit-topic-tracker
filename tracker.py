"""
Reddit Topic Tracker - Main Program
For tracking and analyzing topic trends on Reddit
"""

import argparse
import sys
from datetime import datetime

from config import get_config
from reddit_client import RedditClient
from data_processor import DataProcessor
from exporter import Exporter


def print_banner():
    """Print program banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              Reddit Topic Tracker                            ║
║                                                              ║
║       Track and analyze topic trends on Reddit               ║
║       Version: 1.0                                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def parse_arguments():
    """
    Parse command line arguments
    
    Returns:
        Parsed arguments object
    """
    parser = argparse.ArgumentParser(
        description='Reddit Topic Tracker - Search and analyze Reddit topics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  # Basic search
  python tracker.py --keyword "artificial intelligence" --subreddit "MachineLearning"
  
  # Search across multiple subreddits
  python tracker.py --keyword "climate change" --subreddit "science,environment,climate"
  
  # Trend analysis
  python tracker.py --keyword "gaming" --timeframe week --trends day
  
  # Export data
  python tracker.py --keyword "programming" --export csv
  python tracker.py --keyword "programming" --export json
  python tracker.py --keyword "programming" --export both
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--keyword', '-k',
        type=str,
        required=True,
        help='Keyword or phrase to search for'
    )
    
    # Optional arguments
    parser.add_argument(
        '--subreddit', '-s',
        type=str,
        default='all',
        help='Subreddit to search (comma-separated for multiple, default: all)'
    )
    
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=100,
        help='Maximum number of posts to return per subreddit (default: 100）'
    )
    
    parser.add_argument(
        '--timeframe', '-t',
        type=str,
        choices=['hour', 'day', 'week', 'month', 'year', 'all'],
        default='all',
        help='Time range for search (default: all)'
    )
    
    parser.add_argument(
        '--sort',
        type=str,
        choices=['relevance', 'hot', 'top', 'new', 'comments'],
        default='relevance',
        help='Sort method for results (default: relevance)'
    )
    
    parser.add_argument(
        '--export', '-e',
        type=str,
        choices=['csv', 'json', 'both'],
        help='Export data format (csv, json, or both)'
    )
    
    parser.add_argument(
        '--trends',
        type=str,
        choices=['day', 'week', 'month'],
        help='Time interval for trend analysis'
    )
    
    parser.add_argument(
        '--top', '-n',
        type=int,
        default=10,
        help='Display top N results (default: 10)'
    )
    
    parser.add_argument(
        '--no-summary',
        action='store_true',
        help='Do not display summary information'
    )
    
    return parser.parse_args()


def display_top_posts(processor: DataProcessor, top_n: int = 10):
    """
    Display posts with highest engagement
    
    Args:
        processor: Data processor instance
        top_n: Display top N posts
    """
    print("\n" + "="*60)
    print(f"📊 Top {top_n} Posts by Engagement")
    print("="*60)
    
    top_posts = processor.rank_by_engagement(top_n)
    
    if top_posts.empty:
        print("No posts found.")
        return
    
    for idx, row in enumerate(top_posts.iterrows(), 1):
        post = row[1]
        print(f"\n#{idx}. {post['title'][:70]}{'...' if len(post['title']) > 70 else ''}")
        print(f"   Author: u/{post['author']} | Subreddit: r/{post['subreddit']}")
        print(f"   Score: {post['score']} | Comments: {post['num_comments']} | Engagement: {post['engagement_score']}")
        print(f"   Link: {post['permalink']}")


def display_subreddit_distribution(processor: DataProcessor):
    """
    Display subreddit distribution
    
    Args:
        processor: Data processor instance
    """
    print("\n" + "="*60)
    print("🌐 Subreddit Distribution")
    print("="*60)
    
    distribution = processor.get_subreddit_distribution()
    
    if not distribution:
        print("No data available.")
        return
    
    for idx, sub in enumerate(distribution, 1):
        print(f"{idx}. r/{sub['subreddit']}")
        print(f"   Posts: {sub['post_count']} | Avg Score: {sub['avg_score']:.1f} | Avg Comments: {sub['avg_comments']:.1f}")


def display_top_contributors(processor: DataProcessor, top_n: int = 10):
    """
    Display top contributors
    
    Args:
        processor: Data processor instance
        top_n: Display top N contributors
    """
    print("\n" + "="*60)
    print(f"👥 Top Contributors (Top {top_n})")
    print("="*60)
    
    contributors = processor.get_top_contributors(top_n)
    
    if not contributors:
        print("No data available.")
        return
    
    for idx, user in enumerate(contributors, 1):
        print(f"{idx}. u/{user['author']}")
        print(f"   Posts: {user['post_count']} | Total Score: {user['total_score']} | Total Comments: {user['total_comments']}")


def display_trends(processor: DataProcessor, interval: str = 'day'):
    """
    Display trend analysis
    
    Args:
        processor: Data processor instance
        interval: Time interval
    """
    print("\n" + "="*60)
    print(f"📈 Topic Trend Analysis (by {interval})")
    print("="*60)
    
    trends = processor.analyze_trends(interval)
    
    if trends.empty:
        print("Not enough data for trend analysis.")
        return
    
    print(trends.to_string())
    
    return trends


def main():
    """Main function"""
    print_banner()
    
    # Parse command line arguments
    args = parse_arguments()
    
    try:
        # Load configuration
        print("🔧 Loading configuration...")
        config = get_config()
        
        # Initialize Reddit client
        print("🔌 Connecting to Reddit API...")
        client = RedditClient(config)
        
        # Parse subreddit list
        subreddits = [s.strip() for s in args.subreddit.split(',')]
        
        # Search posts
        if len(subreddits) == 1:
            # Single subreddit
            posts = client.search_posts(
                keyword=args.keyword,
                subreddit=subreddits[0],
                limit=args.limit,
                timeframe=args.timeframe,
                sort=args.sort
            )
        else:
            # Multiple subreddits
            results = client.search_multiple_subreddits(
                keyword=args.keyword,
                subreddits=subreddits,
                limit_per_sub=args.limit,
                timeframe=args.timeframe
            )
            # Merge all results
            posts = []
            for sub_posts in results.values():
                posts.extend(sub_posts)
        
        if not posts:
            print("\n⚠ No matching posts found.")
            sys.exit(0)
        
        # Initialize data processor
        processor = DataProcessor(posts)
        
        # Display summary (unless disabled)
        if not args.no_summary:
            summary = processor.get_summary()
            print(summary)
        
        # Display posts with highest engagement
        display_top_posts(processor, args.top)
        
        # Display subreddit distribution
        if len(subreddits) > 1 or subreddits[0] == 'all':
            display_subreddit_distribution(processor)
        
        # Display top contributors
        display_top_contributors(processor, args.top)
        
        # Trend analysis (if specified)
        trends = None
        if args.trends:
            trends = display_trends(processor, args.trends)
        
        # Export data (if specified)
        if args.export:
            exporter = Exporter()
            summary_text = processor.get_summary()
            exporter.export_all(
                posts=posts,
                summary=summary_text,
                trends=trends,
                format=args.export
            )
        
        print("\n✓ Complete!\n")
        
    except ValueError as e:
        print(f"\n✗ Configuration error: {str(e)}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠ User interrupted operation")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
