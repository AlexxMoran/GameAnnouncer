import {
  Component,
  inject,
  inputBinding,
  OnInit,
  outputBinding,
  ViewChild,
  WritableSignal,
} from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { TranslatePipe } from '@ngx-translate/core';
import { DynamicComponentDirective } from '@shared/directives/dynamic-component.directive';
import { IDialogData } from '@shared/ui/dialog-wrapper/dialog-wrapper.types';
import { IconButton } from '@shared/ui/icon-button/icon-button';

@Component({
  selector: 'app-dialog-wrapper',
  imports: [IconButton, TranslatePipe, DynamicComponentDirective],
  templateUrl: './dialog-wrapper.html',
})
export class DialogWrapper<TComponent> implements OnInit {
  @ViewChild(DynamicComponentDirective, { static: true })
  dialogContent!: DynamicComponentDirective;

  readonly dialogData = inject<IDialogData<TComponent>>(MAT_DIALOG_DATA);
  readonly dialogRef = inject(MatDialogRef);

  readonly component = this.dialogData.component;
  readonly inputs = this.dialogData.options.inputs;
  readonly outputs = this.dialogData.options.outputs;
  readonly title = this.dialogData.options.title;

  ngOnInit() {
    const vcr = this.dialogContent.viewContainerRef;

    const inputBindingList = Object.entries(this.inputs || {}).map(([key, value]) =>
      inputBinding(
        key,
        typeof value === 'function' ? (value as WritableSignal<unknown>) : () => value,
      ),
    );

    const outputBindingList = Object.entries(this.outputs || {}).map(([key, callback]) =>
      outputBinding(key, (event) => (callback as (params: unknown) => void)(event)),
    );

    vcr.createComponent<TComponent>(this.component, {
      bindings: [...inputBindingList, ...outputBindingList],
    });
  }

  closeDialog = () => {
    this.dialogRef.close();
  };
}
