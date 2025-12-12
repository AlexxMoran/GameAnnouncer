import { CommonModule } from '@angular/common';
import { Component, input } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatSelectModule } from '@angular/material/select';
import { TranslatePipe } from '@ngx-translate/core';
import { IIconMenuOption } from '@shared/ui/menu/menu.types';

@Component({
  selector: 'app-menu',
  imports: [
    MatIconModule,
    MatMenuModule,
    MatButtonModule,
    CommonModule,
    MatSelectModule,
    TranslatePipe,
  ],
  templateUrl: './menu.html',
})
export class Menu<TName extends string> {
  optionList = input<IIconMenuOption<TName>[]>([]);
  text = input('');
  icon = input('');
}
