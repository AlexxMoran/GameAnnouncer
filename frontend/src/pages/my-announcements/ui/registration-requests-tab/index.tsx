import BlockOutlinedIcon from "@mui/icons-material/BlockOutlined";
import { RequestCard } from "@pages/my-announcements/ui/request-card";
import { useDialog } from "@shared/hooks/use-dialog";
import { useRootService } from "@shared/hooks/use-root-service";
import {
  ERegistrationRequestActions,
  ERegistrationRequestStatuses,
} from "@shared/services/api/registration-requests-api-service/constants";
import type { IRegistrationRequestDto } from "@shared/services/api/registration-requests-api-service/types";
import { EntityCrudService } from "@shared/services/entity-crud-service";
import type { IMenuAction } from "@shared/ui/actions-menu/types";
import { Badge } from "@shared/ui/badge";
import { Box } from "@shared/ui/box";
import { Divider } from "@shared/ui/divider";
import { ElementObserver } from "@shared/ui/element-observer";
import { Spinner } from "@shared/ui/spinner";
import { T } from "@shared/ui/typography";
import { observer } from "mobx-react-lite";
import { useSnackbar } from "notistack";
import { Fragment, useState, type FC, type RefObject } from "react";
import { useTranslation } from "react-i18next";

export const RegistrationRequestsTab: FC = observer(() => {
  const { t } = useTranslation();
  const { enqueueSnackbar } = useSnackbar();
  const { confirm } = useDialog();
  const { registrationRequestsApiService } = useRootService();

  const [registrationRequestsService] = useState(
    () =>
      new EntityCrudService({
        getEntitiesFn: registrationRequestsApiService.getMyRequests,
        editEntityFn: registrationRequestsApiService.editRegistrationRequest,
      })
  );

  const { listData, paginate, editEntity } = registrationRequestsService;

  const { list, isInitialLoading, isPaginating, total } = listData;

  const handleCancelRequest = async ({ id }: IRegistrationRequestDto) => {
    const result = await confirm({
      title: t("actions.cancelRequest"),
      children: t("texts.cancelRequestConfirmation"),
      confirmationText: t("actions.cancel"),
    });

    if (result) {
      const { closeDialog, setIsLoading } = result;

      setIsLoading(true);

      const response = await editEntity(id, {
        action: ERegistrationRequestActions.Cancel,
      });

      if (response) {
        enqueueSnackbar(t("texts.cancelRequestSuccess"), {
          variant: "success",
        });
      }

      closeDialog();
    }
  };

  const createRequestActionList = (request: IRegistrationRequestDto): IMenuAction[] => [
    {
      id: 1,
      title: t("actions.cancelRequest"),
      onClick: () => handleCancelRequest(request),
      icon: <BlockOutlinedIcon />,
      disabled:
        request.status === ERegistrationRequestStatuses.Rejected ||
        request.status === ERegistrationRequestStatuses.Cancelled ||
        request.status === ERegistrationRequestStatuses.Expired,
    },
  ];

  return (
    <Box display="flex" flexDirection="column" gap={8} height="100%">
      <Badge badgeContent={total} color="secondary">
        <T variant="h6">{t("texts.myRequests")}</T>
      </Badge>
      {isInitialLoading && <Spinner type="backdrop" />}
      {total === 0 && <T variant="body1">{t("texts.haveNoData")}</T>}
      {!!list.length && (
        <Box display="flex" flexDirection="column" gap={5}>
          {list.map((request, index) =>
            index === list.length - 1 ? (
              <ElementObserver key={request.id} onVisible={paginate}>
                {({ ref }) => (
                  <RequestCard
                    ref={ref as RefObject<HTMLDivElement>}
                    request={request}
                    actionList={createRequestActionList(request)}
                  />
                )}
              </ElementObserver>
            ) : (
              <Fragment key={request.id}>
                <RequestCard request={request} actionList={createRequestActionList(request)} />
                <Divider />
              </Fragment>
            )
          )}
        </Box>
      )}
      {isPaginating && <Spinner type="pagination" />}
    </Box>
  );
});
