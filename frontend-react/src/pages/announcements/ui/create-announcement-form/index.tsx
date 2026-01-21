import { createValidationSchema } from "@pages/announcements/model/create-validation-schema";
import type { ICreateAnnouncementsFields } from "@pages/announcements/model/create-validation-schema/types";
import { CreateAnnouncementFields } from "@pages/announcements/ui/create-announcement-fields";
import type { ICreateAnnouncementFormProps } from "@pages/announcements/ui/create-announcement-form/types";
import { Form } from "@shared/ui/form";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const CreateAnnouncementForm: FC<ICreateAnnouncementFormProps> = (
  props
) => {
  const { onSubmit } = props;

  const { t } = useTranslation();

  const initialValues = {
    title: "",
    content: "",
    game: null,
    start_at: "",
    registration_start_at: "",
    registration_end_at: "",
    max_participants: 0,
  };

  const validationSchema = createValidationSchema(t);

  const handleSubmit = async ({
    game,
    ...rest
  }: ICreateAnnouncementsFields) => {
    if (game) {
      await onSubmit?.({ ...rest, game_id: game.id });
    }
  };

  return (
    <Form
      onSubmit={handleSubmit}
      formikConfig={{ initialValues, validationSchema }}
      fields={CreateAnnouncementFields}
      buttonText={t("actions.add")}
      wrapperStyles={{ minWidth: "400px" }}
    />
  );
};
