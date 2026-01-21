import { Component, input, output } from '@angular/core';
import { TranslatePipe } from '@ngx-translate/core';
import { IGame } from '@pages/games/model/game.types';
import { environment } from '@shared/config/environments/environment';
import { StyleFactory } from '@shared/lib/styles/style-factory.service';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { Button } from '@shared/ui/button/button';
import { Menu } from '@shared/ui/menu/menu';
import { IIconMenuOption } from '@shared/ui/menu/menu.types';

@Component({
  selector: 'app-game-card',
  templateUrl: './game-card.html',
  styleUrl: './game-card.scss',
  imports: [TranslatePipe, Button, Menu],
  host: { '[class]': 'cardClasses' },
})
export class GameCard {
  readonly game = input<TMaybe<IGame>>(null);
  readonly gameActionList = input<IIconMenuOption[]>([]);
  readonly buttonClicked = output();

  get getBackgroundImageProperty() {
    const url = this.game()?.image_url;

    return url ? `url(${environment.apiUrl}${url})` : undefined;
  }

  get cardClasses() {
    return StyleFactory.card({ bg: 'container-low', shadow: 'shadow-xl', classes: 'h-95 p-1' });
  }

  redirectToAnnouncement = () => {
    this.buttonClicked.emit();
  };
}
