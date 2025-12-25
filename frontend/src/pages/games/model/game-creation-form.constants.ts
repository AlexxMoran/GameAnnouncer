import { Validators } from '@angular/forms';
import { EGameCategories } from '@shared/api/games/games-api.constants';

const GAME_CATEGORY_LIST = Object.entries(EGameCategories).map(([label, name]) => ({
  label,
  name,
}));

const GAME_CREATION_FORM_FIELD_LIST = [
  { type: 'input' as const, name: 'name' as const, label: 'entities.name', required: true },
  {
    type: 'input' as const,
    name: 'description' as const,
    label: 'entities.description',
    required: true,
    isTextarea: true,
  },
  {
    type: 'select' as const,
    name: 'category' as const,
    label: 'entities.category',
    required: true,
    optionList: GAME_CATEGORY_LIST,
  },
];

const GAME_CREATION_FORM_CONTROLS = {
  name: ['', [Validators.required, Validators.maxLength(256)]],
  description: ['', [Validators.required, Validators.maxLength(256)]],
  category: ['' as EGameCategories, [Validators.required]],
};

export const GAME_CREATION_FORM_INPUTS = {
  controls: GAME_CREATION_FORM_CONTROLS,
  formFieldList: GAME_CREATION_FORM_FIELD_LIST,
};
