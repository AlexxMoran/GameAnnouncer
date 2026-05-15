import type { IEntityIdField } from "@shared/types/commonEntity.types";
import type { TMaybe } from "@shared/types/main.types";

export interface ILoginDto {
  username: string;
  password: string;
}

export interface IRegisterDto {
  email: string;
  password: string;
  nickname?: string;
}

export interface IAccessToken {
  access_token: string;
  token_type: string;
}

export interface IEditUserDto {
  first_name?: string;
  last_name?: string;
  nickname?: string;
  avatar_color?: TMaybe<string>;
  avatar_icon_id?: TMaybe<number>;
}

export interface IUserDto extends IEntityIdField {
  first_name: string;
  last_name: string;
  nickname: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  is_verified: boolean;
  avatar_color: TMaybe<string>;
  avatar_icon_id: TMaybe<number>;
}
