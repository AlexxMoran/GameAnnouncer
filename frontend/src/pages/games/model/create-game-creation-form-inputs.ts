import { FormControl, Validators } from '@angular/forms';
import {
  COMMON_CONTROLS,
  GAME_CREATION_FORM_FIELD_LIST,
} from '@pages/games/model/game-creation-form.constants';
import { ICreateGameParams } from '@pages/games/model/game-creation-form.types';
import { EGameCategories } from '@shared/api/games/games-api-service.constants';

import { TGroupControls } from '@shared/ui/form/form.types';

export const createGameCreationFormInputs = () => {
  const GAME_CREATION_FORM_CONTROLS: TGroupControls<ICreateGameParams> = {
    ...COMMON_CONTROLS,
    category: new FormControl({ value: '' as EGameCategories, disabled: false }, [
      Validators.required,
    ]),
  };

  return {
    controls: GAME_CREATION_FORM_CONTROLS,
    formFieldList: GAME_CREATION_FORM_FIELD_LIST,
  };
};
