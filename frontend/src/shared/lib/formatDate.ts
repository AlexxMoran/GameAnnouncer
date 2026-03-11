import dayjs from "dayjs";

export const formatDate = (dateToPrepare?: string) => {
  const date = dayjs(dateToPrepare);

  return date.format("DD.MM.YYYY HH:mm");
};
