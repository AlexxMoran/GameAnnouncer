import { Observable } from 'rxjs';

export interface IConfirmOptions<TObservable> {
  message: string;
  confirmObservable?: Observable<TObservable>;
  confirmButtonText?: string;
  cancelButtonText?: string;
}
