import type { ReactCropperProps } from 'react-cropper';

export interface IImageCropperProps extends ReactCropperProps {
  imageSizeRestrictionMb?: number;
}
