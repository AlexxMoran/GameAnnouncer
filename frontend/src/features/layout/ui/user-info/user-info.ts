import { Component, inject, input } from '@angular/core';
import { MatTooltipModule } from '@angular/material/tooltip';
import { IUserDto } from '@shared/api/users/users-api.types';
import { AuthService } from '@shared/lib/auth/auth.service';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { Menu } from '@shared/ui/menu/menu';

@Component({
  selector: 'app-user-info',
  imports: [Menu, MatTooltipModule],
  templateUrl: './user-info.html',
})
export class UserInfo {
  private authService = inject(AuthService);
  me = input<TMaybe<IUserDto>>(null);

  get optionList() {
    return [{ name: 'logout', label: 'actions.logout', click: this.logout }];
  }

  get email() {
    return this.me()?.email || '';
  }

  logout = () => {
    this.authService.logout();
  };
}
