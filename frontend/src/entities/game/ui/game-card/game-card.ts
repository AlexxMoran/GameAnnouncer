import { Component, input } from '@angular/core';
import { IGame } from '@entities/game/model/game.types';
import { TranslatePipe } from '@ngx-translate/core';
import { environment } from '@shared/config/environments/environment';
import { StyleFactory } from '@shared/lib/style-factory/style-factory.service';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { Button } from '@shared/ui/button/button';
import { IIconMenuOption, Menu } from '@shared/ui/menu/menu';

@Component({
  selector: 'app-game-card',
  templateUrl: './game-card.html',
  styleUrl: './game-card.scss',
  imports: [TranslatePipe, Button, Menu],
  host: { '[class]': 'cardClasses' },
})
export class GameCard {
  game = input<TMaybe<IGame>>(null);
  gameActionList = input<IIconMenuOption[]>([]);

  get getBackgroundImageProperty() {
    const url = this.game()?.image_url;

    return url ? `url(${environment.apiUrl}${url})` : undefined;
  }

  get cardClasses() {
    return StyleFactory.card({ bg: 'container-low', shadow: 'shadow-xl', classes: 'h-95 p-1' });
  }
}
