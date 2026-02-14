import { createValidationSchema } from "@features/create-announcement/model/create-validation-schema";
import type { ICreateAnnouncementsFields } from "@features/create-announcement/model/create-validation-schema/types";
import { validateRegistrationFormFields } from "@features/create-announcement/model/validate-registration-form-fields";
import type { IRegistrationFormFields } from "@features/create-announcement/model/validate-registration-form-fields/types";
import { AnnouncementInfoFields } from "@features/create-announcement/ui/announcement-info-fields";
import type { ICreateAnnouncementFormProps } from "@features/create-announcement/ui/create-announcement-form/types";
import { RegistrationFormFields } from "@features/create-announcement/ui/registration-form-fields";
import HelpIcon from "@mui/icons-material/Help";
import { useDialog } from "@shared/hooks/use-dialog";
import { EAnnouncementFormat } from "@shared/services/api/announcements-api-service/constants";
import { Box } from "@shared/ui/box";
import { Form } from "@shared/ui/form";
import { Stepper } from "@shared/ui/stepper";
import { Tooltip } from "@shared/ui/tooltip";
import { T } from "@shared/ui/typography";
import isEmpty from "lodash/isEmpty";
import { useState, type FC } from "react";
import { useTranslation } from "react-i18next";

let cashedValues: (ICreateAnnouncementsFields & IRegistrationFormFields) | undefined;

export const CreateAnnouncementForm: FC<ICreateAnnouncementFormProps> = (props) => {
  const { onSubmit } = props;

  const { closeDialog } = useDialog();
  const { t } = useTranslation();
  const [activeStep, setActiveStep] = useState(0);

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
  const stepList = [t("texts.announcementInfo"), t("texts.registrationForm")];

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

        const result = await onSubmit?.(requestValues);

        if (result) {
          cashedValues = undefined;
        }
      }
    }
  };

  const handleValuesChange = (values: ICreateAnnouncementsFields & IRegistrationFormFields) => {
    cashedValues = values;
  };

  const handleBackStep = () => {
    setActiveStep((step) => step - 1);
  };

  const handleNextStep = () => {
    setActiveStep((step) => step + 1);
  };

  const cancelButtonProps = (() => {
    if (activeStep === 0) {
      return { text: t("actions.cancel"), onCancel: closeDialog };
    }

    return { text: t("actions.back"), onCancel: handleBackStep };
  })();

  const fields = (() => {
    if (activeStep === 0) {
      return AnnouncementInfoFields;
    }

    return RegistrationFormFields;
  })();

  const submitButtonText = (() => {
    if (activeStep === 0) {
      return t("actions.next");
    }

    return t("actions.add");
  })();

  const subtitleTooltip = (() => {
    if (activeStep === 1) {
      return t("texts.createRegistrationFormTooltip");
    }
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
    <Box display="flex" flexDirection="column" gap={10}>
      <Stepper steps={stepList} activeStep={activeStep} />
      <Box display="flex" flexDirection="column" gap={6}>
        <Box display="flex" alignItems="flex-start">
          <T variant="h6">{stepList[activeStep]}</T>
          {subtitleTooltip && (
            <Tooltip title={subtitleTooltip}>
              <HelpIcon fontSize="small" sx={{ cursor: "pointer" }} />
            </Tooltip>
          )}
        </Box>
        <Form
          onSubmit={handleSubmit}
          formikConfig={{ initialValues, ...validation }}
          fields={fields}
          buttonText={submitButtonText}
          wrapperStyles={{ minWidth: "500px" }}
          onValuesChange={handleValuesChange}
          cancelButton={cancelButtonProps}
          key={activeStep}
        />
      </Box>
    </Box>
  );
};
