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

export interface IUserDto {
  first_name: string;
  last_name: string;
  nickname: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  is_verified: boolean;
}
