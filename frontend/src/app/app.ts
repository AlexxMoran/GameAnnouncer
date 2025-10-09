import { Component, signal } from '@angular/core';
import { MatButtonToggleModule } from '@angular/material/button-toggle';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  imports: [MatButtonToggleModule],
})
export class App {
  protected readonly title = signal('frontend');
}
