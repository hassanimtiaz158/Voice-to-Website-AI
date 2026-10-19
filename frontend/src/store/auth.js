import { create } from "zustand";
import { fetchCurrentUser } from "../services/authService";

export const useAuth = create((set) => ({
  // Public profile only. Tokens stay in HttpOnly cookies and never reach JS.
  user: null,
  status: "idle",
  setUser: (user) => set({ user, status: "authenticated" }),
  clear: () => set({ user: null, status: "anonymous" }),
  restore: async () => {
    set({ status: "loading" });
    try {
      set({ user: await fetchCurrentUser(), status: "authenticated" });
    } catch {
      set({ user: null, status: "anonymous" });
    }
  },
}));
