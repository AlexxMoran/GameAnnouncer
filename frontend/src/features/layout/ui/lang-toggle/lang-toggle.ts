import { Component, inject } from '@angular/core';
import { MatTooltipModule } from '@angular/material/tooltip';
import { LANG_STORAGE_KEY } from '@features/layout/ui/lang-toggle/lang-toggle.constants';
import { TLang } from '@features/layout/ui/lang-toggle/lang-toggle.types';
import { TranslatePipe, TranslateService } from '@ngx-translate/core';
import translationsEn from '@shared/i18n/en.json';
import translationsRu from '@shared/i18n/ru.json';
import { Menu } from '@shared/ui/menu/menu';
import { IIconMenuOption } from '@shared/ui/menu/menu.types';

@Component({
  selector: 'lang-toggle',
  template: `<app-menu
    [matTooltip]="'actions.changeLanguage' | translate"
    [optionList]="optionList"
    [icon]="'language'"
  />`,
  imports: [Menu, MatTooltipModule, TranslatePipe],
})
export class LangToggle {
  translate = inject(TranslateService);

  constructor() {
    this.translate.setTranslation('en', translationsEn);
    this.translate.setTranslation('ru', translationsRu);
    this.translate.addLangs(['ru', 'en']);
    this.translate.setFallbackLang('ru');
    this.translate.use(this.currentLang);
  }

  get optionList(): IIconMenuOption<TLang>[] {
    return [
      { name: 'ru', label: 'lang.ru', click: this.changeLang },
      { name: 'en', label: 'lang.en', click: this.changeLang },
    ];
  }

  get currentLang(): TLang {
    return (localStorage.getItem(LANG_STORAGE_KEY) as TLang) || 'ru';
  }

  changeLang = (lang?: TLang) => {
    if (lang) {
      localStorage.setItem(LANG_STORAGE_KEY, lang);
      this.translate.use(lang);
    }
  };
}
