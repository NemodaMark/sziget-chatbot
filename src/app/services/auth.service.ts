import { Injectable, computed, inject, signal } from '@angular/core';
import { AuthUser } from '../models/chat.models';
import { ApiService } from './api.service';

const TOKEN_KEY = 'sziget-token';
const USER_KEY = 'sziget-user';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly api = inject(ApiService);
  private readonly tokenState = signal<string | null>(localStorage.getItem(TOKEN_KEY));
  private readonly userState = signal<AuthUser | null>(this.readStoredUser());

  readonly user = this.userState.asReadonly();
  readonly token = this.tokenState.asReadonly();
  readonly isAuthenticated = computed(() => Boolean(this.tokenState() && this.userState()));

  async register(payload: { name: string; email: string; password: string }): Promise<void> {
    const response = await this.api.register(payload);
    this.persistSession(response.token, response.user);
  }

  async login(payload: { email: string; password: string }): Promise<void> {
    const response = await this.api.login(payload);
    this.persistSession(response.token, response.user);
  }

  logout(): void {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    this.tokenState.set(null);
    this.userState.set(null);
  }

  private persistSession(token: string, user: AuthUser): void {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
    this.tokenState.set(token);
    this.userState.set(user);
  }

  private readStoredUser(): AuthUser | null {
    const raw = localStorage.getItem(USER_KEY);
    if (!raw) {
      return null;
    }

    try {
      return JSON.parse(raw) as AuthUser;
    } catch {
      localStorage.removeItem(USER_KEY);
      return null;
    }
  }
}
