import type { IRegistrationFormFields } from "@features/create-announcement/model/validate-registration-form-fields/types";
import type { IAnnouncementDto } from "@shared/services/api/announcements-api-service/types";
import { v4 as uuidv4 } from "uuid";

export const createInitialFields = (registrationForm: IAnnouncementDto["registration_form"]) => {
  return registrationForm
    ? registrationForm.fields.reduce<IRegistrationFormFields["fields"]>(
        (acc, { id, field_type, label, options, required }) => {
          const preparedOptions = options?.reduce<Record<string, string>>((acc, option) => {
            acc[uuidv4()] = option;

            return acc;
          }, {});

          acc[id] = Object.assign({}, { field_type, label, required }, options && { options: preparedOptions });

          return acc;
        },
        {}
      )
    : {};
};
