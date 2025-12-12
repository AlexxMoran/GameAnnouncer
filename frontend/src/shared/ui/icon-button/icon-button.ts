import { Component, input, output } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-icon-button',
  imports: [MatButtonModule, MatIconModule],
  templateUrl: './icon-button.html',
})
export class IconButton {
  clicked = output<void>();
  fontIcon = input<string>('');
}
