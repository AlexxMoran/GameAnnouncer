import { Directive, inject, ViewContainerRef } from '@angular/core';

@Directive({
  selector: '[dynamicComponent]',
})
export class DynamicComponentDirective {
  viewContainerRef = inject(ViewContainerRef);
}
