import { Validators } from '@angular/forms';
import { ICreateGameParams } from '@pages/games/model/game-creation-form.types';
import { EGameCategories } from '@shared/api/games/games-api.constants';
import { TFormField } from '@shared/ui/form/form.types';

export const GAME_CATEGORY_LIST = Object.entries(EGameCategories).map(([label, name]) => ({
  label,
  name,
}));

export const GAME_CREATION_FORM_FIELD_LIST: TFormField<ICreateGameParams>[] = [
  { type: 'input' as const, name: 'name' as const, label: 'entities.name' },
  {
    type: 'input' as const,
    name: 'description' as const,
    label: 'entities.description',
    isTextarea: true,
  },
  {
    type: 'select' as const,
    name: 'category' as const,
    label: 'entities.category',
    optionList: GAME_CATEGORY_LIST,
  },
];

export const COMMON_CONTROLS = {
  name: ['', [Validators.required, Validators.maxLength(256)]],
  description: ['', [Validators.required, Validators.maxLength(256)]],
};
