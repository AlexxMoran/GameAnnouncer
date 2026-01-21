import { Component, input, output } from '@angular/core';
import { IAnnouncementDto } from '@shared/api/announcements/announcements-api-service.types';
import { StyleFactory } from '@shared/lib/styles/style-factory.service';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { Button } from '@shared/ui/button/button';

@Component({
  selector: 'app-announcement-card',
  imports: [Button],
  templateUrl: './announcement-card.html',
  host: { '[class]': 'cardClasses' },
})
export class AnnouncementCard {
  readonly announcement = input<TMaybe<IAnnouncementDto>>();
  readonly buttonClicked = output();

  get cardClasses() {
    return StyleFactory.card({ bg: 'container-low', shadow: 'shadow-xl', classes: 'h-95 p-1' });
  }

  clickButton = () => {
    this.buttonClicked.emit();
  };
}
