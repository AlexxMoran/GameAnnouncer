import { Component, inject, input, signal } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { MatInputModule } from '@angular/material/input';
import { TranslatePipe, TranslateService } from '@ngx-translate/core';
import { SnackBarService } from '@shared/lib/snack-bar/snack-bar.service';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { Button } from '@shared/ui/button/button';
import { TCreateUploadObservable } from '@shared/ui/image-cropper/image-cropper.types';
import { ImageCroppedEvent, ImageCropperComponent } from 'ngx-image-cropper';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-image-cropper',
  imports: [ImageCropperComponent, Button, TranslatePipe, MatInputModule],
  templateUrl: './image-cropper.html',
  host: { class: 'flex flex-col items-start justify-center gap-8 min-h-25 max-w-130 w-full' },
})
export class ImageCropper {
  readonly MAX_FILE_SIZE_MB = 2;
  readonly MAX_FILE_SIZE_B = this.MAX_FILE_SIZE_MB * 1024 * 1024;
  readonly ALLOWED_FILE_FORMATS = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];

  private dialogRef = inject(MatDialogRef);
  private translateService = inject(TranslateService);
  private snackBarService = inject(SnackBarService);

  readonly createUploadObserver = input<TCreateUploadObservable>();
  readonly buttonText = input('');

  readonly isLoading = signal(false);

  imageChangedEvent: TMaybe<Event> = null;
  croppedImageBlob: TMaybe<Blob> = null;

  get allowedFileAccept(): string {
    return this.ALLOWED_FILE_FORMATS.map((type) => type.replace('image/', ''))
      .map((ext) => `.${ext}`)
      .join(', ');
  }

  get imageUploadTooltip() {
    return this.translateService.instant('texts.fileUploadTooltip', {
      formats: this.allowedFileAccept,
      size: this.MAX_FILE_SIZE_MB,
    });
  }

  fileChangeEvent(imageChangedEvent: Event) {
    const input = imageChangedEvent.target as HTMLInputElement;

    if (!input.files || input.files.length === 0 || input.files.length > 1) {
      return;
    }

    const file = input.files[0];

    if (!this.ALLOWED_FILE_FORMATS.includes(file.type)) {
      this.snackBarService.showErrorSnackBar(
        this.translateService.instant('validationErrors.incorrectFileFormat'),
      );

      return;
    }

    if (file.size > this.MAX_FILE_SIZE_B) {
      this.snackBarService.showErrorSnackBar(
        this.translateService.instant('validationErrors.incorrectFileSize'),
      );

      return;
    }

    this.imageChangedEvent = imageChangedEvent;
  }

  imageCropped(event: ImageCroppedEvent) {
    if (event.blob) {
      this.croppedImageBlob = event.blob;
    }
  }

  convertBlobToFile() {
    if (this.croppedImageBlob) {
      const fileType = this.croppedImageBlob.type || 'image/png';
      const extension = fileType.split('/')[1] || 'png';

      const file = new File([this.croppedImageBlob], `cropped-image.${extension}`, {
        type: fileType,
        lastModified: Date.now(),
      });

      return file;
    }

    return;
  }

  uploadImage() {
    const createUploadObserver = this.createUploadObserver();

    if (createUploadObserver) {
      const file = this.convertBlobToFile();

      if (file) {
        this.isLoading.set(true);
        const observer = createUploadObserver?.(file);

        observer
          .pipe(finalize(() => this.isLoading.set(false)))
          .subscribe(() => this.dialogRef.close());
      }
    }
  }
}
