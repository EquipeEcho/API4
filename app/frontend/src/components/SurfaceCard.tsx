import { ComponentPropsWithoutRef, ElementType, ReactNode } from "react";

type SurfaceCardProps<T extends ElementType> = {
  as?: T;
  className?: string;
  children: ReactNode;
} & Omit<ComponentPropsWithoutRef<T>, "as" | "className" | "children">;

export function SurfaceCard<T extends ElementType = "div">({
  as,
  className,
  children,
  ...props
}: SurfaceCardProps<T>) {
  const Component = as ?? "div";

  return (
    <Component
      className={`surface-card${className ? ` ${className}` : ""}`}
      {...props}
    >
      {children}
    </Component>
  );
}
