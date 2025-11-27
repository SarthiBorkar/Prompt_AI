"""
Rate Limiter Module
Implements intelligent rate limiting with exponential backoff to prevent API cost overruns
"""

import time
import asyncio
from typing import Dict, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import random


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting"""
    requests_per_second: int = 2
    requests_per_minute: int = 10
    requests_per_hour: int = 100
    requests_per_day: int = 1000

    # Backoff configuration
    initial_backoff: float = 1.0  # seconds
    max_backoff: float = 60.0  # seconds
    backoff_multiplier: float = 2.0
    jitter: bool = True


@dataclass
class RequestRecord:
    """Record of a single request"""
    timestamp: datetime
    user_id: Optional[str] = None
    endpoint: Optional[str] = None


class RateLimiter:
    """
    Intelligent rate limiter with exponential backoff and jitter
    """

    def __init__(self, config: Optional[RateLimitConfig] = None):
        """
        Initialize rate limiter

        Args:
            config: Rate limit configuration (uses conservative defaults if not provided)
        """
        self.config = config or RateLimitConfig()
        self.requests: deque = deque()
        self.backoff_until: Dict[str, float] = {}  # user_id -> timestamp
        self.consecutive_failures: Dict[str, int] = {}  # user_id -> count

    def check_rate_limit(self, user_id: Optional[str] = None) -> tuple[bool, Optional[str]]:
        """
        Checks if a request should be allowed

        Args:
            user_id: Optional user identifier for per-user limits

        Returns:
            Tuple of (allowed: bool, reason: Optional[str])
        """
        now = datetime.now()
        self._cleanup_old_requests(now)

        # Check backoff period
        if user_id and user_id in self.backoff_until:
            if time.time() < self.backoff_until[user_id]:
                wait_time = self.backoff_until[user_id] - time.time()
                return False, f"Rate limit exceeded. Please wait {wait_time:.1f} seconds."

        # Check per-second limit
        one_second_ago = now - timedelta(seconds=1)
        recent_requests = sum(1 for r in self.requests if r.timestamp > one_second_ago)
        if recent_requests >= self.config.requests_per_second:
            return False, "Per-second rate limit exceeded"

        # Check per-minute limit
        one_minute_ago = now - timedelta(minutes=1)
        minute_requests = sum(1 for r in self.requests if r.timestamp > one_minute_ago)
        if minute_requests >= self.config.requests_per_minute:
            return False, "Per-minute rate limit exceeded"

        # Check per-hour limit
        one_hour_ago = now - timedelta(hours=1)
        hour_requests = sum(1 for r in self.requests if r.timestamp > one_hour_ago)
        if hour_requests >= self.config.requests_per_hour:
            return False, "Per-hour rate limit exceeded"

        # Check per-day limit
        one_day_ago = now - timedelta(days=1)
        day_requests = sum(1 for r in self.requests if r.timestamp > one_day_ago)
        if day_requests >= self.config.requests_per_day:
            return False, "Per-day rate limit exceeded"

        return True, None

    def record_request(self, user_id: Optional[str] = None, endpoint: Optional[str] = None):
        """
        Records a successful request

        Args:
            user_id: Optional user identifier
            endpoint: Optional endpoint identifier
        """
        self.requests.append(RequestRecord(
            timestamp=datetime.now(),
            user_id=user_id,
            endpoint=endpoint
        ))

        # Reset consecutive failures on success
        if user_id and user_id in self.consecutive_failures:
            self.consecutive_failures[user_id] = 0

    def record_failure(self, user_id: Optional[str] = None):
        """
        Records a failed request and applies backoff

        Args:
            user_id: Optional user identifier
        """
        if not user_id:
            user_id = "default"

        # Increment failure count
        self.consecutive_failures[user_id] = self.consecutive_failures.get(user_id, 0) + 1

        # Calculate backoff time
        failures = self.consecutive_failures[user_id]
        backoff = min(
            self.config.initial_backoff * (self.config.backoff_multiplier ** (failures - 1)),
            self.config.max_backoff
        )

        # Add jitter to prevent thundering herd
        if self.config.jitter:
            backoff = backoff * (0.5 + random.random() * 0.5)

        # Set backoff expiration
        self.backoff_until[user_id] = time.time() + backoff

    async def wait_if_needed(self, user_id: Optional[str] = None) -> bool:
        """
        Waits if rate limit is exceeded, returns True if request can proceed

        Args:
            user_id: Optional user identifier

        Returns:
            True if request can proceed, False if permanently blocked
        """
        max_wait_time = 300  # 5 minutes max wait
        start_time = time.time()

        while True:
            allowed, reason = self.check_rate_limit(user_id)

            if allowed:
                return True

            # Check if we've been waiting too long
            if time.time() - start_time > max_wait_time:
                return False

            # Wait before retry
            wait_time = 1.0  # Base wait time
            if user_id and user_id in self.backoff_until:
                wait_time = max(wait_time, self.backoff_until[user_id] - time.time())

            await asyncio.sleep(min(wait_time, 5.0))

    def get_stats(self) -> Dict[str, Any]:
        """
        Gets current rate limiter statistics

        Returns:
            Dictionary with statistics
        """
        now = datetime.now()
        self._cleanup_old_requests(now)

        one_minute_ago = now - timedelta(minutes=1)
        one_hour_ago = now - timedelta(hours=1)
        one_day_ago = now - timedelta(days=1)

        return {
            "total_requests": len(self.requests),
            "requests_last_minute": sum(1 for r in self.requests if r.timestamp > one_minute_ago),
            "requests_last_hour": sum(1 for r in self.requests if r.timestamp > one_hour_ago),
            "requests_last_day": sum(1 for r in self.requests if r.timestamp > one_day_ago),
            "limit_per_minute": self.config.requests_per_minute,
            "limit_per_hour": self.config.requests_per_hour,
            "limit_per_day": self.config.requests_per_day,
            "active_backoffs": len([k for k, v in self.backoff_until.items() if v > time.time()])
        }

    def reset(self, user_id: Optional[str] = None):
        """
        Resets rate limiter state

        Args:
            user_id: If provided, only resets for this user
        """
        if user_id:
            self.requests = deque([r for r in self.requests if r.user_id != user_id])
            if user_id in self.backoff_until:
                del self.backoff_until[user_id]
            if user_id in self.consecutive_failures:
                del self.consecutive_failures[user_id]
        else:
            self.requests.clear()
            self.backoff_until.clear()
            self.consecutive_failures.clear()

    def _cleanup_old_requests(self, now: datetime):
        """Removes requests older than 1 day"""
        one_day_ago = now - timedelta(days=1)
        while self.requests and self.requests[0].timestamp < one_day_ago:
            self.requests.popleft()


class CachedRateLimiter(RateLimiter):
    """
    Rate limiter with caching support to minimize redundant requests
    """

    def __init__(self, config: Optional[RateLimitConfig] = None, cache_ttl: int = 900):
        """
        Initialize cached rate limiter

        Args:
            config: Rate limit configuration
            cache_ttl: Cache time-to-live in seconds (default 15 minutes)
        """
        super().__init__(config)
        self.cache: Dict[str, tuple[Any, float]] = {}  # key -> (result, expiry)
        self.cache_ttl = cache_ttl
        self.cache_hits = 0
        self.cache_misses = 0

    def get_cached(self, key: str) -> Optional[Any]:
        """
        Gets a cached result if available and not expired

        Args:
            key: Cache key

        Returns:
            Cached result or None if not found/expired
        """
        if key in self.cache:
            result, expiry = self.cache[key]
            if time.time() < expiry:
                self.cache_hits += 1
                return result
            else:
                # Expired, remove from cache
                del self.cache[key]

        self.cache_misses += 1
        return None

    def set_cached(self, key: str, value: Any):
        """
        Stores a result in cache

        Args:
            key: Cache key
            value: Value to cache
        """
        expiry = time.time() + self.cache_ttl
        self.cache[key] = (value, expiry)

    def clear_cache(self):
        """Clears all cached entries"""
        self.cache.clear()

    def get_cache_stats(self) -> Dict[str, Any]:
        """Gets cache statistics"""
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = self.cache_hits / total_requests if total_requests > 0 else 0

        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_rate": hit_rate,
            "cached_entries": len(self.cache)
        }


async def rate_limited(func: Callable, rate_limiter: RateLimiter, user_id: Optional[str] = None):
    """
    Decorator function to apply rate limiting to async functions

    Args:
        func: Async function to rate limit
        rate_limiter: RateLimiter instance
        user_id: Optional user identifier

    Returns:
        Rate-limited function result
    """
    can_proceed = await rate_limiter.wait_if_needed(user_id)

    if not can_proceed:
        raise Exception("Rate limit exceeded and maximum wait time reached")

    try:
        result = await func()
        rate_limiter.record_request(user_id)
        return result
    except Exception as e:
        rate_limiter.record_failure(user_id)
        raise e
