import { CommonModule } from '@angular/common';
import { Component, effect, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { CabalaMascotComponent } from '../../components/cabala-mascot/cabala-mascot.component';
import { AuthService } from '../../services/auth.service';
import { ChatService } from '../../services/chat.service';

@Component({
  selector: 'app-chat-page',
  imports: [CommonModule, FormsModule, CabalaMascotComponent],
  templateUrl: './chat-page.component.html',
  styleUrl: './chat-page.component.scss'
})
export class ChatPageComponent {
  protected readonly auth = inject(AuthService);
  protected readonly chat = inject(ChatService);
  private readonly router = inject(Router);

  protected readonly draft = signal('');

  constructor() {
    effect(() => {
      if (this.auth.isAuthenticated() && this.chat.chats().length === 0 && !this.chat.loading()) {
        void this.initialize();
      }
    });
  }

  protected async createChat(): Promise<void> {
    await this.chat.createChat();
  }

  protected async sendMessage(): Promise<void> {
    const message = this.draft();
    this.draft.set('');
    await this.chat.sendLoggedInMessage(message);
  }

  protected async logout(): Promise<void> {
    this.auth.logout();
    this.chat.resetForLogout();
    await this.router.navigateByUrl('/');
  }

  private async initialize(): Promise<void> {
    await this.chat.loadChats();
    if (!this.chat.activeChat() && this.auth.isAuthenticated()) {
      await this.chat.createChat();
    }
  }
}
