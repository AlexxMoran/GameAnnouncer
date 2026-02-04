import type { IImageUploadFormProps } from "@pages/games/ul/image-upload-form/type";
import type { TMaybe } from "@shared/types/main.types";
import { Box } from "@shared/ui/box";
import { Button } from "@shared/ui/button";
import { ImageCropper } from "@shared/ui/image-cropper";
import type { TFunction } from "i18next";
import { useSnackbar, type EnqueueSnackbar } from "notistack";
import { useRef, useState, type FC, type RefObject } from "react";
import type { ReactCropperElement } from "react-cropper";
import { useTranslation } from "react-i18next";
import { v4 as uuidv4 } from "uuid";

const convertRefToFile = async (
  ref: RefObject<TMaybe<ReactCropperElement>>,
  enqueueSnackbar: EnqueueSnackbar,
  t: TFunction,
  fileName?: string
) => {
  try {
    const base64Url = ref.current?.cropper.getCroppedCanvas().toDataURL();

    if (base64Url) {
      const result = await fetch(base64Url);
      const blob = await result.blob();
      const type = blob.type.split("/")[1];

      return new File([blob], `${fileName || uuidv4()}.${type}`, {
        lastModified: Date.now(),
        type,
      });
    } else {
      enqueueSnackbar(t("validationErrors.needToSelectImage"), { variant: "error" });
    }
  } catch (_) {
    enqueueSnackbar(t("validationErrors.failConvertFile"), { variant: "error" });
  }
};

export const ImageUploadForm: FC<IImageUploadFormProps> = ({ onUploadImage, fileName }) => {
  const { enqueueSnackbar } = useSnackbar();
  const { t } = useTranslation();
  const cropperRef = useRef<ReactCropperElement>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    setIsLoading(true);

    try {
      const file = await convertRefToFile(cropperRef, enqueueSnackbar, t, fileName);

      if (file) {
        await onUploadImage?.(file);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box display="flex" flexDirection="column" gap={10}>
      <ImageCropper ref={cropperRef} aspectRatio={37 / 16} />
      <Button onClick={handleSubmit} loading={isLoading}>
        {t("actions.upload")}
      </Button>
    </Box>
  );
};
