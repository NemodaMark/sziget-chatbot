import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ChatMessage } from '../../models/chat.models';
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
  protected readonly previewConversation = signal(false);
  protected readonly questionThemes = [
    {
      category: 'Festival info',
      title: 'Mikor, hol, hogyan indul?',
      example: '"Iden is augusztus elejen lesz a Sziget?"',
      accentClass: 'question-a'
    },
    {
      category: 'Jegyek es arak',
      title: 'Melyik jegy eri meg?',
      example: '"Early bird meg megeri?"',
      accentClass: 'question-b'
    },
    {
      category: 'Camping',
      title: 'Milyen a kemping elet?',
      example: '"Megeri upgrade-elni a kempinget?"',
      accentClass: 'question-c'
    },
    {
      category: 'Szabalyok',
      title: 'Mire figyeljek belepesnel?',
      example: '"Mit nem lehet bevinni?"',
      accentClass: 'question-d'
    },
    {
      category: 'Hangulat',
      title: 'Milyen mostanaban a vibe?',
      example: '"Milyen az altalanos hangulat?"',
      accentClass: 'question-e'
    },
    {
      category: 'Lineup es menetrend',
      title: 'Kik lepnek fel melyik nap?',
      example: '"Ki lep fel melyik nap?"',
      accentClass: 'question-f'
    },
    {
      category: 'Programok',
      title: 'Mit lehet csinalni a koncerteken tul?',
      example: '"Van valami nyugisabb program is?"',
      accentClass: 'question-g'
    }
  ];
  protected readonly previewMessages: ChatMessage[] = [
    {
      id: 201,
      role: 'assistant',
      content: 'Flo itt van. Mondd el, milyen Sziget-napot raknal ossze, es indulhat is a tervezes.',
      speakerLabel: 'FLO MONDJA',
      createdAt: new Date().toISOString()
    },
    {
      id: 202,
      role: 'user',
      content: 'Egy napra megyek, foleg esti koncertek es jo kajak erdekelnek.',
      speakerLabel: 'TE',
      createdAt: new Date().toISOString()
    },
    {
      id: 203,
      role: 'assistant',
      content:
        'Akkor erdemes egy laza delutani erkezessel inditani, utana lineupra ranezni, enni egy nagyobbat, es este nyitni a koncertkort. Ha akarod, osszerakok egy konkret mini-tervet is.',
      speakerLabel: 'FLO MONDJA',
      createdAt: new Date().toISOString()
    }
  ];
  protected readonly displayedMessages = computed(() =>
    this.previewConversation() ? this.previewMessages : this.guestMessages()
  );

  protected togglePreviewConversation(): void {
    this.previewConversation.update((value) => !value);
  }

  protected async sendMessage(): Promise<void> {
    if (this.previewConversation()) {
      this.previewConversation.set(false);
    }

    const draft = this.message();
    this.message.set('');
    await this.chat.sendGuestMessage(draft);
  }
}
