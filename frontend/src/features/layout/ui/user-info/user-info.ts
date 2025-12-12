import { Component, inject } from '@angular/core';
import { MatTooltipModule } from '@angular/material/tooltip';
import { AuthService } from '@shared/lib/auth/auth.service';
import { Menu } from '@shared/ui/menu/menu';
import { IIconMenuOption } from '@shared/ui/menu/menu.types';

@Component({
  selector: 'app-user-info',
  imports: [Menu, MatTooltipModule],
  templateUrl: './user-info.html',
})
export class UserInfo {
  private authService = inject(AuthService);

  get optionList(): IIconMenuOption[] {
    return [{ name: 'logout', label: 'actions.logout', click: this.logout }];
  }

  get me() {
    return this.authService.me();
  }

  get email() {
    return this.me?.email || '';
  }

  logout = () => {
    this.authService.logout();
  };
}
