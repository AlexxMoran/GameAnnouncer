import dayjs from "dayjs";

export function formatDateRange(dateStr1: string, dateStr2: string) {
  const d1 = dayjs.utc(dateStr1);
  const d2 = dayjs.utc(dateStr2);

  if (d1.isSame(d2)) {
    return d1.format("D MMM YYYY");
  }

  const year1 = d1.year();
  const year2 = d2.year();

  const shortFormat = "D MMM";

  if (year1 === year2) {
    return `${d1.format(shortFormat)} - ${d2.format(shortFormat)} ${year1}`;
  } else {
    return `${d1.format(shortFormat)} ${year1} - ${d2.format(shortFormat)} ${year2}`;
  }
}
