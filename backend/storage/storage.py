from utils.utils import Utils
from database.database import Database
from queries import COLD_STORAGE_CREATE_TABLES, \
    COLD_STORAGE_MIGRATE_CHATS, СOLD_STORAGE_MIGRATE_MESSAGES

from config import Config

import asyncpg

cfg = Config()
db = Database(
    host=cfg.DB_INFO["host"],
    user=cfg.DB_INFO["user"],
    password=cfg.DB_INFO["password"],
    database=cfg.DB_INFO["database"]
)

class ColdStorage:
    """Cold storage class for storing."""

    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        self.dsn = f"postgresql://{user}:{password}@{host}/{database}"

    async def connect(self) -> asyncpg.Connection:
        """Connect to the PostgreSQL database.
        
        Returns:
            asyncpg.Connection: Active database connection
        """
        self.connection = await asyncpg.connect(dsn=self.dsn)

        if not self.connection:
            raise ConnectionError("Failed to connect to the database")
        
        return self.connection

    async def close(self) -> None:
        """Close the PostgreSQL connection."""
        if self.connection:
            await self.connection.close()
            self.connection = None

    async def init_tables(self) -> bool:
        """Initialize the database (create tables)."""
        await self.connect()

        try:
            await self.connection.execute(COLD_STORAGE_CREATE_TABLES)

            return True
        
        except asyncpg.exceptions.DuplicateTableError as e:
            raise ValueError("Table already exists") from e
        
        except Exception as e:
            raise RuntimeError(f"Database error: {e}") from e
        
        finally:
            await self.close()


    async def migrate_chats(self, chat_id: str) -> bool:
        """
        Migrate chat data to cold storage.
        
        Args:
            chats_data (str): Chat ID
            
        Returns:
            bool: True if migration succeeded
        """
        await self.connect()
        data = await db.get_chat_by_id(chat_id = chat_id)
        print(data)

        try:
            result = await db.delete_chat(chat_id = chat_id)

            if result:
                return await self._execute_migration(
                    data = data,
                    query = COLD_STORAGE_MIGRATE_CHATS
                )
            else:
                raise ValueError("Chat not found in the database")
            
        except Exception as e:
            raise RuntimeError(f"Migration error: {e}") from e
    
    async def migrate_messages(self, messages_data: dict) -> bool:
        """
        Migrate message data to cold storage.
        
        Args:
            messages_data (dict): Message data in specific format
            
        Returns:
            bool: True if migration succeeded
        """
        await self.connect()

        try:
            result = await db.delete_message(message_id=messages_data["message_id"])

            if result:
                return await self._execute_migration_with_compress(
                    data=messages_data,
                    query=СOLD_STORAGE_MIGRATE_MESSAGES
                )
            else:
                raise ValueError("Message not found in the database")
            
        except Exception as e:
            raise RuntimeError(f"Migration error: {e}") from e


    async def _execute_migration(self, data: dict, query: str) -> bool:
        await self.connect()

        try:
            print(list(data.values()))
            result = await self.connection.execute(query, *list(data.values()))

            return bool(result)
        
        except Exception as e:
            raise RuntimeError(f"Migration error: {e}") from e
        
        finally:
            await self.close()

    async def _execute_migration_with_compress(self, data: dict, query: str) -> bool:
        """
        Shared migration logic
        
        Args:
            data: Data to migrate
            query: SQL query to execute
        
        Returns:
            bool: Migration status
        """
        await self.connect()
        utils = Utils()
        
        try:            
            compressed_data = await utils.async_compress(data)
            result = await self.connection.execute(query, compressed_data.items())

            return bool(result)
        
        except Exception as e:
            raise RuntimeError(f"Migration error: {e}") from e
        
        finally:
            await self.close()


        