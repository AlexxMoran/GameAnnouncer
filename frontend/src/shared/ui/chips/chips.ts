import { Component, input, output, signal } from '@angular/core';
import { MatChipsModule } from '@angular/material/chips';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { IChip } from '@shared/ui/chips/chips.types';

@Component({
  selector: 'app-chips',
  imports: [MatChipsModule],
  templateUrl: './chips.html',
  host: { class: 'block' },
})
export class Chips {
  selected = output<TMaybe<string>>();
  chipList = input<IChip[]>([]);
  selectedChip = signal<TMaybe<IChip>>(null);

  selectChip(selectedChip: IChip) {
    if (this.selectedChip()?.name === selectedChip.name) {
      this.selectedChip.set(null);
      this.selected.emit(null);

      return;
    }

    this.selected.emit(selectedChip.name);
    this.selectedChip.set(selectedChip);
  }

  isSelected(chip: IChip) {
    return Boolean(this.selectedChip()?.name === chip.name);
  }
}
