import { CommonModule } from '@angular/common';
import { Component, input, model } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatSelectModule } from '@angular/material/select';
import { TranslatePipe } from '@ngx-translate/core';
import { IIconMenuOption } from '@shared/ui/actions-menu/actions-menu.types';

@Component({
  selector: 'app-actions-menu',
  imports: [
    MatIconModule,
    MatMenuModule,
    MatButtonModule,
    CommonModule,
    MatSelectModule,
    TranslatePipe,
  ],
  templateUrl: './actions-menu.html',
})
export class ActionsMenu<TName extends string> {
  selectedOptionName = model<TName | undefined>(undefined);
  optionList = input<IIconMenuOption<TName>[]>([]);
  text = input('');
  icon = input('');
}
