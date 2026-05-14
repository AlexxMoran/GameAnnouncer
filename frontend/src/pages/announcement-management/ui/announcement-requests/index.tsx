import PendingActionsIcon from "@mui/icons-material/PendingActions";
import type { IOutletContextData } from "@pages/announcement-management/model/types";
import { useAnnouncementRequestsService } from "@pages/announcement-management/model/use-announcement-request-service";
import { AnnouncementRequestCard } from "@pages/announcement-management/ui/announcement-request-card";
import { AnnouncementRequestFilters } from "@pages/announcement-management/ui/announcement-request-filters";
import { RequestCardsWrapperStyled } from "@pages/announcement-management/ui/request-cards-wrapper-styled";
import { GAPS } from "@shared/constants/gaps";
import type { IAnnouncementDto } from "@shared/services/api/announcements-api-service/types";
import type { IUserDto } from "@shared/services/api/auth-api-service/types";
import { EGameCategories } from "@shared/services/api/games-api-service/constants";
import type { IGameDto } from "@shared/services/api/games-api-service/types";
import { ERegistrationRequestStatuses } from "@shared/services/api/registration-requests-api-service/constants";
import type { IRegistrationRequestDto } from "@shared/services/api/registration-requests-api-service/types";
import { Box } from "@shared/ui/box";
import { Card } from "@shared/ui/card";
import { InfiniteScrollList } from "@shared/ui/infinite-scroll-list";
import { PageTitle } from "@shared/ui/page-title";
import { observer } from "mobx-react-lite";
import { useCallback, type FC } from "react";
import { useTranslation } from "react-i18next";
import { useOutletContext } from "react-router";
// ---- МОКИ ДАННЫХ ----

// Игры (Pick для game в объявлении)
const mockGames: Pick<IGameDto, "category" | "id" | "image_url" | "name">[] = [
  { id: 1, name: "Cyberpunk 2077", category: EGameCategories["Battle Royale"], image_url: "cyberpunk.jpg" },
  { id: 2, name: "FIFA 24", category: EGameCategories.Card, image_url: "fifa.jpg" },
  { id: 3, name: "StarCraft II", category: EGameCategories.Fighting, image_url: "starcraft.jpg" },
  { id: 4, name: "Portal 2", category: EGameCategories.Racing, image_url: "portal.jpg" },
  { id: 5, name: "DOOM Eternal", category: EGameCategories.Sports, image_url: "doom.jpg" },
];

// Объявления (только нужные поля: id, title, game)
const mockAnnouncements: Pick<IAnnouncementDto, "id" | "title" | "game">[] = [
  { id: 101, title: "Киберпанк турнир", game: mockGames[0] },
  { id: 102, title: "Чемпионат по FIFA", game: mockGames[1] },
  { id: 103, title: "Битва стратегов", game: mockGames[2] },
  { id: 104, title: "Головоломка для двоих", game: mockGames[3] },
  { id: 105, title: "Deathmatch в DOOM", game: mockGames[4] },
  { id: 106, title: "Вечер RPG", game: mockGames[0] },
  { id: 107, title: "Кубок FIFA", game: mockGames[1] },
  { id: 108, title: "Стратегия 1v1", game: mockGames[2] },
  { id: 109, title: "Portal Speedrun", game: mockGames[3] },
  { id: 110, title: "DOOM Co-op", game: mockGames[4] },
];

// Пользователи (Pick: id, nickname, avatar_color, avatar_icon_id)
const mockUsers: Pick<IUserDto, "id" | "nickname" | "avatar_color" | "avatar_icon_id">[] = [
  { id: 1001, nickname: "GamerPro", avatar_color: "#ff5733", avatar_icon_id: 1 },
  { id: 1002, nickname: "LuckyShot", avatar_color: "#33ff57", avatar_icon_id: null },
  { id: 1003, nickname: "StealthMaster", avatar_color: null, avatar_icon_id: 3 },
  { id: 1004, nickname: "NoobSlayer", avatar_color: "#3357ff", avatar_icon_id: 10 },
  { id: 1005, nickname: "QueenOfGames", avatar_color: "#ff33f5", avatar_icon_id: 15 },
  { id: 1006, nickname: "DarkKnight", avatar_color: "#333333", avatar_icon_id: 4 },
  { id: 1007, nickname: "FastFinger", avatar_color: null, avatar_icon_id: 6 },
  { id: 1008, nickname: "Tactician", avatar_color: "#ffd700", avatar_icon_id: 9 },
  { id: 1009, nickname: "RageQuit", avatar_color: "#8b0000", avatar_icon_id: null },
  { id: 1010, nickname: "PixelHero", avatar_color: "#00ced1", avatar_icon_id: 30 },
  { id: 1011, nickname: "BlazeWarrior", avatar_color: "#e34c26", avatar_icon_id: 7 },
  { id: 1012, nickname: "ShadowMage", avatar_color: "#2c3e50", avatar_icon_id: 12 },
  { id: 1013, nickname: "IronSniper", avatar_color: "#7f8c8d", avatar_icon_id: null },
  { id: 1014, nickname: "CrimsonFury", avatar_color: "#c0392b", avatar_icon_id: 22 },
  { id: 1015, nickname: "NeonPhantom", avatar_color: "#00ffcc", avatar_icon_id: 5 },
  { id: 1016, nickname: "FrostGiant", avatar_color: "#3498db", avatar_icon_id: 18 },
  { id: 1017, nickname: "MysticArrow", avatar_color: null, avatar_icon_id: 14 },
  { id: 1018, nickname: "RogueAssassin", avatar_color: "#1abc9c", avatar_icon_id: 27 },
  { id: 1019, nickname: "ThunderGod", avatar_color: "#f1c40f", avatar_icon_id: 8 },
  { id: 1020, nickname: "SilentViper", avatar_color: null, avatar_icon_id: 11 },
];

// ---- ГЕНЕРАЦИЯ МАССИВА ЗАПРОСОВ (10 элементов) ----
const registrationRequestMocks: IRegistrationRequestDto[] = [
  {
    id: 1,
    created_at: "2025-01-10T10:00:00Z",
    updated_at: "2025-01-10T10:00:00Z",
    announcement_id: 101,
    announcement: mockAnnouncements.find((a) => a.id === 101)!,
    user: mockUsers[0],
    status: ERegistrationRequestStatuses.Approved,
    cancellation_reason: null,
  },
  {
    id: 2,
    created_at: "2025-01-11T12:30:00Z",
    updated_at: "2025-01-12T09:15:00Z",
    announcement_id: 102,
    announcement: mockAnnouncements.find((a) => a.id === 102)!,
    user: mockUsers[1],
    status: ERegistrationRequestStatuses.Cancelled,
    cancellation_reason: null,
  },
  {
    id: 3,
    created_at: "2025-01-12T08:20:00Z",
    updated_at: "2025-01-13T14:45:00Z",
    announcement_id: 103,
    announcement: mockAnnouncements.find((a) => a.id === 103)!,
    user: mockUsers[2],
    status: ERegistrationRequestStatuses.Expired,
    cancellation_reason: "Не соответствует требованиям рейтинга",
  },
  {
    id: 4,
    created_at: "2025-01-13T16:00:00Z",
    updated_at: "2025-01-14T11:30:00Z",
    announcement_id: 104,
    announcement: mockAnnouncements.find((a) => a.id === 104)!,
    user: mockUsers[3],
    status: ERegistrationRequestStatuses.Pending,
    cancellation_reason: "Пользователь передумал",
  },
  {
    id: 5,
    created_at: "2025-01-14T09:45:00Z",
    updated_at: "2025-01-15T10:20:00Z",
    announcement_id: 105,
    announcement: mockAnnouncements.find((a) => a.id === 105)!,
    user: mockUsers[4],
    status: ERegistrationRequestStatuses.Rejected,
    cancellation_reason: null,
  },
  {
    id: 6,
    created_at: "2025-01-15T14:10:00Z",
    updated_at: "2025-01-16T08:00:00Z",
    announcement_id: 106,
    announcement: mockAnnouncements.find((a) => a.id === 106)!,
    user: mockUsers[5],
    status: ERegistrationRequestStatuses.Rejected,
    cancellation_reason: null,
  },
  {
    id: 7,
    created_at: "2025-01-16T11:55:00Z",
    updated_at: "2025-01-17T13:40:00Z",
    announcement_id: 107,
    announcement: mockAnnouncements.find((a) => a.id === 107)!,
    user: mockUsers[6],
    status: ERegistrationRequestStatuses.Approved,
    cancellation_reason: null,
  },
  {
    id: 8,
    created_at: "2025-01-17T07:30:00Z",
    updated_at: "2025-01-18T16:25:00Z",
    announcement_id: 108,
    announcement: mockAnnouncements.find((a) => a.id === 108)!,
    user: mockUsers[7],
    status: ERegistrationRequestStatuses.Cancelled,
    cancellation_reason: "Превышено количество участников",
  },
  {
    id: 9,
    created_at: "2025-01-18T19:20:00Z",
    updated_at: "2025-01-19T12:10:00Z",
    announcement_id: 109,
    announcement: mockAnnouncements.find((a) => a.id === 109)!,
    user: mockUsers[8],
    status: ERegistrationRequestStatuses.Cancelled,
    cancellation_reason: "Организатор отменил турнир",
  },
  {
    id: 10,
    created_at: "2025-01-19T22:05:00Z",
    updated_at: "2025-01-20T09:50:00Z",
    announcement_id: 110,
    announcement: mockAnnouncements.find((a) => a.id === 110)!,
    user: mockUsers[9],
    status: ERegistrationRequestStatuses.Approved,
    cancellation_reason: null,
  },
];

export const AnnouncementRequests: FC = observer(() => {
  const { announcement } = useOutletContext<IOutletContextData>();
  const { listData, filters, paginate, setFilter } = useAnnouncementRequestsService(announcement);
  const { t } = useTranslation();

  const renderItem = useCallback(
    (request: IRegistrationRequestDto) => <AnnouncementRequestCard key={request.id} request={request} />,
    []
  );

  return (
    <Card sx={{ padding: GAPS, flex: 1, display: "flex", flexDirection: "column", gap: GAPS }}>
      <PageTitle title={t("entities.bid.many")} count={listData.filteredCount} type="tab" />
      <Box display="flex" flexDirection="column" gap={2} flex={1}>
        <AnnouncementRequestFilters filters={filters} handleFilter={setFilter} />
        <InfiniteScrollList
          renderItem={renderItem}
          onLoadMore={paginate}
          noDataIcon={PendingActionsIcon}
          noDataTitle={t("texts.noApplicationsYet")}
          noDataSubtitle={t("texts.allJoinRequestsWillBeShownHere")}
          containerComponent={RequestCardsWrapperStyled}
          {...listData}
          list={registrationRequestMocks}
          hasMore={false}
          totalCount={20}
        />
      </Box>
    </Card>
  );
});
