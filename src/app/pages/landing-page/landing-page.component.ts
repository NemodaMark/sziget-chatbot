import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../../services/chat.service';

@Component({
  selector: 'app-landing-page',
  imports: [CommonModule, FormsModule],
  templateUrl: './landing-page.component.html',
  styleUrl: './landing-page.component.scss'
})
export class LandingPageComponent {
  protected readonly chat = inject(ChatService);
  protected readonly message = signal('');
  protected readonly guestMessages = this.chat.guestMessages;
  protected readonly loading = this.chat.loading;
  protected readonly remainingChats = computed(() => 1);

  protected async sendMessage(): Promise<void> {
    const draft = this.message();
    this.message.set('');
    await this.chat.sendGuestMessage(draft);
  }
}
