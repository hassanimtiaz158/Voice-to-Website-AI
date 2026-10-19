import { useMutation } from "@tanstack/react-query";
import { MailCheck } from "lucide-react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AuthAlert } from "../components/AuthAlert";
import { AuthButton } from "../components/AuthButton";
import { AuthLayout } from "../components/AuthLayout";
import { OtpInput } from "../components/OtpInput";
import { useCountdown } from "../hooks/useCountdown";
import { resendVerificationCode, toAuthErrorMessage, verifyEmail } from "../services/authService";
import { useAuth } from "../store/auth";
import { OTP_TTL_SECONDS, validateOtp } from "../utils/validation";

const RESEND_COOLDOWN = 60;

export function VerifyEmail() {
  const navigate = useNavigate();
  const email = useAuth((state) => state.pendingEmail);

  const [code, setCode] = useState("");
  const [fieldError, setFieldError] = useState();
  const [alert, setAlert] = useState(null);
  const [verified, setVerified] = useState(false);
  const [secondsLeft, startCooldown] = useCountdown();
  const [expiryLeft, startExpiry] = useCountdown();
  const [expiryStarted, setExpiryStarted] = useState(false);
  const expired = expiryStarted && expiryLeft === 0;

  useEffect(() => {
    if (!email) navigate("/signup", { replace: true });
  }, [email, navigate]);

  // The signup call that landed us here just sent a code, so its minute starts now.
  useEffect(() => {
    startExpiry(OTP_TTL_SECONDS);
    setExpiryStarted(true);
  }, [startExpiry]);

  const verify = useMutation({
    mutationFn: (value) => verifyEmail({ email, code: value }),
    onSuccess: () => setVerified(true),
  });

  useEffect(() => {
    if (expired) {
      setCode("");
      setFieldError(undefined);
      verify.reset();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [expired]);

  const resend = useMutation({
    mutationFn: () => resendVerificationCode({ email }),
    onSuccess: () => {
      startCooldown(RESEND_COOLDOWN);
      startExpiry(OTP_TTL_SECONDS);
      setCode("");
      setFieldError(undefined);
      verify.reset();
      setAlert({
        variant: "info",
        message: "If that email is registered, a fresh 6-digit code is on its way.",
      });
    },
  });

  if (!email) return null;

  const runVerify = (value) => {
    const error = validateOtp(value);
    setFieldError(error);
    if (error) return;
    verify.mutate(value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    runVerify(code);
  };

  const handleChange = (value) => {
    setCode(value);
    if (fieldError) setFieldError(validateOtp(value));
    if (verify.error) verify.reset();
  };

  if (verified) {
    return (
      <AuthLayout>
        <div className="animate-fade-rise rounded-2xl border border-white/10 bg-white/[0.04] p-6 text-center shadow-card backdrop-blur sm:p-8">
          <span className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-brand-gradient">
            <MailCheck className="h-6 w-6 text-white" />
          </span>
          <h2 className="text-2xl font-semibold text-white">Email verified</h2>
          <p className="mt-1.5 text-sm text-slate-400">
            {email} is confirmed. Sign in to start building.
          </p>
          <button className="btn-primary mt-6" onClick={() => navigate("/login")} type="button">
            Continue to sign in
          </button>
        </div>
      </AuthLayout>
    );
  }

  const serverError = verify.error ?? resend.error;
  const verifying = verify.isPending;

  return (
    <AuthLayout>
      <div className="animate-fade-rise rounded-2xl border border-white/10 bg-white/[0.04] p-6 shadow-card backdrop-blur sm:p-8">
        <header className="mb-6">
          <h2 className="text-2xl font-semibold text-white sm:text-[26px]">Check your inbox</h2>
          <p className="mt-1.5 text-sm text-slate-400">
            We sent a 6-digit verification code to{" "}
            <span className="font-medium text-slate-200">{email}</span>. Enter it below to activate
            your account.
          </p>
        </header>

        <form className="space-y-5" noValidate onSubmit={handleSubmit}>
          {alert ? <AuthAlert message={alert.message} variant={alert.variant} /> : null}
          {serverError ? (
            <AuthAlert
              message={toAuthErrorMessage(serverError, "We couldn't verify that code. Please try again.")}
              variant="error"
            />
          ) : null}

          <div>
            <OtpInput
              disabled={verifying || expired}
              error={fieldError}
              onChange={handleChange}
              onComplete={runVerify}
              value={code}
            />
            {fieldError ? (
              <p className="auth-error">{fieldError}</p>
            ) : (
              <p className={`mt-1.5 text-xs font-medium ${expired ? "text-rose-300" : "text-slate-400"}`}>
                {expired
                  ? "This code has expired. Resend a new one."
                  : `The code expires in ${expiryLeft}s.`}
              </p>
            )}
          </div>

          <AuthButton disabled={expired} loading={verifying}>
            {verifying ? "Verifying..." : "Verify Email"}
          </AuthButton>
        </form>

        <div className="mt-6 flex flex-wrap items-center justify-between gap-x-4 gap-y-1 text-sm text-slate-400">
          <span>Didn't get the code?</span>
          <button
            className="btn-link min-h-[44px] cursor-pointer disabled:cursor-not-allowed disabled:opacity-60"
            disabled={resend.isPending || secondsLeft > 0}
            onClick={() => resend.mutate()}
            type="button"
          >
            {resend.isPending
              ? "Sending..."
              : secondsLeft > 0
                ? `Resend code in ${secondsLeft}s`
                : "Resend code"}
          </button>
        </div>

        <p className="mt-4 text-center text-sm text-slate-400">
          Wrong address?{" "}
          <button
            className="btn-link"
            onClick={() => navigate("/signup")}
            type="button"
          >
            Back to sign up
          </button>
        </p>
      </div>
    </AuthLayout>
  );
}
