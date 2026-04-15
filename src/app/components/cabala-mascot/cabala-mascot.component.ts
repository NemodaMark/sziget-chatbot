import { CommonModule } from '@angular/common';
import { Component, input } from '@angular/core';

@Component({
  selector: 'app-cabala-mascot',
  imports: [CommonModule],
  templateUrl: './cabala-mascot.component.html',
  styleUrl: './cabala-mascot.component.scss'
})
export class CabalaMascotComponent {
  readonly size = input<'reply' | 'composer'>('reply');
  readonly bubble = input<string>('');
}
