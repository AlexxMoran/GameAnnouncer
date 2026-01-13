import { Validators } from '@angular/forms';
import {
  ICreateAnnouncementParams,
  IEditAnnouncementParams,
} from '@pages/announcements/model/announcement-creation-form.types';
import { TFormField, TGroupControls } from '@shared/ui/form/form.types';

const ANNOUNCEMENT_CREATION_FORM_FIELD_LIST: TFormField<ICreateAnnouncementParams>[] = [
  { type: 'input' as const, name: 'title' as const, label: 'entities.name' },
  {
    type: 'input' as const,
    name: 'content' as const,
    label: 'entities.description',
    isTextarea: true,
  },
  {
    type: 'input' as const,
    name: 'game_id' as const,
    label: 'entities.description',
    isTextarea: true,
  },
];

const COMMON_CONTROLS = {
  title: ['', [Validators.required, Validators.maxLength(64)]],
  content: ['', [Validators.required, Validators.maxLength(256)]],
};

const ANNOUNCEMENT_CREATION_FORM_CONTROLS: TGroupControls<ICreateAnnouncementParams> = {
  ...COMMON_CONTROLS,
  game_id: ['', [Validators.required]],
};

const ANNOUNCEMENT_EDITING_FORM_CONTROLS: TGroupControls<IEditAnnouncementParams> = {
  ...COMMON_CONTROLS,
};

export const ANNOUNCEMENT_CREATION_FORM_INPUTS = {
  controls: ANNOUNCEMENT_CREATION_FORM_CONTROLS,
  formFieldList: ANNOUNCEMENT_CREATION_FORM_FIELD_LIST,
};

export const ANNOUNCEMENT_EDITING_FORM_INPUTS = {
  controls: ANNOUNCEMENT_EDITING_FORM_CONTROLS,
  formFieldList: ANNOUNCEMENT_CREATION_FORM_FIELD_LIST,
};
