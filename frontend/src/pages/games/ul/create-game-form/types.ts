import type { ICreateGameFields } from "@pages/games/model/create-validation-schema/types";
import type { IGameDto } from "@shared/services/api/games-api-service/types";

export interface ICreateGameFormProps {
  initialValues?: IGameDto;
  onSubmit?: (values: ICreateGameFields) => Promise<unknown>;
}
