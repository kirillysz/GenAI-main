from utils.utils import Utils
from queries import CREATE_TABLES, QUERY_ADD_USER, \
    QUERY_GET_USER, QUERY_ADD_CHAT, QUERY_DELETE_CHAT, QUERY_GET_ALL_CHATS, QUERY_GET_CHAT_TITLE, QUERY_GET_CHAT_BY_ID, \
    QUERY_GET_ALL_MESSAGES, QUERY_ADD_MESSAGE, QUERY_EDIT_MESSAGE, QUERY_DELETE_MESSAGE

import asyncpg

utils = Utils()

class Database:
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
        """Close the connection to the PostgreSQL database."""
        if self.connection:
            await self.connection.close()
            self.connection = None

    async def create_tables(self) -> bool:
        """Create tables in the PostgreSQL database (users, chats, messages).
        
        Returns:
            bool: True if tables were created successfully
            
        Raises:
            ValueError: If tables already exist
            RuntimeError: For other database errors
        """
        await self.connect()

        try:
            await self.connection.execute(CREATE_TABLES)
            return True
        
        except asyncpg.exceptions.DuplicateTableError as e:
            raise ValueError("Table already exists") from e
        
        except Exception as e:
            raise RuntimeError(f"Database error: {e}") from e

        finally:
            await self.close()
    
    async def init_db(self) -> bool:
        """Initialize the PostgreSQL database.
        
        Returns:
            bool: True if initialization succeeded
            
        Raises:
            RuntimeError: For database errors during initialization
        """
        await self.connect()
        
        try:
            result = await self.create_tables()
            return result
        
        except ValueError as _:
            pass

        except Exception as e:
            raise RuntimeError(f"Database error: {e}") from e
        
        finally:
            await self.close()
    
    # USER FUNCTIONS
    async def register_user(self, telegram_id: int) -> bool:
        """Add a user to the database.
        
        Args:
            telegram_id: Telegram user ID
            
        Returns:
            bool: True if user was added successfully

        Raises:
            asyncpg.UniqueViolationError: If user already exists
            asyncpg.PostgresError: For other database errors
        """
        await self.connect()
        telegram_id_hash = utils.hash_value(str(telegram_id))

        try:
            await self.connection.execute(
               QUERY_ADD_USER,
                telegram_id_hash
            )
            return True
        
        except asyncpg.exceptions.UniqueViolationError as e:
            raise ValueError("User already exists") from e
        
        except Exception as e:
            raise RuntimeError(f"Database error: {e}") from e
        
        finally:
            await self.close()

    async def get_user(self, telegram_id: str) -> int:
        """Get user ID from the database.
        
        Args:
            telegram_id: Telegram user ID
            
        Returns:
            int: User ID from table 'users'
            
        Raises:
            asyncpg.PostgresError: For other database errors
        """
        await self.connect()
        telegram_id_hash = utils.hash_value(telegram_id)

        try:
            result = await self.connection.fetchrow(
                QUERY_GET_USER,
                telegram_id_hash
            )
            return result
        
        finally:
            await self.close()


    # CHAT'S FUNCTIONS
    async def add_chat(self, user_id: int, chat_id: str, title: str, model: str = "tyt bydet modelka") -> bool:
        """Add a chat to the database.
        
        Args:
            user_id: User ID (from the users table)
            chat_id: Chat ID
            title: Chat title
            model: Model name (default is "tyt bydet modelka")
        
        Returns:
            bool: True if chat was added successfully
            
        Raises:
            asyncpg.UniqueViolationError: If chat already exists
            asyncpg.PostgresError: For other database errors
        """
        await self.connect()

        try:
            await self.connection.execute(
                QUERY_ADD_CHAT,
                chat_id,
                user_id,
                title,
                model
            )
            return True
        
        except asyncpg.exceptions.UniqueViolationError as e:
            raise ValueError("Chat already exists") from e
        
        except Exception as e:
            raise RuntimeError(f"Database error: {e}") from e
        
        finally:
            await self.close()

    async def get_chat_title(self, chat_id: str) -> str:
        """Get chat title from the database.
        
        Args:
            chat_id: Chat ID
            
        Returns:
            str: Chat title
            
        Raises:
            asyncpg.PostgresError: For other database errors
        """
        await self.connect()

        try:
            result = await self.connection.fetchrow(
                QUERY_GET_CHAT_TITLE,
                chat_id
            )
            return result[0]
        
        finally:
            await self.close()

    async def get_all_chats(self, user_id: int) -> list:
        """Get all chats for a user from the database.
        
        Args:
            user_id: User ID
            
        Returns:
            list: List of chat IDs and titles
            
        Raises:
            asyncpg.PostgresError: For other database errors
        """
        await self.connect()
        

        try:
            result = await self.connection.fetch(
                QUERY_GET_ALL_CHATS,
                user_id
            )
            return result
        
        finally:
            await self.close()

    async def delete_chat(self, chat_id: str) -> bool:
        """Delete a chat from the database.
        
        Args:
            chat_id: Chat ID
            
        Returns:
            bool: True if chat was deleted successfully
            
        Raises:
            asyncpg.PostgresError: For other database errors
        """
        await self.connect()

        try:
            await self.connection.execute(
                QUERY_DELETE_CHAT,
                chat_id
            )
            return True
        
        except Exception as e:
            raise RuntimeError(f"Database error: {e}") from e
        
        finally:
            await self.close()

    async def get_chat_by_id(self, chat_id: str) -> dict:
        await self.connect()

        try:
            result = await self.connection.fetch(QUERY_GET_CHAT_BY_ID, chat_id)
            
            if not result:
                return {}
            
            chat_data = dict(result[0])
            return chat_data
        
        except Exception as e:
            raise RuntimeError(f"Database error: {e}") from e
        
        finally:
            await self.close()

    # MESSAGE'S FUNCTIONS
    async def get_all_messages(self, chat_id: str) -> list:
        """Get all messages for a chat from the database.
        
        Args:
            chat_id: Chat ID
            
        Returns:
            list: List of message IDs, roles, and content
            
        Raises:
            asyncpg.PostgresError: For other database errors
        """
        await self.connect()

        try:
            result = await self.connection.fetch(
                QUERY_GET_ALL_MESSAGES,
                chat_id
            )
            return result
        
        finally:
            await self.close()

    async def add_message(self, message_id: str, chat_id: str, role: str, content: str) -> bool:
        """Add a message to the database.
        
        Args:
            chat_id: Chat ID (UUID)
            message_id: Message ID (UUID)
            role: Role of the sender (user, assistant, system)
            content: Content of the message

        Returns:
            bool: True if message was added successfully
            
        Raises:
            asyncpg.UniqueViolationError: If message already exists
            asyncpg.PostgresError: For other database errors
        """
        await self.connect()

        try:
            await self.connection.execute(
                QUERY_ADD_MESSAGE,
                message_id,
                chat_id,
                role,
                content
            )
            return True
        
        finally:
            await self.close()

    async def edit_message(self, chat_id: str, message_id: str, content: str) -> bool:
        """Edit a message in the database.
        
        Args:
            chat_id: Chat ID (UUID)
            message_id: Message ID (UUID)
            content: New content for the message
            
        Returns:
            bool: True if message was edited successfully

        Raises:
            asyncpg.PostgresError: For other database errors
        """
        await self.connect()

        try:
            await self.connection.execute(
                QUERY_EDIT_MESSAGE,
                content,
                message_id,
                chat_id
            )
            return True

        finally:
            await self.close()

    async def delete_message(self, message_id: str, chat_id: str) -> bool:
        """Delete a message from the database.
        
        Args:
            message_id: Message ID (UUID)
            chat_id: Chat ID (UUID)
            
        Returns:
            bool: True if message was deleted successfully
            
        Raises:
            asyncpg.PostgresError: For other database errors
        """
        await self.connect()

        try:
            await self.connection.execute(
                QUERY_DELETE_MESSAGE,
                message_id,
                chat_id
            )
            return True
        
        finally:
            await self.close()