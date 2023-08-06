"""Declares :class:`APIMetadataService`."""
from typing import List


class APIMetadataService:
    """Provides an interface to query the API metadata."""

    async def get(self):
        """Return a dictionary holding all API properties."""
        return {
            'capabilities': await self.capabilities(),
        }

    async def capabilities(self) -> List[str]:
        """Return the list of API capabilities."""
        return []
