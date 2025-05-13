CREATE_TABLES = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        telegram_id_hash VARCHAR(255) UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS chats (
        chat_id UUID PRIMARY KEY,
        user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        title VARCHAR(512) NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        model VARCHAR(50) NOT NULL,
        is_active BOOLEAN NOT NULL DEFAULT TRUE
    );

    CREATE TABLE IF NOT EXISTS messages (
        message_id UUID PRIMARY KEY,
        chat_id UUID NOT NULL REFERENCES chats(chat_id) ON DELETE CASCADE,
        role VARCHAR(9) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
        content TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS balances (
        user_id BIGINT NOT NULL REFERENCES users(id),
        user_balance INTEGER,
        user_tokens TEXT[],
        tokens_balance INTEGER
    );

"""

COLD_STORAGE_CREATE_TABLES = """
    CREATE TABLE IF NOT EXISTS cold_storage_chats (
        chat_id UUID PRIMARY KEY,
        user_id BIGINT NOT NULL,
        title TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL,
        model TEXT NOT NULL,
        is_active BOOLEAN NOT NULL
    );

    CREATE TABLE IF NOT EXISTS cold_storage_messages (
        message_id UUID PRIMARY KEY,
        chat_id UUID NOT NULL REFERENCES cold_storage_chats(chat_id) ON DELETE CASCADE,
        role_compressed BYTEA NOT NULL,
        content_compressed BYTEA NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL
    );
"""




QUERY_ADD_USER =  """INSERT INTO users (telegram_id_hash) VALUES ($1)"""
QUERY_GET_USER = """SELECT id FROM users WHERE telegram_id_hash = $1"""

QUERY_ADD_CHAT = """INSERT INTO chats (chat_id, user_id, title, model) VALUES ($1, $2, $3, $4)"""
QUERY_GET_CHAT_TITLE = """SELECT title FROM chats WHERE chat_id = $1"""
QUERY_GET_ALL_CHATS = """SELECT chat_id, title FROM chats WHERE user_id = $1"""
QUERY_DELETE_CHAT = """
    WITH deleted_messages AS (
        DELETE FROM messages WHERE chat_id = $1
    )
    DELETE FROM chats WHERE chat_id = $1
"""
QUERY_GET_CHAT_BY_ID = """SELECT * FROM chats WHERE chat_id = $1"""

QUERY_ADD_MESSAGE = """INSERT INTO messages (message_id, chat_id, role, content) VALUES ($1, $2, $3, $4)"""
QUERY_GET_ALL_MESSAGES = """SELECT message_id, role, content FROM messages WHERE chat_id = $1"""
QUERY_EDIT_MESSAGE = """UPDATE messages SET content = $1 WHERE message_id = $2 AND chat_id = $3"""
QUERY_DELETE_MESSAGE = """DELETE FROM messages WHERE message_id = $1 AND chat_id = $2"""


COLD_STORAGE_MIGRATE_CHATS = """INSERT INTO cold_storage_chats (chat_id, user_id, title, created_at, model, is_active) 
                            VALUES ($1, $2, $3, $4, $5, $6)"""

СOLD_STORAGE_MIGRATE_MESSAGES = """INSERT INTO cold_storage_messages (message_id, chat_id, role_compressed, content_compressed, created_at)
                            VALUES ($1, $2, $3, $4, $5)"""


