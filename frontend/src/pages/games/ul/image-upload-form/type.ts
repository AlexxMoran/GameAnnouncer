export interface IImageUploadFormProps {
  onUploadImage?: (file: File) => Promise<void>;
  fileName?: string;
}
