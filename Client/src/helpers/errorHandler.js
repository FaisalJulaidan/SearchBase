import * as Sentry from '@sentry/browser';

export function errorHandler(error) {
    Sentry.withScope(scope => {
        Object.keys(error).forEach(key => scope.setExtra(key, error[key]));
        Sentry.captureException(error);
    });
}

