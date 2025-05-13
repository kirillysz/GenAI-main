import hashlib
import asyncio
import lzma
import json

class Utils:
    """ Utils class """
    def hash_value(self, value: str) -> str:
        """Hash a value using SHA-256.
        
        Args:
            value (str): The value to hash.
        
        Returns:
            str: The SHA-256 hash of the value.
        """
        return hashlib.sha256(value.encode()).hexdigest()


    def _compress_data(self, data: dict) -> bytes:
        """Compress dictionary using LZMA."""
        return lzma.compress(json.dumps(data).encode('utf-8'), preset=9)

    def _decompress_data(self, blob: bytes) -> dict:
        """Decompress LZMA-compressed bytes to dictionary."""
        return json.loads(lzma.decompress(blob).decode('utf-8'))

    async def async_compress(self, data: dict) -> bytes:
        """Asynchronously compress a dictionary."""
        return await asyncio.to_thread(self._compress_data, data)

    async def async_decompress(self, blob: bytes) -> dict:
        """Asynchronously decompress LZMA-compressed bytes."""
        return await asyncio.to_thread(self._decompress_data, blob)
