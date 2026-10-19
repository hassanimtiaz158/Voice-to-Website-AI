import { AlertCircle, CheckCircle2, Info } from "lucide-react";

const ICONS = {
  error: AlertCircle,
  success: CheckCircle2,
  info: Info,
};

const STYLES = {
  error: "border-rose-400/40 bg-rose-500/10 text-rose-200",
  success: "border-emerald-400/40 bg-emerald-500/10 text-emerald-200",
  info: "border-brand-indigo/40 bg-brand-indigo/10 text-indigo-100",
};

export function AuthAlert({ message, variant = "info" }) {
  const Icon = ICONS[variant];
  return (
    <div
      aria-live={variant === "error" ? "assertive" : "polite"}
      className={`animate-fade-rise flex items-start gap-2.5 rounded-xl border px-4 py-3 text-sm leading-relaxed ${STYLES[variant]}`}
      role={variant === "error" ? "alert" : "status"}
    >
      <Icon aria-hidden="true" className="mt-0.5 h-4 w-4 shrink-0" />
      <div>{message}</div>
    </div>
  );
}
