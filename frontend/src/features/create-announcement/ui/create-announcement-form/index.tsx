import { createValidationSchema } from "@features/create-announcement/model/create-validation-schema";
import type { ICreateAnnouncementsFields } from "@features/create-announcement/model/create-validation-schema/types";
import { validateRegistrationFormFields } from "@features/create-announcement/model/validate-registration-form-fields";
import type { IRegistrationFormFields } from "@features/create-announcement/model/validate-registration-form-fields/types";
import { AnnouncementInfoFields } from "@features/create-announcement/ui/announcement-info-fields";
import type { ICreateAnnouncementFormProps } from "@features/create-announcement/ui/create-announcement-form/types";
import { RegistrationFormFields } from "@features/create-announcement/ui/registration-form-fields";
import { useDialog } from "@shared/hooks/use-dialog";
import { EAnnouncementFormat } from "@shared/services/api/announcements-api-service/constants";
import type { TMaybe } from "@shared/types/main.types";
import { Box } from "@shared/ui/box";
import { Form } from "@shared/ui/form";
import { Stepper } from "@shared/ui/stepper";
import { T } from "@shared/ui/typography";
import isEmpty from "lodash/isEmpty";
import { useState, type FC } from "react";
import { useTranslation } from "react-i18next";

export const CreateAnnouncementForm: FC<ICreateAnnouncementFormProps> = (props) => {
  const { onSubmit } = props;

  const { closeDialog } = useDialog();
  const { t } = useTranslation();
  const [activeStep, setActiveStep] = useState(0);
  const [cashedValues, setCashedValues] = useState<TMaybe<ICreateAnnouncementsFields & IRegistrationFormFields>>(null);

  const initialValues = cashedValues || {
    title: "",
    content: "",
    game: null,
    start_at: "",
    registration_start_at: "",
    registration_end_at: "",
    max_participants: 0,
    format: EAnnouncementFormat.SingleElimination,
    has_qualification: false,
    fields: {},
  };

  const validationSchema = createValidationSchema(t);
  const stepList = [t("texts.announcementInfo"), t("texts.applicationForm")];

  const handleCreateAnnouncement = async () => {
    if (cashedValues) {
      const { game, fields, ...rest } = cashedValues;

      if (game) {
        const requestValues = Object.assign(
          {},
          rest,
          !isEmpty(fields)
            ? {
                registration_form: {
                  fields: Object.values(fields).map((field) => ({
                    ...field,
                    options: field.options ? Object.values(field.options) : undefined,
                  })),
                },
              }
            : {},
          {
            game_id: game.id,
          }
        );

        await onSubmit?.(requestValues);
      }
    }
  };

  const handleValuesChange = (values: ICreateAnnouncementsFields & IRegistrationFormFields) => {
    setCashedValues(values);
  };

  const handleBackStep = () => {
    setActiveStep((step) => step - 1);
  };

  const handleNextStep = () => {
    setActiveStep((step) => step + 1);
  };

  const cancelButtonText = (() => {
    if (activeStep === 0) {
      return t("actions.cancel");
    }

    return t("actions.back");
  })();

  const handleCancel = (() => {
    if (activeStep === 0) {
      return closeDialog;
    }

    return handleBackStep;
  })();

  const fields = (() => {
    if (activeStep === 0) {
      return AnnouncementInfoFields;
    }

    return RegistrationFormFields;
  })();

  const confirmButtonText = (() => {
    if (activeStep === 0) {
      return t("actions.next");
    }

    return t("actions.add");
  })();

  const subtitle = (() => {
    if (activeStep === 1) {
      return t("texts.customizeForm");
    }

    return t("texts.fillInBasicTournamentInfo");
  })();

  const handleSubmit = (() => {
    if (activeStep === 0) {
      return handleNextStep;
    }

    return handleCreateAnnouncement;
  })();

  const validation = (() => {
    if (activeStep === 0) {
      return { validationSchema };
    }

    return { validate: (values: IRegistrationFormFields) => validateRegistrationFormFields(values, t) };
  })();

  return (
    <>
      <Box display="flex" flexDirection="column" gap={2} paddingInline={3}>
        <Stepper steps={stepList} activeStep={activeStep} />
        {subtitle && (
          <T variant="caption" color="textSecondary">
            {subtitle}
          </T>
        )}
      </Box>
      <Form
        onSubmit={handleSubmit}
        formikConfig={{ initialValues, ...validation }}
        fields={fields}
        confirmButtonText={confirmButtonText}
        onValuesChange={handleValuesChange}
        cancelButtonText={cancelButtonText}
        onCancel={handleCancel}
        key={activeStep}
        isForDialog
      />
    </>
  );
};
