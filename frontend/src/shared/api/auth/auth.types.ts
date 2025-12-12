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
