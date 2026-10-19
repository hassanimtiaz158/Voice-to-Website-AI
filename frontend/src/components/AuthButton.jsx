import { Loader2 } from "lucide-react";

export function AuthButton({ loading = false, children, disabled, ...rest }) {
  return (
    <button
      {...rest}
      aria-busy={loading || undefined}
      className="btn-primary"
      disabled={disabled || loading}
      type={rest.type ?? "submit"}
    >
      {loading ? <Loader2 aria-hidden="true" className="h-5 w-5 animate-spin" /> : null}
      {children}
    </button>
  );
}
