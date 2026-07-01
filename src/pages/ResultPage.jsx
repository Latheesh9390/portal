import { useLocation, Link } from "react-router-dom";
import MemoDisplay from "../components/MemoDisplay";

export default function ResultPage() {
  const { state } = useLocation();
  const memo = state?.memo;

  if (!memo) {
    return (
      <div className="min-h-screen bg-portal-bg flex flex-col items-center justify-center p-6">
        <p className="text-gray-500 mb-4">No result data found.</p>
        <Link to="/" className="text-portal-blue underline">← Go Back</Link>
      </div>
    );
  }

  const handlePrint = () => window.print();

  return (
    <div className="min-h-screen bg-portal-bg">
      <header className="bg-portal-navy text-white px-6 py-4 flex items-center justify-between print:hidden">
        <div>
          <p className="font-bold text-lg">KEC Results Portal</p>
          <p className="text-xs text-white/60">Kuppam Engineering College (Autonomous)</p>
        </div>
        <div className="flex gap-3">
          <button onClick={handlePrint} className="text-sm border border-white/30 px-4 py-1.5 rounded hover:bg-white/10 transition-colors">
            🖨️ Print
          </button>
          <Link to="/" className="text-sm border border-white/30 px-4 py-1.5 rounded hover:bg-white/10 transition-colors">
            ← Back
          </Link>
        </div>
      </header>

      <MemoDisplay memo={memo} />
    </div>
  );
}
