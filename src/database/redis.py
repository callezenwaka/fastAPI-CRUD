# src/database/redis.py
import asyncio
from redis.asyncio import Redis
from src.config import Config

JTI_EXPIRY = 3600

class RedisClient:
    def __init__(self):
        self.redis = Redis(
            host=Config.redis_host,
            port=Config.redis_port,
            decode_responses=True  # Ensures values are returned as strings
        )

    async def add_jti_to_blocklist(self, jti: str) -> None:
        """
        Add a JTI (JWT Token ID) to the blocklist with an expiry time.
        """
        await self.redis.set(
            name=jti,
            value="",
            ex=JTI_EXPIRY,  # Expiration time in seconds
        )

    async def token_in_blocklist(self, jti: str) -> bool:
        """
        Check if a JTI is in the blocklist.
        """
        result = await self.redis.get(jti)
        return result is not None
    
# Create database instance without connecting
redisClient = RedisClient()
