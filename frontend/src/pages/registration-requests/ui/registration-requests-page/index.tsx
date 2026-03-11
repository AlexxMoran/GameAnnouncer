import AssignmentIcon from "@mui/icons-material/Assignment";
import { RegistrationRequestsService } from "@pages/registration-requests/model/registration-requests-service";
import { useCancelRegistrationRequest } from "@pages/registration-requests/model/use-cancel-registration-request";
import { RequestCard } from "@pages/registration-requests/ui/request-card";
import { RequestCardsContainer } from "@pages/registration-requests/ui/request-cards-container";
import { useRootService } from "@shared/hooks/use-root-service";
import type { IRegistrationRequestDto } from "@shared/services/api/registration-requests-api-service/types";
import { PageContentWrapperStyled } from "@shared/ui/_styled/page-content-wrapper-styled";
import { InfiniteScrollList } from "@shared/ui/infinite-scroll-list";
import { PageTitle } from "@shared/ui/page-title";
import { observer } from "mobx-react-lite";
import { useCallback, useState, type FC } from "react";
import { useTranslation } from "react-i18next";

export const RegistrationRequestsPage: FC = observer(() => {
  const { t } = useTranslation();
  const { registrationRequestsApiService } = useRootService();
  const [registrationRequestsService] = useState(() => new RegistrationRequestsService(registrationRequestsApiService));

  const { editEntity, paginate, listData } = registrationRequestsService;

  const { handleCancelRequest } = useCancelRegistrationRequest(editEntity);

  const renderItem = useCallback(
    (request: IRegistrationRequestDto) => (
      <RequestCard request={request} onCancelRequest={() => handleCancelRequest(request)} />
    ),
    [t, handleCancelRequest]
  );

  return (
    <PageContentWrapperStyled>
      <PageTitle title={t("texts.myRequests")} count={listData.filteredCount} />
      <InfiniteScrollList
        renderItem={renderItem}
        onLoadMore={paginate}
        noDataTitle={t("texts.noApplications")}
        noDataSubtitle={t("texts.howToSubmitApplication")}
        noDataIcon={AssignmentIcon}
        containerComponent={RequestCardsContainer}
        {...listData}
      />
    </PageContentWrapperStyled>
  );
});
