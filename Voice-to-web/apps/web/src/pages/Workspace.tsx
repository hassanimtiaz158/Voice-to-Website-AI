import { ChatPanel } from "../features/chat/ChatPanel";
import { FileViewer } from "../features/files/FileViewer";
import { GithubPanel } from "../features/github/GithubPanel";

export const Workspace = () => (
  <div className="workspace">
    <ChatPanel />
    <section>
      <GithubPanel />
      <FileViewer />
    </section>
  </div>
);
