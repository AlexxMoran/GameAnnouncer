import { CreateAnnouncementFields } from "@pages/announcements/ui/create-announcement-fields";
import type { ICreateAnnouncementFormProps } from "@pages/announcements/ui/create-announcement-form/types";
import { createValidationSchema } from "@pages/games/model/create-validation-schema";
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
    game_id: "",
    start_at: "",
    registration_start_at: "",
    registration_end_at: "",
    max_participants: 0,
  };

  const validationSchema = createValidationSchema(t);

  return (
    <Form
      onSubmit={(values) => onSubmit?.(values)}
      formikConfig={{ initialValues, validationSchema }}
      fields={CreateAnnouncementFields}
      buttonText={t("actions.add")}
      wrapperStyles={{ minWidth: "400px" }}
    />
  );
};
