import type { ICreateAnnouncementsFields } from "@features/create-announcement/model/create-validation-schema/types";
import { MenuItem } from "@mui/material";
import type { PickerValue } from "@mui/x-date-pickers/internals";
import { useRootService } from "@shared/hooks/use-root-service";
import { EAnnouncementFormat } from "@shared/services/api/announcements-api-service/constants";
import type { IGameDto, IGetGamesDto } from "@shared/services/api/games-api-service/types";
import { PaginationService } from "@shared/services/pagination-service";
import type { TMaybe } from "@shared/types/main.types";
import { Autocomplete } from "@shared/ui/autocomplete";
import { DateTimePicker } from "@shared/ui/date-time-picker";
import { TextField } from "@shared/ui/text-field";
import dayjs from "dayjs";
import { useFormikContext } from "formik";
import { debounce } from "lodash";
import { observer } from "mobx-react-lite";
import { useState, type ChangeEvent, type FC, type SyntheticEvent } from "react";
import { useTranslation } from "react-i18next";

export const AnnouncementInfoFields: FC = observer(() => {
  const { t } = useTranslation();
  const { gamesApiService } = useRootService();
  const [input, setInput] = useState("");

  const { errors, values, handleChange, setFieldValue } = useFormikContext<ICreateAnnouncementsFields>();

  const [paginationService] = useState(
    () =>
      new PaginationService<IGameDto, IGetGamesDto>({
        loadFn: gamesApiService.getGames,
        initImmediately: true,
      })
  );

  const { list, isInitialLoading, isPaginating, paginate, init } = paginationService;

  const handlePickerChange = (name: keyof ICreateAnnouncementsFields, value: PickerValue) => {
    if (dayjs(value).isValid()) {
      setFieldValue(name, value?.toISOString());
    }
  };

  const handleMaxParticipantsChange = (event: ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value ? parseInt(event.target.value, 10).toString() : 0;
    setFieldValue("max_participants", value);
  };

  const handleChangeGame = (_: SyntheticEvent, value: TMaybe<IGameDto>) => {
    setFieldValue("game", value);
  };

  const handleInputChange = debounce((_: SyntheticEvent, value: string) => {
    init({ name: value });
    setInput(value);
  }, 300);

  const handlePaginate = () => paginate({ name: input });

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
      <Autocomplete
        name="category"
        label={t("entities.game")}
        value={values["game"]}
        error={!!errors["game"]}
        helperText={errors["game"]}
        options={list}
        loading={isInitialLoading || isPaginating}
        getOptionLabel={({ name }) => name}
        onChange={handleChangeGame}
        onInputChange={handleInputChange}
        onLastItemVisible={handlePaginate}
        filterOptions={(options) => options}
        required
      />
      <TextField
        name="max_participants"
        label={t("texts.participantsCount")}
        onChange={handleMaxParticipantsChange}
        value={values["max_participants"]}
        error={!!errors["max_participants"]}
        helperText={errors["max_participants"]}
        type="number"
        required
      />
      <TextField
        name="format"
        label={t("texts.announcementFormat")}
        onChange={handleChange}
        value={values["format"]}
        error={!!errors["format"]}
        helperText={errors["format"]}
        select
        required
      >
        {Object.values(EAnnouncementFormat).map((format) => (
          <MenuItem key={format} value={format}>
            {format}
          </MenuItem>
        ))}
      </TextField>
      <DateTimePicker
        slotProps={{
          textField: {
            required: true,
            label: t("texts.registrationStartDate"),
            error: !!errors["registration_start_at"],
            helperText: errors["registration_start_at"],
          },
        }}
        onChange={(value) => handlePickerChange("registration_start_at", value)}
        value={dayjs(values["registration_start_at"])}
        maxDateTime={dayjs(values["start_at"]) || dayjs(values["registration_end_at"])}
        disablePast
      />
      <DateTimePicker
        slotProps={{
          textField: {
            required: true,
            label: t("texts.registrationEndDate"),
            error: !!errors["registration_start_at"],
            helperText: errors["registration_end_at"],
          },
        }}
        onChange={(value) => handlePickerChange("registration_end_at", value)}
        value={dayjs(values["registration_end_at"])}
        minDateTime={dayjs(values["registration_start_at"])}
        maxDateTime={dayjs(values["start_at"])}
        disablePast
      />
      <DateTimePicker
        slotProps={{
          textField: {
            required: true,
            label: t("texts.announcementStartDate"),
            error: !!errors["start_at"],
            helperText: errors["start_at"],
          },
        }}
        onChange={(value) => handlePickerChange("start_at", value)}
        value={dayjs(values["start_at"])}
        minDateTime={dayjs(values["registration_end_at"]) || dayjs(values["registration_start_at"])}
        disablePast
      />
      <TextField
        name="content"
        label={t("entities.description")}
        onChange={handleChange}
        value={values["content"]}
        error={!!errors["content"]}
        helperText={errors["content"]}
        maxRows={3}
        multiline
      />
    </>
  );
});
