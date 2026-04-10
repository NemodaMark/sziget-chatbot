import { Injectable, computed, inject, signal } from '@angular/core';
import { ChatMessage, ChatSummary } from '../models/chat.models';
import { ApiService } from './api.service';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private readonly api = inject(ApiService);
  private readonly auth = inject(AuthService);

  private readonly guestMessagesState = signal<ChatMessage[]>([
      {
        id: 1,
        role: 'assistant',
        content: 'Flo itt van. Dobd be, milyen napot raknal ossze a Szigeten, es indulhat a flow.',
        speakerLabel: 'FLO',
        createdAt: new Date().toISOString()
      }
  ]);
  private readonly chatsState = signal<ChatSummary[]>([]);
  private readonly activeChatIdState = signal<number | null>(null);
  private readonly loadingState = signal(false);

  readonly guestMessages = this.guestMessagesState.asReadonly();
  readonly chats = this.chatsState.asReadonly();
  readonly activeChatId = this.activeChatIdState.asReadonly();
  readonly loading = this.loadingState.asReadonly();
  readonly activeChat = computed(() => this.chatsState().find((chat) => chat.id === this.activeChatIdState()) ?? null);

  async sendGuestMessage(message: string): Promise<void> {
    const trimmed = message.trim();
    if (!trimmed) {
      return;
    }

    this.loadingState.set(true);
    const currentMessages = this.guestMessagesState();
    const userMessage = this.createLocalMessage(trimmed, 'user');
    this.guestMessagesState.set([...currentMessages, userMessage]);

    try {
      const response = await this.api.guestChat({
        message: trimmed,
        messages: [...currentMessages, userMessage].map((entry) => ({
          role: entry.role,
          content: entry.content
        }))
      });

      this.guestMessagesState.set(this.normalizeMessages(response.chat.messages));
    } finally {
      this.loadingState.set(false);
    }
  }

  async loadChats(): Promise<void> {
    const token = this.auth.token();
    if (!token) {
      return;
    }

    this.loadingState.set(true);
    try {
      const response = await this.api.listChats(token);
      const normalizedChats = response.chats.map((chat) => this.normalizeChat(chat));
      this.chatsState.set(normalizedChats);
      this.activeChatIdState.set(normalizedChats[0]?.id ?? null);
    } finally {
      this.loadingState.set(false);
    }
  }

  async createChat(): Promise<void> {
    const token = this.auth.token();
    if (!token) {
      return;
    }

    this.loadingState.set(true);
    try {
      const response = await this.api.createChat(token);
      const nextChats = [this.normalizeChat(response.chat), ...this.chatsState()];
      this.chatsState.set(nextChats);
      this.activeChatIdState.set(response.chat.id);
    } finally {
      this.loadingState.set(false);
    }
  }

  selectChat(chatId: number): void {
    this.activeChatIdState.set(chatId);
  }

  async sendLoggedInMessage(message: string): Promise<void> {
    const trimmed = message.trim();
    const token = this.auth.token();
    const chatId = this.activeChatIdState();
    if (!trimmed || !token || !chatId) {
      return;
    }

    const currentChat = this.activeChat();
    if (!currentChat) {
      return;
    }

    const optimisticMessage = this.createLocalMessage(trimmed, 'user');
    this.patchChat({
      ...currentChat,
      preview: trimmed,
      updatedAt: optimisticMessage.createdAt,
      messages: [...currentChat.messages, optimisticMessage]
    });

    this.loadingState.set(true);
    try {
      const response = await this.api.sendMessage(token, chatId, trimmed);
      this.patchChat(this.normalizeChat(response.chat), true);
    } finally {
      this.loadingState.set(false);
    }
  }

  resetForLogout(): void {
    this.chatsState.set([]);
    this.activeChatIdState.set(null);
  }

  private patchChat(chat: ChatSummary, moveToFront = false): void {
    const remaining = this.chatsState().filter((entry) => entry.id !== chat.id);
    this.chatsState.set(moveToFront ? [chat, ...remaining] : [chat, ...remaining]);
  }

  private normalizeChat(chat: ChatSummary): ChatSummary {
    return {
      ...chat,
      preview: this.cleanAssistantPrefix(chat.preview),
      messages: this.normalizeMessages(chat.messages)
    };
  }

  private normalizeMessages(messages: ChatMessage[]): ChatMessage[] {
    return messages.map((message) => ({
      ...message,
      speakerLabel: message.role === 'assistant' ? 'FLO' : 'TE',
      content: message.role === 'assistant' ? this.cleanAssistantPrefix(message.content) : message.content
    }));
  }

  private cleanAssistantPrefix(content: string): string {
    return content.replace(/^FLO MONDJA:\s*/i, '').trim();
  }

  private createLocalMessage(content: string, role: 'user' | 'assistant'): ChatMessage {
    return {
      id: Date.now(),
      role,
      content,
      speakerLabel: role === 'assistant' ? 'FLO' : 'TE',
      createdAt: new Date().toISOString()
    };
  }
}
