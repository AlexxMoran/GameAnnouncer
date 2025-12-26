import { Component, inject, OnInit, signal } from '@angular/core';
import { MatProgressSpinner } from '@angular/material/progress-spinner';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthApiService } from '@shared/api/auth/auth-api.service';
import { SnackBarService } from '@shared/lib/snack-bar/snack-bar.service';
import { TMaybe } from '@shared/lib/utility-types/additional.types';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-email-verification-page',
  imports: [MatProgressSpinner],
  template: `@if (verifyingInProcess()) {
    <mat-spinner></mat-spinner>
  } `,
  host: { class: 'w-full h-full' },
})
export class EmailVerificationPage implements OnInit {
  private route = inject(ActivatedRoute);
  private authApiService = inject(AuthApiService);
  private snackbarService = inject(SnackBarService);
  private router = inject(Router);

  readonly verifyingInProcess = signal(false);

  ngOnInit() {
    const token = this.route.snapshot.queryParamMap.get('token');

    this.verify(token);
  }

  verify = (token: TMaybe<string>) => {
    if (token) {
      this.verifyingInProcess.set(true);

      this.authApiService
        .verifyEmail(token)
        .pipe(finalize(() => this.verifyingInProcess.set(false)))
        .subscribe(() => {
          this.snackbarService.showSuccessSnackBar('texts.emailVerificationSuccess');
          this.router.navigateByUrl('/login');
        });
    } else {
      this.snackbarService.showErrorSnackBar('texts.emptyVerifyTokenAlert');
    }
  };
}
