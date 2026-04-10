import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { lastValueFrom } from 'rxjs';
import { AuthResponse, ChatResponse, ChatSummary, QuestionTheme } from '../models/chat.models';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = 'http://127.0.0.1:8000/api';

  async register(payload: { name: string; email: string; password: string }): Promise<AuthResponse> {
    return lastValueFrom(this.http.post<AuthResponse>(`${this.baseUrl}/register`, payload));
  }

  async login(payload: { email: string; password: string }): Promise<AuthResponse> {
    return lastValueFrom(this.http.post<AuthResponse>(`${this.baseUrl}/login`, payload));
  }

  async guestChat(payload: { message: string; messages: { role: string; content: string }[] }): Promise<ChatResponse> {
    return lastValueFrom(this.http.post<ChatResponse>(`${this.baseUrl}/guest-chat`, payload));
  }

  async listThemes(): Promise<{ themes: QuestionTheme[] }> {
    return lastValueFrom(this.http.get<{ themes: QuestionTheme[] }>(`${this.baseUrl}/themes`));
  }

  async listChats(token: string): Promise<{ chats: ChatSummary[] }> {
    return lastValueFrom(this.http.get<{ chats: ChatSummary[] }>(`${this.baseUrl}/chats`, {
      headers: this.authHeaders(token)
    }));
  }

  async createChat(token: string): Promise<ChatResponse> {
    return lastValueFrom(this.http.post<ChatResponse>(`${this.baseUrl}/chats`, {}, {
      headers: this.authHeaders(token)
    }));
  }

  async sendMessage(token: string, chatId: number, message: string): Promise<ChatResponse> {
    return lastValueFrom(this.http.post<ChatResponse>(`${this.baseUrl}/chats/${chatId}/messages`, {
      message
    }, {
      headers: this.authHeaders(token)
    }));
  }

  private authHeaders(token: string): HttpHeaders {
    return new HttpHeaders({
      Authorization: `Bearer ${token}`
    });
  }
}
