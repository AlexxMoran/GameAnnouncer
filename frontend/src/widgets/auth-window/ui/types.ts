import type { IAuthFields } from "@features/auth/model/create-validation-schema/types";
import { EAppRoutes } from "@shared/constants/appRoutes";

export interface IAuthWindowProps {
  titleText: string;
  buttonText: string;
  urlText: string;
  haveAccountText: string;
  url: EAppRoutes;
  onSubmit?: (values: IAuthFields) => Promise<unknown>;
}
