import { getPasswordStrength } from "../utils/validation";

const SEGMENTS = 4;

export function PasswordStrength({ password }) {
  const strength = getPasswordStrength(password);

  return (
    <div className="mt-2.5">
      <div aria-hidden="true" className="flex gap-1.5">
        {Array.from({ length: SEGMENTS }, (_, index) => (
          <span
            className={`h-1.5 flex-1 rounded-full transition-colors duration-300 ${
              password && index < strength.score ? strength.bars : "bg-white/10"
            }`}
            key={index}
          />
        ))}
      </div>
      <p
        aria-live="polite"
        className={`mt-1.5 text-xs font-medium ${password ? strength.text : "text-slate-400"}`}
      >
        {password
          ? `Password strength: ${strength.label}`
          : "Use at least 10 characters. Length matters more than symbols."}
      </p>
    </div>
  );
}
