import { createValidationSchema } from "@pages/games/model/create-validation-schema";
import { CreateGameFields } from "@pages/games/ul/create-game-fields";
import type { ICreateGameFormProps } from "@pages/games/ul/create-game-form/types";
import { useDialog } from "@shared/hooks/use-dialog";
import { EGameCategories } from "@shared/services/api/games-api-service/constants";
import { Form } from "@shared/ui/form";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const CreateGameForm: FC<ICreateGameFormProps> = (props) => {
  const { onSubmit, initialValues: values } = props;
  const { closeDialog } = useDialog();

  const { t } = useTranslation();

  const initialValues = values || {
    name: "",
    description: "",
    category: EGameCategories["RTS"],
  };

  const validationSchema = createValidationSchema(t);

  return (
    <Form
      onSubmit={(values) => onSubmit?.(values)}
      onCancel={closeDialog}
      formikConfig={{ initialValues, validationSchema }}
      fields={CreateGameFields}
      confirmButtonText={t(`actions.${values ? "save" : "add"}`)}
      isForDialog
    />
  );
};
