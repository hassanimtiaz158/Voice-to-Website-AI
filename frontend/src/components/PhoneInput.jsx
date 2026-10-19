import { Phone } from "lucide-react";
import { useId } from "react";
import { COUNTRIES } from "../utils/countries";

export function PhoneInput({
  dialCode,
  national,
  error,
  onDialCodeChange,
  onNationalChange,
  onBlur,
  name = "phoneNumber",
}) {
  const generatedId = useId();
  const dialId = `${generatedId}-dial`;
  const errorId = `${generatedId}-error`;

  return (
    <div>
      <label className="auth-label" htmlFor={generatedId}>
        Phone number
      </label>
      <div
        className={`flex overflow-hidden rounded-xl border bg-navy-800/70 transition duration-200 focus-within:border-brand-indigo/70 focus-within:ring-2 focus-within:ring-brand-indigo/40 hover:border-white/20 ${
          error ? "auth-field--invalid" : "border-white/10"
        }`}
      >
        <div className="relative shrink-0">
          <select
            aria-label="Country code"
            className="h-full cursor-pointer appearance-none bg-transparent py-3 pl-3.5 pr-7 text-[15px] text-slate-100 focus:outline-none"
            id={dialId}
            name="phoneDialCode"
            onChange={onDialCodeChange}
            value={dialCode}
          >
            {COUNTRIES.map((country) => (
              <option className="bg-navy-800" key={`${country.iso2}${country.dialCode}`} value={country.dialCode}>
                {country.flag} {country.dialCode}
              </option>
            ))}
          </select>
          <span className="pointer-events-none absolute right-2 top-1/2 -translate-y-1/2 text-xs text-slate-400">
            ▾
          </span>
        </div>
        <div className="relative min-w-0 flex-1 border-l border-white/10">
          <Phone
            aria-hidden="true"
            className="pointer-events-none absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400"
          />
          <input
            aria-describedby={error ? errorId : undefined}
            aria-invalid={error ? true : undefined}
            autoComplete="tel-national"
            className="min-h-[44px] w-full bg-transparent py-3 pl-10 pr-4 text-[15px] text-slate-100 placeholder:text-slate-500 focus:outline-none"
            id={generatedId}
            inputMode="tel"
            name={name}
            onBlur={onBlur}
            onChange={onNationalChange}
            placeholder="555 1234567"
            type="text"
            value={national}
          />
        </div>
      </div>
      {error ? (
        <p className="auth-error" id={errorId} role="alert">
          {error}
        </p>
      ) : null}
    </div>
  );
}
