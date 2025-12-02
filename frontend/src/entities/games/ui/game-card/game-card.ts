import { Component, input } from '@angular/core';
import { IGame } from '@entities/games/model/game.types';
import { TranslatePipe } from '@ngx-translate/core';
import { environment } from '@shared/config/environments/environment';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { Button } from '@shared/ui/button/button';

@Component({
  selector: 'game-card',
  templateUrl: './game-card.html',
  styleUrl: './game-card.scss',
  imports: [TranslatePipe, Button],
  host: { class: 'h-95 flex flex-col rounded-3xl p-1 overflow-hidden' },
})
export class GameCard {
  game = input<TMaybe<IGame>>(null);

  get getBackgroundImageProperty() {
    const url = this.game()?.image_url;

    return url ? `url(${environment.apiUrl}${url})` : undefined;
  }
}
