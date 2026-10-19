import { useMutation } from "@tanstack/react-query";
import { useCallback, useRef, useState } from "react";

export function useAuthForm({ initialValues, validators, onSubmit, invalidMessage }) {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [alert, setAlert] = useState(null);
  const formRef = useRef(null);

  const mutation = useMutation({ mutationFn: onSubmit });

  const runField = useCallback(
    (name, nextValues) => {
      const error = validators[name]?.(nextValues[name], nextValues);
      setErrors((current) => ({ ...current, [name]: error }));
      return error;
    },
    [validators]
  );

  const setValue = useCallback(
    (name, value) => {
      setValues((current) => {
        const next = { ...current, [name]: value };
        if (touched[name]) runField(name, next);
        return next;
      });
      if (value) setAlert(null);
    },
    [runField, touched]
  );

  const handleBlur = useCallback(
    (name) => {
      setTouched((current) => ({ ...current, [name]: true }));
      runField(name, values);
    },
    [runField, values]
  );

  const handleSubmit = useCallback(
    async (event) => {
      event.preventDefault();
      if (mutation.isPending) return;

      const nextErrors = {};
      for (const [name, validate] of Object.entries(validators)) {
        const error = validate(values[name], values);
        if (error) nextErrors[name] = error;
      }
      setErrors(nextErrors);
      setTouched(Object.fromEntries(Object.keys(values).map((name) => [name, true])));
      setAlert(null);

      const firstInvalid = Object.keys(nextErrors)[0];
      if (firstInvalid) {
        setAlert({
          variant: "error",
          message: invalidMessage ?? "Please fix the highlighted fields.",
        });
        formRef.current?.querySelector(`[name="${firstInvalid}"]`)?.focus();
        return;
      }

      try {
        const success = await mutation.mutateAsync(values);
        if (success) setAlert({ variant: "success", message: success });
      } catch {
        // The rejection is kept in mutation.error so the page can show safe wording.
      }
    },
    [invalidMessage, mutation, values, validators]
  );

  return {
    values,
    errors,
    alert,
    setAlert,
    setValue,
    handleBlur,
    handleSubmit,
    formRef,
    isSubmitting: mutation.isPending,
    serverError: mutation.error ?? null,
  };
}
