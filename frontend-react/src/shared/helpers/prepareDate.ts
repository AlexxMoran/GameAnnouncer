import dayjs from "dayjs";

export const prepareDate = (dateToPrepare: string) => {
  const date = dayjs(dateToPrepare);

  return date.format("DD.MM.YYYY HH:mm");
};
