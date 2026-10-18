import { create } from "zustand";

type UI = { activeFile: string | null; setActiveFile: (f: string | null) => void };

export const useUI = create<UI>((set) => ({
  activeFile: null,
  setActiveFile: (activeFile) => set({ activeFile }),
}));
