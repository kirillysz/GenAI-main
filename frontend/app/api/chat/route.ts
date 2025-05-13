import { NextRequest, NextResponse } from 'next/server';

const API = process.env.FASTAPI_URL;

export async function POST(req: NextRequest) {
  try {

    const { content, model = 'llama3.1', telegram_id } = await req.json();
    console.log(telegram_id)
    
    let userRes = await fetch(`${API}/users/get?telegram_id=${telegram_id}`);
    let userId: number;
    
    if (userRes.status === 404) {
      const addUser = await fetch(`${API}/users/add`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ telegram_id }),
      });
      
      if (!addUser.ok) throw new Error('Не удалось создать пользователя');
      userId = await addUser.json();
    } else {
      if (!userRes.ok) throw new Error('Ошибка при получении пользователя');
      userId = await userRes.json();
    }

    let chatsRes = await fetch(`${API}/chats/get_all_chats?user_id=${userId}`);
    let chats = chatsRes.ok ? await chatsRes.json() : [];
    let chatId: string;

    if (!Array.isArray(chats) || chats.length === 0) {
      const newChat = await fetch(`${API}/chats/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },

        body: JSON.stringify({
          user_id: userId,
          chat_title: 'Новый чат',
          model,
        }),
      });
      if (!newChat.ok) throw new Error('Не удалось создать чат');
      chatId = await newChat.json();
    } else {
      chatId = chats[0].chat_id;
    }

    await fetch(`${API}/messages/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: chatId, role: 'user', content }),
    });

    const msgHistoryRes = await fetch(`${API}/messages/get_all_messages?chat_id=${chatId}`);
    if (!msgHistoryRes.ok) throw new Error('Не удалось получить историю сообщений');
    const messages = await msgHistoryRes.json();

    const aiRes = await fetch(`${API}/neuro/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: chatId, messages, model }),
    });

    if (!aiRes.ok) {
      const errText = await aiRes.text();

      return NextResponse.json({ error: errText }, { status: aiRes.status });
    }
    const aiData = await aiRes.json();

    await fetch(`${API}/messages/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: chatId,
        role: 'assistant',
        content: aiData.reply,
      }),
    });

    return NextResponse.json(aiData);
  } catch (err: any) {
    console.error(err);
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
