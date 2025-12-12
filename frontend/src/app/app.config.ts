import { provideHttpClient, withFetch, withInterceptors } from '@angular/common/http';
import {
  ApplicationConfig,
  provideBrowserGlobalErrorListeners,
  provideZonelessChangeDetection,
} from '@angular/core';
import { provideRouter } from '@angular/router';
import { authInterceptor } from '@app/interceptors/auth.interceptor';
import { errorInterceptor } from '@app/interceptors/error.interceptor';
import { provideTranslateCompiler, provideTranslateService } from '@ngx-translate/core';
import {
  MESSAGE_FORMAT_CONFIG,
  TranslateMessageFormatCompiler,
} from 'ngx-translate-messageformat-compiler';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZonelessChangeDetection(),
    provideRouter(routes),
    provideTranslateService({
      fallbackLang: 'ru',
      lang: 'ru',
      compiler: provideTranslateCompiler(TranslateMessageFormatCompiler),
    }),
    {
      provide: MESSAGE_FORMAT_CONFIG,
      useValue: {
        throwOnError: true,
        formatters: { upcase: (v: string) => v.toUpperCase() },
      },
    },
    provideHttpClient(withFetch(), withInterceptors([authInterceptor, errorInterceptor])),
  ],
};
