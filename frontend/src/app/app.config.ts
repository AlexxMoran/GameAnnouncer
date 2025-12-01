import { provideHttpClient, withFetch, withInterceptors } from '@angular/common/http';
import {
  ApplicationConfig,
  provideBrowserGlobalErrorListeners,
  provideZonelessChangeDetection,
} from '@angular/core';
import { provideRouter } from '@angular/router';
import { errorInterceptor } from '@app/interceptors/error.interceptor';
import { provideTranslateService } from '@ngx-translate/core';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZonelessChangeDetection(),
    provideRouter(routes),
    provideTranslateService({ fallbackLang: 'ru', lang: 'ru' }),
    provideHttpClient(withFetch(), withInterceptors([errorInterceptor])),
  ],
};
