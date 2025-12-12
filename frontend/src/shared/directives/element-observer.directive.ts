import { Directive, ElementRef, inject, OnDestroy, output } from '@angular/core';

@Directive({
  selector: '[elementObserver]',
})
export class ElementObserverDirective implements OnDestroy {
  elementReached = output();

  private observer: IntersectionObserver;
  private element = inject(ElementRef);

  constructor() {
    this.observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          this.elementReached.emit();
        }
      },
      {
        threshold: 0.1,
      },
    );

    this.observer.observe(this.element.nativeElement);
  }

  ngOnDestroy() {
    this.observer.disconnect();
  }
}
