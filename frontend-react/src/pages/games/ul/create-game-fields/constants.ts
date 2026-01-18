import { EGameCategories } from "@shared/services/api/games-api-service/constants";
import invert from "lodash/invert";

export const CATEGORY_LIST = Object.values(EGameCategories);
export const INVERTED_GAME_CATEGORIES = invert(EGameCategories);
