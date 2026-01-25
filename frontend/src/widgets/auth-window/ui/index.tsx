import { AuthForm } from "@features/auth/ui/auth-form";
import { Box } from "@shared/ui/box";
import { Link } from "@shared/ui/link";
import { T } from "@shared/ui/typography";
import { AuthFormWrapperStyled } from "@widgets/auth-window/ui/styles";
import type { IAuthWindowProps } from "@widgets/auth-window/ui/types";
import type { FC } from "react";

export const AuthWindow: FC<IAuthWindowProps> = (props) => {
  const { titleText, buttonText, urlText, haveAccountText, url, onSubmit } =
    props;

  return (
    <Box
      display="flex"
      flexDirection="column"
      justifyContent="center"
      alignItems="center"
      width="100%"
      height="100%"
    >
      <AuthFormWrapperStyled>
        <T variant="h5" capitalizeFirst>
          {titleText}
        </T>
        <AuthForm buttonText={buttonText} onSubmit={onSubmit} />
        <T variant="body2">
          {haveAccountText} <Link to={url}>{urlText}</Link>
        </T>
      </AuthFormWrapperStyled>
    </Box>
  );
};
