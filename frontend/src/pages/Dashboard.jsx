import { useAuth } from "../store/auth";

export function Dashboard() {
  const user = useAuth((state) => state.user);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-3 bg-navy-950 px-5 text-center">
      <h1 className="text-2xl font-semibold text-white">
        {user ? `Welcome, ${user.full_name ?? user.email}` : "Not signed in"}
      </h1>
      <p className="text-sm text-slate-400">
        {user
          ? "Your dashboard is coming next. For now, this confirms the session."
          : "Head to /login or /signup to continue."}
      </p>
    </main>
  );
}
