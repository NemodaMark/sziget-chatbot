export interface ChatMessage {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  speakerLabel: string;
  createdAt: string;
}

export interface ChatSummary {
  id: number;
  title: string;
  preview: string;
  updatedAt: string;
  messages: ChatMessage[];
}

export interface AuthUser {
  id: number;
  name: string;
  email: string;
}

export interface AuthResponse {
  token: string;
  user: AuthUser;
}

export interface ChatResponse {
  chat: ChatSummary;
}
