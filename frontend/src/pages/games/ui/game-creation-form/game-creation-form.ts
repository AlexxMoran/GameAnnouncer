import { Component, inject, input, OnInit, output } from '@angular/core';
import { FormBuilder, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { TranslatePipe } from '@ngx-translate/core';
import { ICreateGameParams } from '@pages/games/model/game-creation-form.types';
import { IGame } from '@pages/games/model/game.types';
import { EGameCategories } from '@shared/api/games/games-api.constants';
import { Button } from '@shared/ui/button/button';
import { InputField } from '@shared/ui/input-field/input-field';
import { SelectField } from '@shared/ui/select-field/select-field';

@Component({
  selector: 'app-game-creation-form',
  imports: [
    ReactiveFormsModule,
    MatFormFieldModule,
    TranslatePipe,
    FormsModule,
    SelectField,
    InputField,
    Button,
  ],
  templateUrl: './game-creation-form.html',
  host: { class: 'w-full' },
})
export class GameCreationForm implements OnInit {
  private formBuilder = inject(FormBuilder);
  submitted = output<ICreateGameParams>();
  buttonText = input.required<string>();
  isLoading = input<boolean>(false);
  gameToUpdate = input<IGame>();

  createGameForm = this.formBuilder.group({
    name: [this.gameToUpdate()?.name || '', [Validators.required, Validators.maxLength(256)]],
    description: [
      this.gameToUpdate()?.description || '',
      [Validators.required, Validators.maxLength(256)],
    ],
    category: [this.gameToUpdate()?.category || null, [Validators.required]],
  });

  ngOnInit() {
    const gameToUpdate = this.gameToUpdate();

    if (gameToUpdate) {
      this.createGameForm.patchValue({
        name: gameToUpdate.name,
        description: gameToUpdate.description,
        category: gameToUpdate.category,
      });

      this.createGameForm.markAllAsTouched();
    }
  }

  get nameControl() {
    return this.createGameForm.controls['name'];
  }

  get descriptionControl() {
    return this.createGameForm.controls['description'];
  }

  get categoryControl() {
    return this.createGameForm.controls['category'];
  }

  get optionList() {
    return Object.entries(EGameCategories).map(([label, name]) => ({ label, name }));
  }

  get disabled() {
    return this.createGameForm.invalid;
  }

  submit() {
    if (this.createGameForm.invalid) {
      return;
    }

    const formData = this.createGameForm.value;

    const values = {
      name: formData.name || '',
      description: formData.description || '',
      category: formData.category || EGameCategories.RTS,
    };

    this.submitted.emit(values);
  }
}
