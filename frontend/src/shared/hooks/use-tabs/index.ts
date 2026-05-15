import type { SyntheticEvent } from "react";
import { useLocation, useNavigate } from "react-router";

export const useTabs = <TTabs extends Record<string, string>>() => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleChangeTab = (_: SyntheticEvent, value: TTabs[keyof TTabs]) => {
    navigate(value, { replace: true, preventScrollReset: true });
  };

  const tabValue = location.pathname.split("/").at(-1);

  return { handleChangeTab, tabValue };
};
