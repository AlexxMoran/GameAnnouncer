import { AuthForm } from "@features/auth/ui/auth-form";
import { PageContentWrapperStyled } from "@shared/ui/_styled/page-content-wrapper-styled";
import { Box } from "@shared/ui/box";
import { Card } from "@shared/ui/card";
import { Link } from "@shared/ui/link";
import { T } from "@shared/ui/typography";
import type { IAuthWindowProps } from "@widgets/auth-window/ui/types";
import type { FC } from "react";

export const AuthWindow: FC<IAuthWindowProps> = (props) => {
  const { titleText, buttonText, urlText, haveAccountText, url, onSubmit } = props;

  return (
    <PageContentWrapperStyled>
      <Box display="flex" flexDirection="column" justifyContent="center" alignItems="center" width="100%" height="100%">
        <Card
          sx={{
            alignItems: "center",
            width: { xs: "100%", md: "500px" },
            px: { xs: 2, md: 6 },
            py: { xs: 2, md: 4 },
            gap: { xs: 2, md: 4 },
          }}
        >
          <T variant="h5" sx={{ "&::first-letter": { textTransform: "capitalize" } }}>
            {titleText}
          </T>
          <AuthForm buttonText={buttonText} onSubmit={onSubmit} />
          <T variant="body2">
            {haveAccountText} <Link to={url}>{urlText}</Link>
          </T>
        </Card>
      </Box>
    </PageContentWrapperStyled>
  );
};
