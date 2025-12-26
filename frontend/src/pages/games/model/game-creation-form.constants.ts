import { FormControl, Validators } from '@angular/forms';
import { ICreateGameParams, IEditGameParams } from '@pages/games/model/game-creation-form.types';
import { EGameCategories } from '@shared/api/games/games-api.constants';
import { TFormField, TGroupControls } from '@shared/ui/form/form.types';

const GAME_CATEGORY_LIST = Object.entries(EGameCategories).map(([label, name]) => ({
  label,
  name,
}));

const GAME_CREATION_FORM_FIELD_LIST: TFormField<ICreateGameParams>[] = [
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

const COMMON_CONTROLS = {
  name: ['', [Validators.required, Validators.maxLength(256)]],
  description: ['', [Validators.required, Validators.maxLength(256)]],
};

const GAME_CREATION_FORM_CONTROLS: TGroupControls<ICreateGameParams> = {
  ...COMMON_CONTROLS,
  category: new FormControl({ value: '' as EGameCategories, disabled: false }, [
    Validators.required,
  ]),
};

const GAME_EDITING_FORM_CONTROLS: TGroupControls<IEditGameParams> = {
  ...COMMON_CONTROLS,
  category: new FormControl({ value: '' as EGameCategories, disabled: true }, [
    Validators.required,
  ]),
};

export const GAME_CREATION_FORM_INPUTS = {
  controls: GAME_CREATION_FORM_CONTROLS,
  formFieldList: GAME_CREATION_FORM_FIELD_LIST,
};

export const GAME_EDITING_FORM_INPUTS = {
  controls: GAME_EDITING_FORM_CONTROLS,
  formFieldList: GAME_CREATION_FORM_FIELD_LIST,
};
