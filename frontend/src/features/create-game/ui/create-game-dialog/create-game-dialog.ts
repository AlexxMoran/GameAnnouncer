import { Component, inject, WritableSignal } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ICreateGameParams } from '@features/create-game/model/create-game-form.types';
import { CreateGameForm } from '@features/create-game/ui/create-game-form/create-game-form';
import { TranslatePipe } from '@ngx-translate/core';
import { DialogWrapper } from '@shared/ui/dialog-wrapper/dialog-wrapper';

export interface IDialogData {
  submit: (values: ICreateGameParams) => void;
  isLoading: WritableSignal<boolean>;
}

@Component({
  selector: 'app-create-game-dialog',
  imports: [DialogWrapper, CreateGameForm, TranslatePipe],
  templateUrl: './create-game-dialog.html',
})
export class CreateGameDialog {
  readonly dialogData = inject<IDialogData>(MAT_DIALOG_DATA);

  submit = (values: ICreateGameParams) => {
    this.dialogData.submit(values);
  };
}
