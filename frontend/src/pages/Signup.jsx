import { CheckCircle2, Lock, Mail, User } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { AuthAlert } from "../components/AuthAlert";
import { AuthButton } from "../components/AuthButton";
import { AuthCheckbox } from "../components/AuthCheckbox";
import { AuthInput } from "../components/AuthInput";
import { AuthLayout } from "../components/AuthLayout";
import { PasswordStrength } from "../components/PasswordStrength";
import { PhoneInput } from "../components/PhoneInput";
import { useAuthForm } from "../hooks/useAuthForm";
import { signUp, toAuthErrorMessage } from "../services/authService";
import {
  toE164,
  validateCheckbox,
  validateConfirmPassword,
  validateEmail,
  validatePassword,
  validatePhone,
  validateRequiredName,
} from "../utils/validation";

export function Signup() {
  const navigate = useNavigate();

  const {
    values,
    errors,
    alert,
    setValue,
    handleBlur,
    handleSubmit,
    formRef,
    isSubmitting,
    serverError,
  } = useAuthForm({
    initialValues: {
      fullName: "",
      email: "",
      phoneDialCode: "+92",
      phoneNumber: "",
      password: "",
      confirmPassword: "",
      terms: false,
    },
    validators: {
      fullName: (value) => validateRequiredName(String(value)),
      email: (value) => validateEmail(String(value)),
      phoneNumber: (value) => validatePhone(String(value)),
      password: (value) => validatePassword(String(value)),
      confirmPassword: (value, all) =>
        validateConfirmPassword(String(all.password), String(value)),
      terms: (value) => validateCheckbox(Boolean(value)),
    },
    onSubmit: async (fields) => {
      const email = String(fields.email).trim().toLowerCase();
      const result = await signUp({
        fullName: String(fields.fullName),
        email,
        password: String(fields.password),
        phoneNumber: toE164(String(fields.phoneDialCode), String(fields.phoneNumber)),
      });
      // The API always answers with the same generic line, so a taken email
      // stays private. Then send the visitor to sign in.
      return (
        <span>
          {result.message ??
            "If that email is available, a 6-digit verification code is on its way."}{" "}
          <button className="btn-link" onClick={() => navigate("/login")} type="button">
            Continue to sign in
          </button>
        </span>
      );
    },
    invalidMessage: "Please check the highlighted fields before creating your account.",
  });

  return (
    <AuthLayout>
      <div className="animate-fade-rise rounded-2xl border border-white/10 bg-white/[0.04] p-6 shadow-card backdrop-blur sm:p-8">
        <header className="mb-6">
          <h2 className="text-2xl font-semibold text-white sm:text-[26px]">
            Create your account
          </h2>
          <p className="mt-1.5 text-sm text-slate-400">
            One account for the builder, the previews and your version history.
          </p>
        </header>

        <form className="space-y-4" noValidate onSubmit={handleSubmit} ref={formRef}>
          {alert ? <AuthAlert message={alert.message} variant={alert.variant} /> : null}
          {serverError ? (
            <AuthAlert
              message={toAuthErrorMessage(serverError, "We couldn't create your account. Please try again.")}
              variant="error"
            />
          ) : null}

          <AuthInput
            autoComplete="name"
            error={errors.fullName}
            icon={User}
            label="Full name"
            name="fullName"
            onBlur={() => handleBlur("fullName")}
            onChange={(event) => setValue("fullName", event.target.value)}
            placeholder="Alex Rivera"
            value={String(values.fullName)}
          />

          <AuthInput
            autoComplete="email"
            error={errors.email}
            icon={Mail}
            label="Email address"
            name="email"
            onBlur={() => handleBlur("email")}
            onChange={(event) => setValue("email", event.target.value)}
            placeholder="you@company.com"
            value={String(values.email)}
          />

          <PhoneInput
            dialCode={String(values.phoneDialCode)}
            error={errors.phoneNumber}
            name="phoneNumber"
            national={String(values.phoneNumber)}
            onBlur={() => handleBlur("phoneNumber")}
            onDialCodeChange={(event) => setValue("phoneDialCode", event.target.value)}
            onNationalChange={(event) => setValue("phoneNumber", event.target.value)}
          />

          <div>
            <AuthInput
              autoComplete="new-password"
              error={errors.password}
              icon={Lock}
              label="Password"
              name="password"
              onBlur={() => handleBlur("password")}
              onChange={(event) => setValue("password", event.target.value)}
              placeholder="At least 10 characters"
              type="password"
              value={String(values.password)}
            />
            <PasswordStrength password={String(values.password)} />
          </div>

          <AuthInput
            autoComplete="new-password"
            error={errors.confirmPassword}
            icon={CheckCircle2}
            label="Confirm password"
            name="confirmPassword"
            onBlur={() => handleBlur("confirmPassword")}
            onChange={(event) => setValue("confirmPassword", event.target.value)}
            placeholder="Re-enter your password"
            type="password"
            value={String(values.confirmPassword)}
          />

          <AuthCheckbox
            checked={Boolean(values.terms)}
            error={errors.terms}
            label="I agree to the Terms of Service and Privacy Policy."
            name="terms"
            onBlur={() => handleBlur("terms")}
            onChange={(event) => setValue("terms", event.target.checked)}
          />

          <AuthButton loading={isSubmitting}>
            {isSubmitting ? "Creating your account..." : "Create Account"}
          </AuthButton>
        </form>

        <p className="mt-6 text-center text-sm text-slate-400">
          Already have an account?{" "}
          <Link className="btn-link" to="/login">
            Sign in
          </Link>
        </p>
      </div>
    </AuthLayout>
  );
}
