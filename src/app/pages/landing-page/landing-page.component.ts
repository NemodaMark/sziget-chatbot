import { CommonModule } from '@angular/common';
import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ChatMessage, QuestionTheme } from '../../models/chat.models';
import { ApiService } from '../../services/api.service';
import { ChatService } from '../../services/chat.service';

@Component({
  selector: 'app-landing-page',
  imports: [CommonModule, FormsModule],
  templateUrl: './landing-page.component.html',
  styleUrl: './landing-page.component.scss'
})
export class LandingPageComponent implements OnInit {
  protected readonly chat = inject(ChatService);
  private readonly api = inject(ApiService);
  protected readonly message = signal('');
  protected readonly guestMessages = this.chat.guestMessages;
  protected readonly loading = this.chat.loading;
  protected readonly remainingChats = computed(() => 1);
  protected readonly previewConversation = signal(false);
  protected readonly questionThemes = signal<QuestionTheme[]>([
    {
      intent: 'festival_info',
      category: 'Festival info',
      title: 'Mikor, hol, hogyan indul?',
      example: 'Iden is augusztus elejen lesz a Sziget?',
      accentClass: 'question-a',
      questions: ['Iden is augusztus elejen lesz a Sziget?']
    },
    {
      intent: 'pricing',
      category: 'Jegyek es arak',
      title: 'Melyik jegy eri meg?',
      example: 'Early bird meg megeri?',
      accentClass: 'question-b',
      questions: ['Early bird meg megeri?']
    },
    {
      intent: 'camping',
      category: 'Camping',
      title: 'Milyen a kemping elet?',
      example: 'Megeri upgrade-elni a kempinget?',
      accentClass: 'question-c',
      questions: ['Megeri upgrade-elni a kempinget?']
    },
    {
      intent: 'rules',
      category: 'Szabalyok',
      title: 'Mire figyeljek belepesnel?',
      example: 'Mit nem lehet bevinni?',
      accentClass: 'question-d',
      questions: ['Mit nem lehet bevinni?']
    },
    {
      intent: 'general',
      category: 'Hangulat',
      title: 'Milyen mostanaban a vibe?',
      example: 'Milyen az altalanos hangulat?',
      accentClass: 'question-e',
      questions: ['Milyen az altalanos hangulat?']
    },
    {
      intent: 'lineup_schedule',
      category: 'Lineup es menetrend',
      title: 'Kik lepnek fel melyik nap?',
      example: 'Ki lep fel melyik nap?',
      accentClass: 'question-f',
      questions: ['Ki lep fel melyik nap?']
    },
    {
      intent: 'programs',
      category: 'Programok',
      title: 'Mit lehet csinalni a koncerteken tul?',
      example: 'Van valami nyugisabb program is?',
      accentClass: 'question-g',
      questions: ['Van valami nyugisabb program is?']
    }
  ]);
  protected readonly previewMessages: ChatMessage[] = [
    {
      id: 201,
      role: 'assistant',
      content: 'Flo itt van. Mondd el, milyen Sziget-napot raknal ossze, es indulhat is a tervezes.',
      speakerLabel: 'FLO',
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
      speakerLabel: 'FLO',
      createdAt: new Date().toISOString()
    }
  ];
  protected readonly displayedMessages = computed(() =>
    this.previewConversation() ? this.previewMessages : this.guestMessages()
  );

  async ngOnInit(): Promise<void> {
    try {
      const response = await this.api.listThemes();
      if (response.themes.length) {
        this.questionThemes.set(response.themes);
      }
    } catch {
      // Keep frontend fallbacks if backend themes are unavailable.
    }
  }

  protected togglePreviewConversation(): void {
    this.previewConversation.update((value) => !value);
  }

  protected useThemeQuestion(question: string): void {
    this.message.set(question);
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
