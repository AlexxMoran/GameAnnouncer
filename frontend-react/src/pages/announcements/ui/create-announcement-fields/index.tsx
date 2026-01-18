import type { ICreateAnnouncementsFields } from "@pages/announcements/model/create-validation-schema/types";
import { DatePicker } from "@shared/ui/date-picker";
import { TextField } from "@shared/ui/text-field";
import { useFormikContext } from "formik";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

export const CreateAnnouncementFields: FC = () => {
  const { t } = useTranslation();
  const { errors, values, handleChange, setFieldValue } =
    useFormikContext<ICreateAnnouncementsFields>();

  return (
    <>
      <TextField
        name="title"
        label={t("entities.name")}
        onChange={handleChange}
        value={values["title"]}
        error={!!errors["title"]}
        helperText={errors["title"]}
        required
      />
      <TextField
        name="title"
        label={t("entities.description")}
        onChange={handleChange}
        value={values["content"]}
        error={!!errors["content"]}
        helperText={errors["content"]}
        required
      />
      <DatePicker slotProps={{ textField: { required: true } }} />
      <DatePicker slotProps={{ textField: { required: true } }} />
      <DatePicker slotProps={{ textField: { required: true } }} />

      {/* <Autocomplete
        name="category"
        label={t("entities.category")}
        onChange={handleChangeCategory}
        value={values["category"]}
        error={!!errors["category"]}
        helperText={errors["category"] ? errors["category"] : ""}
        options={CATEGORY_LIST}
        getOptionLabel={(category) => INVERTED_GAME_CATEGORIES[category] || ""}
        required
      /> */}
    </>
  );
};
