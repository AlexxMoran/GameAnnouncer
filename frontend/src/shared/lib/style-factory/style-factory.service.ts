interface ICardVariants {
  bg?: 'none' | 'container-low';
  border?: 'none' | 'outline';
  shadow?: 'none' | 'shadow-sm' | 'shadow-xl';
  classes?: string;
}

export class StyleFactory {
  private static readonly classes = {
    card: {
      base: 'flex flex-col relative overflow-hidden rounded-3xl',
      bg: {
        none: '',
        'container-low': 'bg-[var(--mat-sys-surface-container-low)]',
      },
      border: {
        none: '',
        outline: 'border border-[var(--mat-sys-outline)]',
      },
      shadow: {
        none: '',
        'shadow-sm': 'shadow-sm',
        'shadow-md': 'shadow-md',
        'shadow-lg': 'shadow-lg',
        'shadow-xl': 'shadow-xl',
      },
    },
  } as const;

  static card(variants?: ICardVariants) {
    const { bg = 'none', border = 'none', shadow = 'none', classes = '' } = variants || {};

    const classList = [
      classes,
      this.classes.card.base,
      this.classes.card.bg[bg],
      this.classes.card.border[border],
      this.classes.card.shadow[shadow],
    ];

    return classList.join(' ');
  }
}
