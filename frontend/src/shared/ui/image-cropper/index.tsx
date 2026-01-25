import { Box } from '@shared/ui/box';
import {
  ALLOWED_IMAGE_FORMATS,
  DEFAULT_IMAGE_SIZE_RESTRICTION_MB,
} from '@shared/ui/image-cropper/constants';
import type { IImageCropperProps } from '@shared/ui/image-cropper/types';
import { T } from '@shared/ui/typography';
import 'cropperjs/dist/cropper.css';
import { useSnackbar } from 'notistack';
import { forwardRef, useState, type ChangeEvent } from 'react';
import Cropper, { type ReactCropperElement } from 'react-cropper';
import { useTranslation } from 'react-i18next';

export const ImageCropper = forwardRef<ReactCropperElement, IImageCropperProps>((props, ref) => {
  const { imageSizeRestrictionMb = DEFAULT_IMAGE_SIZE_RESTRICTION_MB, ...rest } = props;

  const [image, setImage] = useState<string | undefined>();
  const { enqueueSnackbar } = useSnackbar();
  const { t } = useTranslation();

  const allowedFileAccept = ALLOWED_IMAGE_FORMATS.map((type) => type.replace('image/', ''))
    .map((ext) => `.${ext}`)
    .join(', ');

  const imageUploadTooltip = t('texts.fileUploadTooltip', {
    size: imageSizeRestrictionMb,
    formats: allowedFileAccept,
  });

  const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
    const fileList = Array.from(event.target.files || []);

    if (fileList.length > 1) {
      enqueueSnackbar(t('validationErrors.incorrectFileCount', { variant: 'error' }));
    } else if (fileList.length === 1) {
      const newImage = fileList[0];

      if (newImage.size > imageSizeRestrictionMb * Math.pow(10, 6)) {
        enqueueSnackbar(t('validationErrors.incorrectFileSize'), { variant: 'error' });
      } else if (!ALLOWED_IMAGE_FORMATS.includes(newImage.type)) {
        enqueueSnackbar(t('validationErrors.incorrectFileFormat'), { variant: 'error' });
      } else {
        const reader = new FileReader();

        reader.onload = () => {
          if (typeof reader.result === 'string') {
            setImage(reader.result);
          }
        };

        reader.readAsDataURL(newImage);
      }
    }
  };

  return image ? (
    <Cropper
      src={image}
      viewMode={2}
      minCropBoxWidth={100}
      ref={ref}
      guides={false}
      checkOrientation={false}
      background={false}
      movable={false}
      rotatable={false}
      scalable={false}
      {...rest}
    />
  ) : (
    <Box display="flex" flexDirection="column" gap={4}>
      <input type="file" onChange={handleInputChange} accept={ALLOWED_IMAGE_FORMATS.join(', ')} />
      <T variant="caption">{imageUploadTooltip}</T>
    </Box>
  );
});
