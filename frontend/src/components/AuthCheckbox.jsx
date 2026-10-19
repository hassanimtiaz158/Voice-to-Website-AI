import { useId } from "react";

export function AuthCheckbox({ label, error, ...rest }) {
  const id = useId();
  const errorId = `${id}-error`;

  return (
    <div>
      <label
        className="flex min-h-[44px] cursor-pointer items-center gap-3 text-sm text-slate-300"
        htmlFor={id}
      >
        <input
          {...rest}
          aria-describedby={error ? errorId : undefined}
          aria-invalid={error ? true : undefined}
          className="h-5 w-5 shrink-0 cursor-pointer rounded-md border border-white/25 bg-navy-800 accent-brand-violet transition focus-visible:ring-2 focus-visible:ring-brand-indigo/60"
          id={id}
          type="checkbox"
        />
        <span>{label}</span>
      </label>
      {error ? (
        <p className="auth-error" id={errorId} role="alert">
          {error}
        </p>
      ) : null}
    </div>
  );
}
