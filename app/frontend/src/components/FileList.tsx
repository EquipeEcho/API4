import { ReactNode } from "react";
import { SurfaceCard } from "./SurfaceCard";

type FileListProps = {
  header?: ReactNode;
  footer?: ReactNode;
  children: ReactNode;
  className?: string;
};

export function FileList({ header, footer, children, className }: FileListProps) {
  return (
    <SurfaceCard as="section" className={`file-list-card${className ? ` ${className}` : ""}`}>
      {header ? <div className="file-list-card__header">{header}</div> : null}
      <div className="file-list-card__body" role="list">
        {children}
      </div>
      {footer ? <div className="file-list-card__footer">{footer}</div> : null}
    </SurfaceCard>
  );
}
