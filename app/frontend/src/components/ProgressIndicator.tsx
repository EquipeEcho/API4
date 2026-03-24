import { SpinnerIcon } from "./Icons";

type ProgressIndicatorProps = {
  progress: number;
};

export function ProgressIndicator({ progress }: ProgressIndicatorProps) {
  return (
    <div className="progress-indicator">
      <div className="progress-indicator__spinner" aria-hidden="true">
        <SpinnerIcon />
      </div>

      <div
        className="progress-indicator__bar"
        aria-label={`Progresso do processamento: ${progress}%`}
        role="progressbar"
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={progress}
      >
        <span
          className="progress-indicator__bar-fill"
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  );
}
