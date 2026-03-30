import { ReactNode, useEffect, useId } from "react";
import { Button } from "./Button";
import { CloseIcon } from "./Icons";
import { SurfaceCard } from "./SurfaceCard";

type ConfirmationModalProps = {
  open: boolean;
  title: string;
  description: ReactNode;
  confirmLabel: string;
  cancelLabel?: string;
  confirmTone?: "primary" | "success";
  onClose: () => void;
  onConfirm: () => void;
};

export function ConfirmationModal({
  open,
  title,
  description,
  confirmLabel,
  cancelLabel = "Cancelar",
  confirmTone = "primary",
  onClose,
  onConfirm,
}: ConfirmationModalProps) {
  const titleId = useId();
  const descriptionId = useId();

  useEffect(() => {
    if (!open) {
      return;
    }

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        onClose();
      }
    };

    document.body.style.overflow = "hidden";
    window.addEventListener("keydown", handleEscape);

    return () => {
      document.body.style.overflow = "";
      window.removeEventListener("keydown", handleEscape);
    };
  }, [open, onClose]);

  if (!open) {
    return null;
  }

  return (
    <div className="modal-backdrop" onClick={onClose} role="presentation">
      <SurfaceCard
        as="div"
        className="modal-card"
        onClick={(event) => event.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        aria-describedby={descriptionId}
      >
        <div className="modal-card__header">
          <h2 className="modal-card__title" id={titleId}>
            {title}
          </h2>

          <button
            className="modal-card__close"
            type="button"
            onClick={onClose}
            aria-label="Fechar modal"
          >
            <CloseIcon />
          </button>
        </div>

        <div className="modal-card__description" id={descriptionId}>
          {description}
        </div>

        <div className="modal-card__actions">
          <Button variant="ghost" onClick={onClose}>
            {cancelLabel}
          </Button>
          <Button variant={confirmTone} onClick={onConfirm}>
            {confirmLabel}
          </Button>
        </div>
      </SurfaceCard>
    </div>
  );
}
