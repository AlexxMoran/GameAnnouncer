import AddAPhotoOutlinedIcon from "@mui/icons-material/AddAPhotoOutlined";
import DeleteOutlinedIcon from "@mui/icons-material/DeleteOutlined";
import EditOutlinedIcon from "@mui/icons-material/EditOutlined";
import type { ICreateGameActionListParams } from "@pages/games/model/create-game-action-list/types";
import type { IMenuAction } from "@shared/ui/actions-menu/types";

export const createGameActionList = ({
  t,
  game,
  handleDeleteGame,
  handleOpenEditDialog,
  handleOpenUploadImageDialog,
}: ICreateGameActionListParams): IMenuAction[] => [
  {
    id: 1,
    title: t("actions.uploadImage"),
    onClick: () => handleOpenUploadImageDialog(game),
    icon: <AddAPhotoOutlinedIcon />,
  },
  {
    id: 2,
    title: t("actions.edit"),
    onClick: () => handleOpenEditDialog(game),
    icon: <EditOutlinedIcon />,
  },
  {
    id: 3,
    title: t("actions.delete"),
    onClick: () => handleDeleteGame(game),
    icon: <DeleteOutlinedIcon />,
  },
];
