import { Component, input } from '@angular/core';
import { IGame } from '@entities/game/model/game.types';
import { TranslatePipe } from '@ngx-translate/core';
import { environment } from '@shared/config/environments/environment';
import { StyleFactory } from '@shared/lib/style-factory/style-factory.service';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { Button } from '@shared/ui/button/button';

@Component({
  selector: 'game-card',
  templateUrl: './game-card.html',
  styleUrl: './game-card.scss',
  imports: [TranslatePipe, Button],
  host: { '[class]': 'cardClasses' },
})
export class GameCard {
  game = input<TMaybe<IGame>>(null);

  get getBackgroundImageProperty() {
    const url = this.game()?.image_url;

    return url ? `url(${environment.apiUrl}${url})` : undefined;
  }

  get cardClasses() {
    return StyleFactory.card({ bg: 'container-low', shadow: 'shadow-xl', classes: 'h-95 p-1' });
  }
}
