import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-auth-page',
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './auth-page.component.html',
  styleUrl: './auth-page.component.scss'
})
export class AuthPageComponent {
  protected readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  protected readonly mode = signal<'login' | 'register'>('login');
  protected readonly busy = signal(false);
  protected readonly error = signal('');
  protected readonly form = signal({
    name: '',
    email: '',
    password: ''
  });

  protected setMode(nextMode: 'login' | 'register'): void {
    this.mode.set(nextMode);
    this.error.set('');
  }

  protected updateField(field: 'name' | 'email' | 'password', value: string): void {
    this.form.update((current) => ({
      ...current,
      [field]: value
    }));
  }

  protected async submit(): Promise<void> {
    const value = this.form();
    this.busy.set(true);
    this.error.set('');

    try {
      if (this.mode() === 'register') {
        await this.auth.register(value);
      } else {
        await this.auth.login({
          email: value.email,
          password: value.password
        });
      }

      await this.router.navigateByUrl('/app');
    } catch (error) {
      this.error.set(error instanceof Error ? error.message : 'Sikertelen hitelesites.');
    } finally {
      this.busy.set(false);
    }
  }
}
