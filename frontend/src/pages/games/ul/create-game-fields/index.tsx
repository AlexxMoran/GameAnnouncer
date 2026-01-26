import type { ICreateGameFields } from "@pages/games/model/create-validation-schema/types";
import { CATEGORY_LIST, INVERTED_GAME_CATEGORIES } from "@pages/games/ul/create-game-fields/constants";
import { EGameCategories } from "@shared/services/api/games-api-service/constants";
import type { TMaybe } from "@shared/types/main.types";
import { Autocomplete } from "@shared/ui/autocomplete";
import { TextField } from "@shared/ui/text-field";
import { useFormikContext } from "formik";
import type { FC, SyntheticEvent } from "react";
import { useTranslation } from "react-i18next";

export const CreateGameFields: FC = () => {
  const { t } = useTranslation();
  const { errors, values, handleChange, setFieldValue } = useFormikContext<ICreateGameFields>();

  const handleChangeCategory = (_: SyntheticEvent, value: TMaybe<EGameCategories>) => {
    setFieldValue("category", value);
  };

  return (
    <>
      <TextField
        name="name"
        label={t("entities.name")}
        onChange={handleChange}
        value={values["name"]}
        error={!!errors["name"]}
        helperText={errors["name"]}
        required
      />
      <TextField
        name="description"
        label={t("entities.description")}
        onChange={handleChange}
        value={values["description"]}
        error={!!errors["description"]}
        helperText={errors["description"]}
        maxRows={4}
        required
        multiline
      />
      <Autocomplete
        name="category"
        label={t("entities.category")}
        onChange={handleChangeCategory}
        value={values["category"]}
        error={!!errors["category"]}
        helperText={errors["category"]}
        options={CATEGORY_LIST}
        getOptionLabel={(category) => INVERTED_GAME_CATEGORIES[category] || ""}
        required
      />
    </>
  );
};
