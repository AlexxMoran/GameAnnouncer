import {
  Component,
  Directive,
  inject,
  inputBinding,
  OnInit,
  outputBinding,
  Type,
  ViewChild,
  ViewContainerRef,
  WritableSignal,
} from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { TranslatePipe } from '@ngx-translate/core';
import { TExtractInputs, TExtractOutputs } from '@shared/lib/utility-types/extract-component.types';
import { IconButton } from '@shared/ui/icon-button/icon-button';

export interface IOpenDialogOptions<TComponent> {
  title: string;
  inputs?: TExtractInputs<TComponent>;
  outputs?: TExtractOutputs<TComponent>;
}

export interface IDialogData<TComponent> {
  component: Type<TComponent>;
  options: IOpenDialogOptions<TComponent>;
}

@Directive({
  selector: '[dynamicComponentLoader]',
})
export class DialogContentDirective {
  viewContainerRef = inject(ViewContainerRef);
}

@Component({
  selector: 'app-dialog-wrapper',
  imports: [IconButton, DialogContentDirective, TranslatePipe],
  templateUrl: './dialog-wrapper.html',
})
export class DialogWrapper<TComponent> implements OnInit {
  @ViewChild(DialogContentDirective, { static: true })
  dialogContent!: DialogContentDirective;

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
