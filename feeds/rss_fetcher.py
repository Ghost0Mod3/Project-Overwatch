"""
Project Overwatch
RSS Feed Retrieval Engine
"""

import re
from html import unescape

import feedparser
import requests

from feeds.sources import get_enabled_sources
from intelligence.classifier import classify_event
from intelligence.relevance import calculate_relevance


class RSSFetcher:

    def __init__(self):
        # Load no more than four articles from each feed.
        self.max_articles_per_feed = 4

        # Prevent one broken feed from freezing Overwatch.
        self.request_timeout = 10

        self.user_agent = (
            "ProjectOverwatch/0.1 "
            "Windows RSS Intelligence Monitor"
        )

    # ==================================================
    # FETCH ALL ENABLED SOURCES
    # ==================================================

    def get_articles(self):
        """
        Retrieve up to four articles from every enabled feed.

        Returns one combined list sorted by relevance score.
        """

        enabled_sources = get_enabled_sources()

        articles = []
        seen_links = set()
        seen_headlines = set()

        for source in enabled_sources:
            source_articles = self.fetch_source(
                source
            )

            for article in source_articles:
                link_key = self.normalize_link(
                    article.get(
                        "link",
                        ""
                    )
                )

                headline_key = self.normalize_headline(
                    article.get(
                        "title",
                        ""
                    )
                )

                # Remove duplicate articles found in overlapping
                # feeds or Google News monitoring searches.
                if link_key and link_key in seen_links:
                    continue

                if (
                    headline_key
                    and headline_key in seen_headlines
                ):
                    continue

                if link_key:
                    seen_links.add(link_key)

                if headline_key:
                    seen_headlines.add(headline_key)

                articles.append(article)

        articles.sort(
            key=lambda item: self.score_article(item),
            reverse=True,
        )

        return articles

    def fetch_source(self, source):
        """
        Fetch and normalize articles from a single source.
        """
        try:
            response = requests.get(
                source["url"],
                timeout=self.request_timeout,
                headers={"User-Agent": self.user_agent},
            )
            response.raise_for_status()
        except requests.RequestException:
            return []

        feed = feedparser.parse(response.text)
        entries = feed.entries[: self.max_articles_per_feed]

        parsed_articles = []
        for entry in entries:
            article = {
                "title": self.clean_title(entry.get("title", "")),
                "link": entry.get("link", ""),
                "summary": self.clean_summary(entry.get("summary", "")),
                "published": entry.get("published", ""),
                "source": source.get("name", "Unknown"),
                "category": source.get("category", "general"),
            }

            parsed_articles.append(article)

        return parsed_articles

    def normalize_link(self, link):
        if not link:
            return ""
        return re.sub(r"[?#].*$", "", link.strip())

    def normalize_headline(self, headline):
        if not headline:
            return ""
        return re.sub(r"\s+", " ", unescape(headline)).strip().lower()

    def clean_title(self, title):
        return unescape(re.sub(r"\s+", " ", title or "")).strip()

    def clean_summary(self, summary):
        if not summary:
            return ""
        return unescape(re.sub(r"\s+", " ", summary)).strip()

    def score_article(self, article):
        text = " ".join(
            [
                article.get("title", ""),
                article.get("summary", ""),
                article.get("source", ""),
            ]
        )
        classification = classify_event(text)
        relevance = calculate_relevance(text, classification)
        return relevance
