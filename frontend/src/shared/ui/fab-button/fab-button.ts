import { Component, input, output } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';

@Component({
  selector: 'app-fab-button',
  imports: [MatButtonModule, MatIconModule, MatTooltipModule],
  templateUrl: './fab-button.html',
})
export class FabButton {
  icon = input.required<string>();
  disabled = input<boolean>(false);
  tooltip = input<string>('');
  clicked = output<void>();
}
