import { Observable } from 'rxjs';

export type TCreateUploadObservable = (file: File) => Observable<unknown>;
