"use client";

import { useEffect, useRef } from "react";

export function ConfirmDialog({
  open,
  title,
  description,
  confirmLabel,
  danger = false,
  busy = false,
  onConfirm,
  onClose,
}: {
  open: boolean;
  title: string;
  description: string;
  confirmLabel: string;
  danger?: boolean;
  busy?: boolean;
  onConfirm: () => void;
  onClose: () => void;
}) {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (open && !dialog.open) dialog.showModal();
    if (!open && dialog.open) dialog.close();
  }, [open]);

  return (
    <dialog ref={dialogRef} className="confirm-dialog" onCancel={onClose} onClose={onClose}>
      <div className="dialog-body">
        <span className={danger ? "dialog-icon danger" : "dialog-icon"} aria-hidden="true">!</span>
        <h2>{title}</h2>
        <p>{description}</p>
        <div className="dialog-actions">
          <button className="button button-quiet" onClick={onClose} disabled={busy}>إلغاء</button>
          <button className={danger ? "button button-danger" : "button button-primary"} onClick={onConfirm} disabled={busy}>
            {busy ? "جارٍ التنفيذ…" : confirmLabel}
          </button>
        </div>
      </div>
    </dialog>
  );
}
