import { CommonModule } from '@angular/common';
import { Component, input } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatSelectModule } from '@angular/material/select';
import { TranslatePipe } from '@ngx-translate/core';
import { IOption } from '@shared/lib/utility-types/base-ui.types';

export interface IIconMenuOption<TName extends string = string> extends IOption<TName> {
  icon?: string;
  click?: (name?: TName) => void;
}

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
