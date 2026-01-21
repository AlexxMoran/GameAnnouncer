import { DialogContext } from "@shared/providers/dialog-provider/constants";
import { useContext } from "react";

export const useDialog = () => useContext(DialogContext);
