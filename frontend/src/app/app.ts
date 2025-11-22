import { Component } from '@angular/core';
import { AppLayout } from '@app/app-layout/app-layout';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  imports: [AppLayout],
  styleUrl: './app.scss',
  host: {
    class: 'w-full h-full flex flex-col',
  },
})
export class App {}
