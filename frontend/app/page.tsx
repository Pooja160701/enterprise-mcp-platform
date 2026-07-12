import DashboardLayout from "@/components/layout/DashboardLayout";
import ChatWindow from "@/components/chat/ChatWindow";
import ActivityPanel from "@/components/activity/ActivityPanel";

export default function Home() {
  return (
    <DashboardLayout activity={<ActivityPanel />}>
      <ChatWindow />
    </DashboardLayout>
  );
}