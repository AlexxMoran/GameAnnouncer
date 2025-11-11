import { Component } from '@angular/core';
import { ActionsMenu } from 'src/components/actions-menu/actions-menu';

import { inject } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { LANG_STORAGE_NAME } from 'src/app/lang-toggle/lang-toggle.constants';
import { TLang } from 'src/app/lang-toggle/lang-toggle.types';
import { IIconMenuOption } from 'src/components/actions-menu/actions-menu.types';
import translationsEn from '../../../public/i18n/en.json';
import translationsRu from '../../../public/i18n/ru.json';

@Component({
  selector: 'lang-toggle',
  template: `<ui-actions-menu
    [optionList]="optionList"
    [icon]="icon"
    [selectedOptionName]="currentLang"
    (selectedOptionNameChange)="changeLang($event)"
  />`,
  imports: [ActionsMenu],
})
export class LangToggle {
  translate = inject(TranslateService);
  optionList: IIconMenuOption<TLang>[] = [
    { name: 'ru', label: 'lang.ru' },
    { name: 'en', label: 'lang.en' },
  ];
  icon = 'language';

  constructor() {
    this.translate.setTranslation('en', translationsEn);
    this.translate.setTranslation('ru', translationsRu);
    this.translate.addLangs(['ru', 'en']);
    this.translate.setFallbackLang('ru');
    this.translate.use(this.currentLang);
  }

  get currentLang(): TLang {
    return (localStorage.getItem(LANG_STORAGE_NAME) as TLang) || 'ru';
  }

  changeLang(lang?: TLang) {
    if (lang) {
      localStorage.setItem(LANG_STORAGE_NAME, lang);
      this.translate.use(lang);
    }
  }
}
