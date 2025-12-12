import { Component, computed, input, output } from '@angular/core';
import { MatButtonAppearance, MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-button',
  imports: [MatButtonModule, MatProgressSpinnerModule],
  templateUrl: './button.html',
})
export class Button {
  appearance = input<MatButtonAppearance>('filled');
  disabled = input<boolean>(false);
  isLoading = input<boolean>(false);
  fullWidth = input<boolean>(false);
  clicked = output<void>();
  fullWidthClasses = computed(() => (this.fullWidth() ? 'w-full' : ''));
}
