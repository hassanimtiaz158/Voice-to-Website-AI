import { Check as Check2, Mic, Wand2 } from "lucide-react";

export function AuthLayout({ children }) {
  return (
    <div className="grid min-h-screen lg:grid-cols-[1.05fr_1fr]">
      <aside className="relative hidden overflow-hidden bg-navy-900 lg:flex lg:flex-col lg:justify-between lg:p-12">
        <div className="pointer-events-none absolute inset-0" aria-hidden="true">
          <div className="animate-float absolute -left-24 -top-24 h-96 w-96 rounded-full bg-brand-violet/25 blur-3xl" />
          <div className="absolute -bottom-32 right-0 h-96 w-96 rounded-full bg-brand-blue/25 blur-3xl" />
          <div className="absolute inset-0 bg-brand-gradient opacity-[0.08]" />
        </div>

        <div className="relative flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-gradient shadow-glow">
            <Mic className="h-5 w-5 text-white" />
          </span>
          <span className="text-lg font-semibold text-white">Voice-to-Website AI</span>
        </div>

        <div className="relative max-w-lg">
          <p className="mb-4 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs font-medium uppercase tracking-wider text-brand-cyan">
            <Wand2 className="h-3.5 w-3.5" /> Speak it. We build it.
          </p>
          <h1 className="text-4xl font-bold leading-tight text-white xl:text-5xl">
            Turn your ideas into{" "}
            <span className="bg-brand-gradient bg-clip-text text-transparent">live websites</span>{" "}
            with AI.
          </h1>
          <p className="mt-5 text-base leading-relaxed text-slate-300">
            Describe the site you want by voice or text. Our agents plan it, write it, test it in a
            sandbox, and hand you a preview you can keep editing.
          </p>
        </div>

        <div className="relative flex flex-wrap gap-x-6 gap-y-2 text-sm text-slate-400">
          <span className="inline-flex items-center gap-2">
            <Check2 className="h-4 w-4 text-brand-cyan" /> Voice and text briefs
          </span>
          <span className="inline-flex items-center gap-2">
            <Check2 className="h-4 w-4 text-brand-cyan" /> Sandboxed builds and tests
          </span>
          <span className="inline-flex items-center gap-2">
            <Check2 className="h-4 w-4 text-brand-cyan" /> Version history and rollback
          </span>
        </div>
      </aside>

      <main className="flex flex-col items-center justify-center bg-navy-950 px-5 py-10 sm:px-10">
        <div className="mb-8 flex items-center gap-3 lg:hidden">
          <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand-gradient">
            <Mic className="h-5 w-5 text-white" />
          </span>
          <h1 className="text-base font-semibold text-white">Voice-to-Website AI</h1>
        </div>
        <div className="w-full max-w-md">{children}</div>
      </main>
    </div>
  );
}
